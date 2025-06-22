from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class WorkEvent(SQLModel, table=True):
    """
    /events で作成する「作業イベント」のテーブルモデル
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str
    action: str
    content: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        orm_mode = True

class Session(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str
    work_name: Optional[str] = None
    start_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    planned_end: datetime
    actual_end: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
