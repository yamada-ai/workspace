from datetime import datetime, timedelta, timezone
from typing import List

from app.db.init_db import engine
from app.db.models import User
from app.infrastructure.user_repository_impl import UserRepositoryImpl

def create_user(
    repository: UserRepositoryImpl, 
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

    if repository.get_by_name(user_name) != None:
        raise ValueError(f"User with name '{user_name}' already exists.")

    return repository.add(new_user)

def list_users(repository: UserRepositoryImpl, limit: int = 100) -> List[User]:
    return repository.list(limit=limit)

def get_user_by_id(repository: UserRepositoryImpl, user_id: int) -> User:
    user = repository.get_by_id(user_id)
    if user is None:
        raise ValueError(f"User with ID '{user_id}' not found.")
    return user

def get_user_by_name(repository: UserRepositoryImpl, user_name: str) -> User:
    return repository.get_by_name(user_name)