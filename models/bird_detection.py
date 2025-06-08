from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, Float, Text
from . import Base
from sqlalchemy.orm import relationship

class BirdDetection(Base):
    __tablename__ = 'bird_detections'
    id = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP)
    video_id = Column(Integer, ForeignKey('recorded_videos.id'))
    confidence = Column(Float)
    bird_lowest_amount = Column(Integer)
    bird_highest_amount = Column(Integer)
    video_path = Column(Text)

    video = relationship("RecordedVideo", back_populates="detections")
    permission = relationship("DeterrencePermission", back_populates="detection", uselist=False)