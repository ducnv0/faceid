from typing import Any

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.services.crud_person import service_instance as crud_person
from src import schemas
from src.api import dependencies as deps


router = APIRouter()


@router.get('', response_model=list[schemas.PersonResponse])
def get_people(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Retrieve People
    """
    people = crud_person.get_multi(db, skip=skip, limit=limit)
    return people


@router.post('', response_model=schemas.PersonResponse)
def create_person(
    *,
    db: Session = Depends(deps.get_db),
    person_in: schemas.PersonCreate,
) -> Any:
    """
    Create new person
    """
    person = crud_person.get_by_email(db, email=person_in.email)
    if person:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The user with this email already exists in the system.'
        )
    person = crud_person.create(db, obj_in=person_in)
    return person


@router.put('', response_model=schemas.PersonResponse)
def update_person(
    *,
    db: Session = Depends(deps.get_db),
    person_in: schemas.PersonUpdate,
) -> Any:
    """
    Update an existing person
    """
    person_with_id = crud_person.get(db, id=person_in.id)
    if not person_with_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The user with this id does not exist in the system.'
        )
    
    person_with_email = crud_person.get_by_email(db, email=person_in.email)
    if person_with_email and person_with_email.id != person_with_id.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The user with this email already exists in the system.'
        )

    person = crud_person.update(db, db_obj=person_with_id, obj_in=person_in)
    return person
