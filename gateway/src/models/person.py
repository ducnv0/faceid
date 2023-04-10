from sqlalchemy import Column, Float, String, Integer, DateTime, Boolean, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from  src.database.base import Base


class Person(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    create_time = Column(DateTime(timezone=True), server_default=now())
    # FIXME: server_onupdate does not work
    update_time = Column(DateTime(timezone=True), server_default=now(), server_onupdate=now())
    # TODO: add embedding

    photos = relationship('Photo', back_populates='owner')
