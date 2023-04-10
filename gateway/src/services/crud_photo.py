from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.services.crud_base import CRUDBase
from src.models.photo import Photo
from src.schemas.photo import PhotoCreate, PhotoUpdate


class CRUDPhoto(CRUDBase[Photo, PhotoCreate, PhotoUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: PhotoCreate, owner_id: int
    ) -> Photo:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_multiple_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> list[Photo]:
        return (
            db.query(Photo)
            .filter(Photo.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def update(self):
        raise RuntimeError('Person updation is not supported!')
    

service_instance = CRUDPhoto(Photo)
