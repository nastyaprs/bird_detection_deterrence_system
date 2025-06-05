from sqlalchemy import Column, Integer, Text
from . import Base

class Camera(Base):
    __tablename__ = 'cameras'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    interface_type = Column(Text)
    device_path = Column(Text)
    model = Column(Text)
