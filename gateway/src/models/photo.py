from sqlalchemy import Column, ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from src.database.base import Base


class Photo(Base):
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('person.id'))
    upload_time = Column(DateTime(timezone=True), server_default=now())
    url = Column(String)

    owner = relationship('Person', back_populates='photos')
