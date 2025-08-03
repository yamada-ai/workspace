from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SessionCreate(BaseModel):
    user_name: str
    work_name: Optional[str] = None
    planned_minutes: int = 120  # デフォルトは 120分

class SessionRead(BaseModel):
    id: int
    user_id: int
    work_name: Optional[str]
    start_time: datetime
    planned_end: datetime
    actual_end: Optional[datetime]
    created_at: datetime

    class Config:
        orm_mode = True
