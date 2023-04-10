from src.database.engine import engine
from src.database.base import Base
from src.models.person import Person  # noqa
from src.models.photo import Photo    # noqa

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
