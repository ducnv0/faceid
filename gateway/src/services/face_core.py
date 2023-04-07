# This should be moved to a dedicated service for better scalability
from abc import ABC, abstractmethod
import os

from deepface import DeepFace


class FaceCore(ABC):

    @abstractmethod
    def detect_faces(self, img_path: str) -> tuple[dict]:
        """
        Detect faces from an image
        Example return value:       
        (
            {'x': 52, 'y': 40, 'w': 83, 'h': 83},
            {'x': 50, 'y': 20, 'w': 65, 'h': 72},
        )
        """
        raise NotImplementedError()
    
    @abstractmethod
    def detect_and_extract_embeddings(self, img_path: str) -> tuple[dict]:
        """
        Detect faces from an image then extract embeddings of these faces
        Example return value:       
        (   
            {
                'embedding': [0.3164752125740051, -1.8336374759674072, ...],
                'facial_area': {'x': 50, 'y': 20, 'w': 65, 'h': 72}
            },
            {
                'embedding': [0.3164752125740051, -1.8336374759674072, ...],
                'facial_area': {'x': 50, 'y': 20, 'w': 65, 'h': 72}
            },
        )
        """
        raise NotImplementedError()


class DeepFaceWrapper(FaceCore):
    def __init__(self) -> None:
        super().__init__()
        self.detector_backend = os.getenv('DEEP_FACE_DETECTOR_BACKEND', 'opencv')
        self.model_name = os.getenv('DEEP_FACE_MODEL_NAME', 'Facenet')

    def detect_faces(self, img_path: str) -> tuple[dict]:
        face_objects = DeepFace.extract_faces(
            img_path=img_path,
            detector_backend=self.detector_backend,
        )
        results = []
        for face_object in face_objects:
            results.append(face_object['facial_area'])
        
        return tuple(results)

    def detect_and_extract_embeddings(self, img_path: str) -> tuple[dict]:
        face_objects = DeepFace.represent(
            img_path=img_path,
            model_name=self.model_name,
            detector_backend=self.detector_backend,
        )
        results = []
        for face_object in face_objects:
            results.append({
                'embedding': face_object['embedding'],
                'facial_area': face_object['facial_area'],
            })
        
        return tuple(results)

