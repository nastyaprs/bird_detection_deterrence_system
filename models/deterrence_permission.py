from sqlalchemy import Column, Integer, Boolean, ForeignKey, TIMESTAMP
from models import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class DeterrencePermission(Base):
    __tablename__ = 'deterrence_permission'

    id = Column(Integer, primary_key=True)
    detection_id = Column(Integer, ForeignKey('bird_detections.id'), unique=True)
    user_id = Column(Integer, ForeignKey("users.id")) 
    allow = Column(Boolean, nullable=True, default=None)
    issued_at = Column(TIMESTAMP, default=datetime.now)

    detection = relationship("BirdDetection", back_populates="permission")
    user = relationship("User", back_populates="permissions")