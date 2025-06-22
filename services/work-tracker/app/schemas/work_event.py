from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WorkEventCreate(BaseModel):
    """
    POST /events のリクエスト用スキーマ
    """
    user_name: str
    action: str
    content: Optional[str] = None

class WorkEventRead(BaseModel):
    """
    GET /events のレスポンス用スキーマ
    """
    id: int
    user_name: str
    action: str
    content: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
