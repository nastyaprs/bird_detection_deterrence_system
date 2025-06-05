from sqlalchemy import Column, Integer, Text, TIMESTAMP, JSON, ForeignKey
from . import Base

class DeterrenceAction(Base):
    __tablename__ = 'deterrence_actions'
    id = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP)
    device_type = Column(Text)
    action = Column(Text)
    parameters = Column(JSON)
    triggered_by = Column(Integer)
    detection_id = Column(Integer, ForeignKey('bird_detections.id'))
    deterrent_id = Column(Integer, ForeignKey('deterrent_systems.id'))