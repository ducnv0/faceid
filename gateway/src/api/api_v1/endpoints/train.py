from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.services.face import service_instance as face_service
from src.api import dependencies as deps


router = APIRouter()


@router.post('')
def train(*, db: Session = Depends(deps.get_db)): 
    face_service.train(db)
    return 'DONE'
