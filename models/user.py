from sqlalchemy import Column, Integer, Text, TIMESTAMP
from . import Base
from .enums.user_role import UserRole
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Text, unique=True)
    password_hash = Column(Text)
    email = Column(Text)
    created_at = Column(TIMESTAMP)
    name = Column(Text)
    surname = Column(Text)
    role = Column(Text, default=UserRole.user.value) 

    permissions = relationship("DeterrencePermission", back_populates="user")