from sqlmodel import Session as DBSession
from datetime import datetime, timedelta, timezone
from typing import List

from app.db.init_db import engine
from app.db.models import Session, User
from app.domain.session_repository import SessionRepository
from app.domain.user_repository import UserRepository

def create_session(
    session_repository: SessionRepository, 
    user_repository: UserRepository,
    user_name: str, 
    work_name: str,
    planned_minutes: int
) -> Session:
    now = datetime.now(timezone.utc)
    planned_end = now + timedelta(minutes=planned_minutes)

    # 新規ユーザの場合は登録する
    user = (
        user_repository.get_by_name(user_name)
        or user_repository.add(User(
            name=user_name,
            role_id=1,
            created_at=now,
            updated_at=now
        ))
    )

    # 現在有効なセッションが存在する場合は生成しない
    if session_repository.get_active_by_user_id(user.id):
        raise ValueError(f"User '{user_name}' already has an active session.")

    new_session = Session(
        user_id=user.id,
        work_name=work_name,
        start_time=now,
        planned_end=planned_end
    )

    return session_repository.add(new_session), user

def list_sessions(repository: SessionRepository, limit: int = 100) -> List[Session]:
    return repository.list(limit=limit)
