import datetime

from pydantic import BaseModel


class PhotoBase(BaseModel):
    photo_url: str


class PhotoCreate(PhotoBase):
    pass


class PhotoUpdate(PhotoBase):
    pass


class PhotoInDBBase(PhotoBase):
    id: int
    owner_id: int
    upload_time: datetime.datetime
    
    class Config:
        orm_mode = True

    
class PhotoResponse(PhotoInDBBase):
    pass
