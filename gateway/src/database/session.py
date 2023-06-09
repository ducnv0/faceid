from sqlalchemy.orm import sessionmaker

from src.database.engine import engine


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
