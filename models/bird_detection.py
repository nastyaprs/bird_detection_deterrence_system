from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, Float
from . import Base

class BirdDetection(Base):
    __tablename__ = 'bird_detections'
    id = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP)
    video_id = Column(Integer, ForeignKey('recorded_videos.id'))
    confidence = Column(Float)
    bird_lowest_amount = Column(Integer)
    bird_highest_amount = Column(Integer)