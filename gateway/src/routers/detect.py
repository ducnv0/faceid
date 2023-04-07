import os
import tempfile

from fastapi import APIRouter, UploadFile

from ..services.face import FaceService


router = APIRouter()


@router.post('/detect')
async def detect_faces_rest(file: UploadFile):
    # TODO: improve this. Avoid directly call blocking operations
    facial_areas = FaceService().detect_faces(await file.read())

    return facial_areas

