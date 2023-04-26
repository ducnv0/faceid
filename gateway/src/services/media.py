from datetime import datetime, timedelta
import json

from external_utils.src.storage.minio.client import CustomMinio
from src.settings import settings


class MediaService():
    def __init__(self) -> None:
        self.minio = CustomMinio(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
            default_bucket=settings.MINIO_DEFAULT_BUCKET
        )

    def photo_presigned_put_object(self, person_id: int):
        filename = datetime.utcnow().isoformat()
        bucket_name = self.minio.default_bucket
        object_name = f'photo/{person_id}/{filename}'
        # FIXME: Consider to get expires time from environment variables for better flexibility
        expires = timedelta(minutes=5)
        presigned_put_url = self.minio.presigned_put_object(object_name=object_name, bucket_name=bucket_name,  expires=expires)
        
        return {
            'presigned_put_url': presigned_put_url,
            'object_name': object_name,
            'bucket_name': bucket_name
        }

    def update_embedding_data(self, embedding_data: list[dict]) -> None:
        data = json.dumps(embedding_data, indent=4)
        data = bytes(data, encoding='utf-8')
        # FIXME: parameterize object_name of embedding data
        self.minio.put_object(object_name='embedding_data.json', data=data, content_type='application/json')

    def get_embedding_data(self) -> list[dict]:
        data = self.minio.get_object('embedding_data.json')
        return json.loads(data)


service_instance = MediaService()

