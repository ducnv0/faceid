from typing import Optional

from sqlalchemy.orm import Session

from src.services.crud_base import CRUDBase
from src.models.person import Person
from src.schemas.person import PersonCreate, PersonUpdate


class CRUDPerson(CRUDBase[Person, PersonCreate, PersonUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Person]:
        return db.query(Person).filter(Person.email == email).first()
    
    def is_active(self, person: Person) -> bool:
        return person.is_active


service_instance = CRUDPerson(Person)
