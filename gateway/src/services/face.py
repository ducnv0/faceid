import tempfile

import numpy as np

from src.core.face import DeepFaceWrapper


class FaceService():
    def __init__(self) -> None:
        self.face_core = DeepFaceWrapper()

    def detect_faces(self, bytes_img: bytes) -> tuple[dict]:
        with tempfile.NamedTemporaryFile() as tmpf:
            tmpf.write(bytes_img)
            results = self.face_core.detect_faces(tmpf.name)
        return results
    
    
    def get_general_embedding(self, bytes_imgs: list[bytes]) -> tuple[float]:
        embeddings = []
        for bytes_img in bytes_imgs:
            with tempfile.NamedTemporaryFile() as tmpf:
                tmpf.write(bytes_img)
                face_objects = self.face_core.detect_and_extract_embeddings(tmpf.name)
                if len(face_objects) > 0:
                    # for simplicity, If there're multiple faces in the photo, use the first face only
                    embeddings.append(face_objects[0]['embedding'])
        if len(embeddings) == 0:
            return ()
        return tuple(np.mean(embeddings, axis=0).tolist())
        

service_instance = FaceService()
