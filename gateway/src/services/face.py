import tempfile

from .face_core import DeepFaceWrapper


class FaceService():
    def __init__(self) -> None:
        self.face_core = DeepFaceWrapper()

    def detect_faces(self, bytes_img: bytes) -> tuple[dict]:
        with tempfile.NamedTemporaryFile() as tmpf:
            tmpf.write(bytes_img)
            results = self.face_core.detect_faces(tmpf.name)
        return results
