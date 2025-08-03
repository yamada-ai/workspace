from fastapi import APIRouter, Depends
from typing import List
from sqlmodel import Session as DBSession

from app.domain.session import SessionCreate, SessionRead
from app.usecase.session_usecase import create_session, list_sessions
from app.db.init_db import get_session
from app.infrastructure.session_repository_impl import SessionRepositoryImpl
from app.infrastructure.user_repository_impl import UserRepositoryImpl
from app.socket.socket import ws_manager
router = APIRouter(prefix="/sessions", tags=["Session"])

@router.post("", response_model=SessionRead, status_code=201)
async def post_session(
    session_in: SessionCreate, 
    db: DBSession = Depends(get_session)
):
    session_repository = SessionRepositoryImpl(db)
    user_repository = UserRepositoryImpl(db)
    session = create_session(
        session_repository=session_repository,
        user_repository=user_repository,
        user_name=session_in.user_name,
        work_name=session_in.work_name,
        planned_minutes=session_in.planned_minutes
    )

    await ws_manager.broadcast({
        "id": session.id,
        "type": "session_start",
        "user_id": session.user_id,
        "work_name": session.work_name,
        "start_time": session.start_time.isoformat(),
        "planned_end": session.planned_end.isoformat()
    })

    return session

@router.get("", response_model=List[SessionRead])
def get_sessions(db: DBSession = Depends(get_session), limit: int = 100):
    repository = SessionRepositoryImpl(db)
    return list_sessions(repository=repository, limit=limit)