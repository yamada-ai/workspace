from fastapi import APIRouter
from fastapi import Response
from typing import List
from pydantic import BaseModel
from datetime import datetime
from .db import save_event, init_db, fetch_events  # fetch_events を追加

router = APIRouter(prefix="/api")

class WorkEventIn(BaseModel):
    user_name: str
    action: str
    content: str

class WorkEventOut(BaseModel):
    id: int
    user_name: str
    action: str
    content: str
    created_at: datetime

@router.on_event("startup")
async def startup():
    await init_db()

@router.options("/work-events")
async def preflight():
    return Response(status_code=200)

@router.post("/work-events", response_model=dict)
async def receive_work_event(event: WorkEventIn):
    await save_event(event.user_name, event.action, event.content)
    return {"status": "ok"}

@router.get("/work-events", response_model=List[WorkEventOut])
async def list_work_events():
    return await fetch_events()
