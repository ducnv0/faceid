import logging
import os


LOGGER = logging.getLogger('faceid')


def init_logging():
    # remove default uvicorn logs
    logging.getLogger('uvicorn').handlers.clear()
    logging.basicConfig(level=os.getenv('LOG_LEVEL', 'DEBUG'))
