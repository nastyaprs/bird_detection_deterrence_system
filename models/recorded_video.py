from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey
from . import Base
from models.camera import Camera
from sqlalchemy.orm import relationship

class RecordedVideo(Base):
    __tablename__ = 'recorded_videos'
    id = Column(Integer, primary_key=True)
    start_time = Column(TIMESTAMP)
    end_time = Column(TIMESTAMP)
    file_path = Column(Text)
    camera_id = Column(Integer, ForeignKey('cameras.id'))
    note = Column(Text)

    camera = relationship("Camera")
    detections = relationship("BirdDetection", back_populates="video")