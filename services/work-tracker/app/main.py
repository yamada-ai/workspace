from fastapi import FastAPI
import uvicorn
import os

from app.db.init_db import init_db
from app.routers.work_event_router import router as work_event_router
from app.routers.session_router import router as session_router  

app = FastAPI(
    title="Work Tracker MVP",
    description="SQLModel + FastAPI で構築する作業イベント管理サービス",
    version="0.1.0",
)

root_path = os.getenv("FASTAPI_ROOT_PATH", "")
app = FastAPI(root_path=root_path)

# DB の初期化（テーブル作成など）をアプリ起動時に一度だけ実行
@app.on_event("startup")
def on_startup():
    init_db()

# ルータを登録
app.include_router(work_event_router)
app.include_router(session_router) 

# CLI／ローカル起動用
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)