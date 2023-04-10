from fastapi import FastAPI

from src.database.init_db import init_db
from src.utils.common import init_logging
from src.api.api_v1.api import api_router


init_db()
init_logging()
app = FastAPI()
app.include_router(api_router, prefix='/api/v1/faceid')

