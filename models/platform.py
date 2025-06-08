from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models import Base

class Platform(Base):
    __tablename__ = 'platforms'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    camera_id = Column(Integer, ForeignKey("cameras.id"), nullable=False)
    deterrent_system_id = Column(Integer, ForeignKey("deterrent_systems.id"), nullable=False)

    camera = relationship("Camera", backref="platforms")
    deterrent_system = relationship("DeterrentSystem", backref="platforms")