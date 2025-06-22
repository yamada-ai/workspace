from fastapi import APIRouter
from typing import List

from app.schemas.session import SessionCreate, SessionRead
from app.services.session_service import create_session, list_sessions

router = APIRouter(prefix="/sessions", tags=["Session"])

@router.post("", response_model=SessionRead, status_code=201)
def post_session(session_in: SessionCreate):
    session = create_session(
        user_name=session_in.user_name,
        work_name=session_in.work_name,
        planned_minutes=session_in.planned_minutes
    )
    return session

@router.get("", response_model=List[SessionRead])
def get_sessions(limit: int = 100):
    return list_sessions(limit=limit)
