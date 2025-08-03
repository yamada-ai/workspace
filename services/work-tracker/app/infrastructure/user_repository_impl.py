from typing import Optional, List
from sqlmodel import Session
from app.db.models import User
from app.domain.user_repository import UserRepository

class UserRepositoryImpl(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def list(self, limit: int = 100) -> List[User]:
        return self.session.query(User).order_by(User.created_at.desc()).limit(limit).all()

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.session.query(User).filter(User.id == user_id).first()
    
    def get_by_name(self, user_name: str) -> Optional[User]:
        return self.session.query(User).filter(User.name == user_name).first()
