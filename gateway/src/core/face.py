# This should be moved to a dedicated service for better scalability
from abc import ABC, abstractmethod
import os

from sklearn.metrics.pairwise import cosine_similarity
from deepface import DeepFace


class FaceCore(ABC):

    @abstractmethod
    def detect_faces(self, img_path: str) -> list[dict]:
        """
        Detect faces and identity from an image
        Example return value:
        [
            {
                'facial_area': {'x': 52, 'y': 40, 'w': 83, 'h': 83}
            },
            {
                'facial_area': {'x': 55, 'y': 43, 'w': 82, 'h': 30}
            }
        ]
        """
        raise NotImplementedError()
    
    @abstractmethod
    def detect_and_extract_embeddings(self, img_path: str) -> list[dict]:
        """
        Detect faces from an image then extract embeddings of these faces
        Example return value:       
        [  
            {
                'embedding': [0.3164752125740051, -1.8336374759674072, ...],
                'facial_area': {'x': 50, 'y': 20, 'w': 65, 'h': 72}
            },
            {
                'embedding': [0.3164752125740051, -1.8336374759674072, ...],
                'facial_area': {'x': 50, 'y': 20, 'w': 65, 'h': 72}
            },
        ]
        """
        raise NotImplementedError()
    
    def recognize(self, img_path: str, embedding_candidates: list[list[float]]):
        """
        Extract faces from image and compare their embedding similarities
        Example return value 
        [
             {
                'facial_area': {'x': 50, 'y': 20, 'w': 65, 'h': 72},
                'nearest': {
                    'index': 1,
                    'score': 0.3
                }
            },
            {
                'facial_area': {'x': 50, 'y': 20, 'w': 65, 'h': 72},
                'nearest': {
                    'index': 0,
                    'score': 0.9
                }
            },
        ]
        """
        results = []
        extraction_results = self.detect_and_extract_embeddings(img_path=img_path)
        for person in extraction_results:
            results.append({
                'facial_area': person['facial_area'],
                'nearest': self.get_nearest(current=person['embedding'], candidates=embedding_candidates)
            })
        return results
    
    def get_nearest(self, current: list[float], candidates: list[list[float]]) -> dict:
        distances = 1 - cosine_similarity([current], candidates)[0]
        index_min = distances.argmin()
        distance_min = distances[index_min]
        return {
            'index': int(index_min),
            'score': float(distance_min)
        }


class DeepFaceWrapper(FaceCore):
    def __init__(self) -> None:
        super().__init__()
        self.detector_backend = os.getenv('DEEP_FACE_DETECTOR_BACKEND', 'opencv')
        self.model_name = os.getenv('DEEP_FACE_MODEL_NAME', 'Facenet')

    def detect_faces(self, img_path: str) -> list[dict]:
        try:
            face_objects = DeepFace.extract_faces(
                img_path=img_path,
                detector_backend=self.detector_backend
            )
        except (ValueError, AttributeError):
            return []

        results = []
        for face_object in face_objects:
            results.append({
                'facial_area': face_object['facial_area']
            })
        
        return results

    def detect_and_extract_embeddings(self, img_path: str) -> list[dict]:
        try:
            face_objects = DeepFace.represent(
                img_path=img_path,
                model_name=self.model_name,
                detector_backend=self.detector_backend
            )
        except (ValueError, AttributeError): # Face could not be detected
            return []

        results = []
        for face_object in face_objects:
            results.append({
                'embedding': face_object['embedding'],
                'facial_area': face_object['facial_area'],
            })
        
        return results
