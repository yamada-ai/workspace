from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    user_name: str
    role_id: Optional[int]

class UserRead(BaseModel):
    id: int
    name: str
    role_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
