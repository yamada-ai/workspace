from abc import ABC, abstractmethod
from typing import List, Optional
from app.db.models import Session as SessionModel

class SessionRepository(ABC):
    @abstractmethod
    def add(self, session: SessionModel) -> SessionModel:
        pass

    @abstractmethod
    def list(self, limit: int = 100) -> List[SessionModel]:
        pass

    @abstractmethod
    def get_active_by_user_id(self, user_id: int) -> Optional[SessionModel]:
        """未終了（actual_endがNULL）のセッションを1件返す"""
        pass
