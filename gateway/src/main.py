from fastapi import FastAPI

from src.database.init_db import init_db
from src.utils.common import init_logging
from src.api.api_v1.api import api_router
from src.services.media import service_instance as media


app = FastAPI()
app.include_router(api_router, prefix='/api/v1/faceid')


@app.on_event('startup')
def startup_event():
    # TODO: migrate db
    init_db()
    init_logging()
    media.minio.create_default_bucket()
    # TODO: load models
