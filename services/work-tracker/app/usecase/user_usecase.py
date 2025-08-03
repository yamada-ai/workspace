from sqlmodel import Session as DBSession
from datetime import datetime, timedelta, timezone
from typing import List

from app.db.init_db import engine
from app.db.models import User

def create_user(
    db: DBSession, 
    user_name: str, 
    role_id: int = None
) -> User:
    now = datetime.now(timezone.utc)

    new_user = User(
        name=user_name,
        role_id=role_id,
        created_at=now,
        updated_at=now
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def list_users(limit: int = 100) -> List[User]:
    with DBSession(engine) as session:
        results = session.query(User).order_by(User.created_at.desc()).limit(limit).all()
        return results

def get_user_by_id(user_id: int) -> User:
    with DBSession(engine) as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return user