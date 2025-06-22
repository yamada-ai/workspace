from sqlmodel import Session as DBSession
from datetime import datetime, timedelta
from typing import List

from app.db.init_db import engine
from app.db.models import Session as WorkSession

def create_session(user_name: str, work_name: str, planned_minutes: int) -> WorkSession:
    now = datetime.utcnow()
    planned_end = now + timedelta(minutes=planned_minutes)

    with DBSession(engine) as session:
        new_session = WorkSession(
            user_name=user_name,
            work_name=work_name,
            start_time=now,
            planned_end=planned_end,
        )
        session.add(new_session)
        session.commit()
        session.refresh(new_session)
        return new_session

def list_sessions(limit: int = 100) -> List[WorkSession]:
    with DBSession(engine) as session:
        results = session.query(WorkSession).order_by(WorkSession.created_at.desc()).limit(limit).all()
        return results
