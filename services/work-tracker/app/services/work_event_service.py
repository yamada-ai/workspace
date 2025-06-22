from sqlmodel import Session, select
from typing import List
from app.db.models import WorkEvent
from app.db.init_db import engine

def create_event(user_name: str, action: str, content: str = None) -> WorkEvent:
    """
    新しい WorkEvent を作成してデータベースに保存し、保存したレコードを返す。
    """
    with Session(engine) as session:
        event = WorkEvent(user_name=user_name, action=action, content=content)
        session.add(event)
        session.commit()
        session.refresh(event)
        return event

def list_events(limit: int = 100) -> List[WorkEvent]:
    """
    最新のイベントを created_at DESC で取得（デフォルト100件）
    """
    with Session(engine) as session:
        statement = select(WorkEvent).order_by(WorkEvent.created_at.desc()).limit(limit)
        results = session.exec(statement).all()
        return results
