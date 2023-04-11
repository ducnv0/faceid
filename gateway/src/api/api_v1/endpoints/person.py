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
    Retrieve all people
    """
    people = crud_person.get_multi(db, skip=skip, limit=limit)
    return people


@router.get('/{id}', response_model=schemas.PersonResponse)
def get_person_by_id(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Retrieve a single person
    """
    person = crud_person.get(db, id=id)
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Person not found.'
        )
    return person
    

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


@router.put('/{id}', response_model=schemas.PersonResponse)
def update_person(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    person_in: schemas.PersonUpdate,
) -> Any:
    """
    Update an existing person
    """
    person_with_id = crud_person.get(db, id=id)
    if not person_with_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Person not found."
        )
    
    person_with_email = crud_person.get_by_email(db, email=person_in.email)
    if person_with_email and person_with_email != person_with_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already taken.'
        )

    person = crud_person.update(db, db_obj=person_with_id, obj_in=person_in)
    return person


@router.delete('/{id}', response_model=schemas.PersonResponse)
def delete_person(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete a person
    """
    person = crud_person.get(db, id=id)
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Person not found."
        )
    person = crud_person.remove(db, id=id)
    return person


# TODO: deactivate/activate person
# TODO: get all activate people
