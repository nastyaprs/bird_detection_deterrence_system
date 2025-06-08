from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP
from models import Base
from .enums.system_mode import SystemMode

class SystemState(Base):
    __tablename__ = 'system_state'

    id = Column(Integer, primary_key=True)
    mode = Column(String, default=SystemMode.auto.value)
    date_in = Column(TIMESTAMP, default=datetime.now)
