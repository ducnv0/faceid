import tempfile

import numpy as np
from fastapi import WebSocket
from fastapi.concurrency import run_in_threadpool
import asyncio
from sqlalchemy.orm import Session

from src.core.face import DeepFaceWrapper
from src.utils.common import LOGGER
from src.services.crud_person import service_instance as crud_person
from src.services.crud_photo import service_instance as crud_photo
from src.services.media import service_instance as media
from src.exceptions.websocket import WebsocketSendError

class FaceService():
    def __init__(self) -> None:
        self.face_core = DeepFaceWrapper()
        self.names = None
        self.embeddings = None
        self.embeddings_loaded = False
        try:
            self.reload_embedding_data()
        except:
            pass

    def detect(self, bytes_img: bytes) -> tuple[dict]:
        with tempfile.NamedTemporaryFile() as tmpf:
            tmpf.write(bytes_img)
            results = self.face_core.detect_faces(tmpf.name)
        return results

    def extract_general_embedding(self, bytes_imgs: list[bytes]) -> list[float]:
        embeddings = []
        for bytes_img in bytes_imgs:
            with tempfile.NamedTemporaryFile() as tmpf:
                tmpf.write(bytes_img)
                face_objects = self.face_core.detect_and_extract_embeddings(tmpf.name)
                if len(face_objects) > 0:
                    # for simplicity, If there're multiple faces in the photo, use the first face only
                    embeddings.append(face_objects[0]['embedding'])
        if len(embeddings) == 0:
            return []
        return np.mean(embeddings, axis=0).tolist()

    def reload_embedding_data(self):
        embedding_data = media.get_embedding_data()
        names = []
        embeddings = []
        for person in embedding_data:
            names.append(person['name'])
            embeddings.append(person['embedding'])
        self.names = names
        self.embeddings = embeddings
        self.embeddings_loaded = True

    def recognize(self, bytes_img: bytes, threshold: float = 0.3) -> list[dict]:
        results = []
        with tempfile.NamedTemporaryFile() as tmpf:
            tmpf.write(bytes_img)
            reg_results = self.face_core.recognize(img_path=tmpf.name, embedding_candidates=self.embeddings)
            for person in reg_results:
                score = person['nearest']['score']
                if score < threshold:
                    name = self.names[person['nearest']['index']]
                else:
                    name = 'Unknown'
                results.append({
                    'facial_area': person['facial_area'],
                    'identity': {
                        'name': name,
                        'score': score
                    }
                })

        return results

    def train(self, db: Session):
        model = []
        # TODO: handle skip/limit
        people = crud_person.get_multi(db)
        for person in people:
            # get all photos from s3
            photos = crud_photo.get_multiple_by_owner(db, owner_id=person.id)
            bytes_imgs = []
            for photo in photos:
                bytes_img = media.minio.get_object(object_name=photo.object_name, bucket_name=photo.bucket_name)
                bytes_imgs.append(bytes_img)

            # calculate embedding    
            embedding = self.extract_general_embedding(bytes_imgs)
            if len(embedding) > 0:
                model.append({
                    'id': person.id,
                    'name': person.full_name,
                    'embedding': embedding
                })
        media.update_embedding_data(model)
        self.reload_embedding_data()

    async def receive_imgs_helper(self, ws: WebSocket, queue: asyncio.Queue):
        """
        Wait to receive images from the client then put them to the queue
        """
        while True:
            bytes_img = await ws.receive_bytes()
            try:
                # LOGGER.debug('[ws] Received image: %s KB', len(bytes_img))
                queue.put_nowait(bytes_img)
            except asyncio.QueueFull:
                # drop new frame
                LOGGER.debug('[ws] Dropped new frame due to the queue exceeded its capacity')

    async def detect_faces_helper(self, ws: WebSocket, queue: asyncio.Queue, identity: bool = False):
        """
        Pull images from the image queue, run detections and send results back to the client
        """
        while True:
            bytes_img = await queue.get()
            if identity:
                results = await run_in_threadpool(self.recognize, bytes_img)
            else:
                results = await run_in_threadpool(self.detect, bytes_img)
            # LOGGER.debug('[ws] Sending detection results back to the client: %s', results)
            if len(results) > 0:
                try:
                    await ws.send_json(results)
                except RuntimeError:
                    raise WebsocketSendError


service_instance = FaceService()
