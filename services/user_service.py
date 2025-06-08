import hashlib
from models.user import User
from datetime import datetime
from sqlalchemy.orm import Session


class UserService:
    def __init__(self, db_session: Session):
        self.session = db_session

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate(self, username: str, password: str):
        hashed = self.hash_password(password)
        return self.session.query(User).filter_by(username=username, password_hash=hashed).first()

    def register(self, username: str, password: str, email: str, name: str, surname: str):
        existing_user = self.session.query(User).filter_by(username=username).first()
        if existing_user:
            return None 

        new_user = User(
            username=username,
            password_hash=self.hash_password(password),
            email=email,
            name=name,
            surname=surname,
            created_at=datetime.utcnow()
        )
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def get_by_id(self, user_id: int):
        return self.session.query(User).filter_by(id=user_id).first()
