from sqlmodel import Session as DBSession
from datetime import datetime, timedelta, timezone
from typing import List

from app.db.init_db import engine
from app.db.models import Session

def create_session(
    db: DBSession, 
    user_name: str, 
    work_name: str,
    planned_minutes: int
) -> Session:
    now = datetime.now(timezone.utc)
    planned_end = now + timedelta(minutes=planned_minutes)

    new_session = Session(
        user_name=user_name,
        work_name=work_name,
        start_time=now,
        planned_end=planned_end
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

def list_sessions(limit: int = 100) -> List[Session]:
    with DBSession(engine) as session:
        results = session.query(Session).order_by(Session.created_at.desc()).limit(limit).all()
        return results
