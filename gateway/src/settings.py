from typing import Optional

from external_utils.src.storage.minio.settings import MinioSettings


class Settings(MinioSettings):
    LOG_LEVEL: str = 'DEBUG'
    WS_QUEUE_MAX_SIZE: int = 10


settings = Settings()
