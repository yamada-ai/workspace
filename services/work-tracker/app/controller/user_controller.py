from fastapi import APIRouter, Depends
from typing import List
from sqlmodel import Session as DBSession

from app.domain.user import UserCreate, UserRead
from app.usecase.user_usecase import create_user, list_users
from app.infrastructure.user_repository_impl import UserRepositoryImpl
from app.db.init_db import get_session
from app.socket.socket import ws_manager
router = APIRouter(prefix="/users", tags=["User"])

@router.post("", response_model=UserRead, status_code=201)
async def post_session(
    user_in: UserCreate, 
    db: DBSession = Depends(get_session)
):
    repository = UserRepositoryImpl(db)
    user = create_user(
        repository=repository,
        user_name=user_in.user_name,
        role_id=user_in.role_id
    )

    return user

@router.get("", response_model=List[UserRead])
def get_sessions(db: DBSession = Depends(get_session), limit: int = 100):
    repository = UserRepositoryImpl(db)
    return list_users(repository=repository, limit=limit)
