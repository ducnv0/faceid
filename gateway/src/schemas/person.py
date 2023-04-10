import datetime

from pydantic import BaseModel


# Shared properties
class PersonBase(BaseModel):
    full_name: str
    email: str


# Properties to receive via API on creation
class PersonCreate(PersonBase):
    pass


# Properties to receive via API on update
class PersonUpdate(PersonBase):
    id: int
    pass


# Properties shared by models stored in DB
class PersonInDBBase(PersonBase):
    id: int
    is_active: bool
    create_time: datetime.datetime
    update_time: datetime.datetime

    class Config:
        orm_mode = True


# Properties to return to client
class PersonResponse(PersonInDBBase):
    pass


# Properties stored in DB
class PersonInDB(PersonInDBBase):
    pass
