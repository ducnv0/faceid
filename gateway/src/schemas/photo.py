from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, validator, root_validator

from src.services.media import service_instance as media


class PhotoBase(BaseModel):
    pass

class PhotoCreate(PhotoBase):
    bucket_name: str
    object_name: str

    @root_validator
    def validate_object_exists(cls, values):
        bucket_name = values['bucket_name']
        object_name = values['object_name']
        if not media.minio.object_exists(bucket_name=bucket_name, object_name=object_name):
            raise ValueError('Photo is not uploaded!')

        return values


class PhotoUpdate(PhotoBase):
    pass


class PhotoInDBBase(PhotoBase):
    id: int
    owner_id: int
    bucket_name: str
    object_name: str
    upload_time: datetime

    class Config:
        orm_mode = True


class PhotoResponse(PhotoInDBBase):
    presigned_get_url: Optional[str]

    @validator('presigned_get_url', always=True, pre=True)
    def get_presigned_get_url(cls, value, values):
        if value:
            raise ValueError('Cannot assign value to presigned_url')
        bucket_name = values['bucket_name']
        object_name = values['object_name']
        presigned_get_url = media.minio.presigned_get_object(
            object_name=object_name,
            bucket_name=bucket_name,
            expires=timedelta(minutes=5)
        )

        return presigned_get_url


class PhotoInDB(PhotoInDBBase):
    pass


class PhotoPresignedPutResponse(BaseModel):
    presigned_put_url: str
    object_name: str
    bucket_name: str
