import os
import logging

from fastapi import FastAPI

from .routers.detect import router as detect_router


def init_logging():
    # remove default uvicorn logs
    logging.getLogger('uvicorn').handlers.clear()
    logging.basicConfig(level=os.getenv('LOG_LEVEL', 'DEBUG'))


init_logging()
app = FastAPI()
app.include_router(detect_router, prefix='/api/v1/faceid')
