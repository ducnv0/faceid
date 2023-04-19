from sqlalchemy.engine import create_engine


# FIXME: get from os env
SQLALCHEMY_DATABASE_URL = 'sqlite:///./database/sql_app.tmp.db'
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
engine = create_engine(
    url=SQLALCHEMY_DATABASE_URL,
    connect_args={
        'check_same_thread': False,
    }
)
