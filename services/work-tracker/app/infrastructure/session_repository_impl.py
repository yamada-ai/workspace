from typing import Optional, List
from sqlmodel import Session as DBSession
from app.db.models import Session as SessionModel
from app.domain.session_repository import SessionRepository

class SessionRepositoryImpl(SessionRepository):
    def __init__(self, db: DBSession):
        self.db = db

    def add(self, session: SessionModel) -> SessionModel:
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def list(self, limit: int = 100) -> List[SessionModel]:
        return self.db.query(SessionModel).order_by(SessionModel.created_at.desc()).limit(limit).all()
    
    def get_active_by_user_id(self, user_id: int) -> Optional[SessionModel]:
        return self.db.query(SessionModel).filter(
            SessionModel.user_id == user_id,
            SessionModel.actual_end.is_(None)
        ).order_by(SessionModel.start_time.desc()).first()
