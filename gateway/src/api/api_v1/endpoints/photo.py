from typing import Any

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.services.crud_photo import service_instance as crud_photo
from src.services.crud_person import service_instance as crud_person
from src.services.media import service_instance as media
from src import schemas
from src.api import dependencies as deps


router = APIRouter()


@router.get('/person/{person_id}', response_model=list[schemas.PhotoResponse])
def get_photos(
    *,
    db: Session = Depends(deps.get_db),
    person_id: int,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get multiple photos of a person
    """
    photos = crud_photo.get_multiple_by_owner(
        db, owner_id=person_id, skip=skip, limit=limit
    )
    return photos


@router.post('/person/{person_id}', response_model=schemas.PhotoResponse)
def create_photo(
    *,
    db: Session = Depends(deps.get_db),
    person_id: int,
    photo_in: schemas.PhotoCreate,
) -> Any:
    """
    Create new photo
    """
    person = crud_person.get(db, id=person_id)
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Person not found."
        )
    
    photo = crud_photo.create_with_owner(
        db, obj_in=photo_in, owner_id=person_id
    )
    return photo


@router.delete('/{id}', response_model=schemas.PhotoResponse)
def delete_photo(
    *,
    db: Session = Depends(deps.get_db),
    id: int
) -> Any:
    """
    Delete an photo
    """
    photo = crud_photo.get(db, id=id)
    if not photo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Photo not found."
        )
    photo = photo.remove(db, id=id)
    # TODO: delete from s3

    return photo


@router.get('/presigned_put/person/{person_id}', response_model=schemas.PhotoPresignedPutResponse)
def get_presigned_put_url(
    *,
    db: Session = Depends(deps.get_db),
    person_id: int,
) -> Any:
    """
    Get presigned url to upload photo
    """
    person = crud_person.get(db, id=person_id)
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Person not found."
        )
        
    return media.photo_presigned_put_object(person_id)

