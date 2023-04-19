import logging


LOGGER = logging.getLogger('faceid')


def init_logging(level):
    # remove default uvicorn logs
    logging.getLogger('uvicorn').handlers.clear()
    logging.basicConfig(level=level)
