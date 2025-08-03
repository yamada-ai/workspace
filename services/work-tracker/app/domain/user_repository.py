from abc import ABC, abstractmethod
from typing import Optional, List
from app.db.models import User  # または domain.model.user

class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> User:
        pass

    @abstractmethod
    def list(self, limit: int = 100) -> List[User]:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_name(self, user_name: str) -> Optional[User]:
        pass
    