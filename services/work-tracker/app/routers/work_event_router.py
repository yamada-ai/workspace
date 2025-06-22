from fastapi import APIRouter, HTTPException
from typing import List

from app.schemas.work_event import WorkEventCreate, WorkEventRead
from app.services.work_event_service import create_event, list_events

router = APIRouter(prefix="/events", tags=["WorkEvent"])

@router.post("", response_model=WorkEventRead, status_code=201)
def post_event(event_in: WorkEventCreate):
    """
    新しい作業イベントを作成する
    """
    try:
        event = create_event(
            user_name=event_in.user_name,
            action=event_in.action,
            content=event_in.content,
        )
        return event
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[WorkEventRead])
def get_events(limit: int = 100):
    """
    最新の作業イベントを取得する
    query parameter: limit (最大取得件数)
    """
    return list_events(limit=limit)
