from sqlalchemy import Column, Integer, Text
from . import Base

class DeterrentSystem(Base):
    __tablename__ = 'deterrent_systems'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    type = Column(Text, 'laser')
    model = Column(Text)