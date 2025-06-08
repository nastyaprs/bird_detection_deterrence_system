from sqlalchemy import Column, Integer, Text, TIMESTAMP, JSON, ForeignKey
from . import Base
from sqlalchemy.orm import relationship
from models.deterrent_system import DeterrentSystem
from models.user import User

class DeterrenceAction(Base):
    __tablename__ = 'deterrence_actions'
    id = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP)
    detection_id = Column(Integer, ForeignKey('bird_detections.id'))
    deterrent_id = Column(Integer, ForeignKey('deterrent_systems.id'))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True) 

    deterrent = relationship("DeterrentSystem")
    user = relationship("User")