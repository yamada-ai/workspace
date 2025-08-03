# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
import os

from app.db.init_db import init_db
from app.socket.socket import ws_manager
from app.controller.session_controller import router as session_controller  
from app.controller.user_controller import router as user_controller

app = FastAPI(
    title="Work Tracker MVP",
    description="SQLModel + FastAPI で構築する作業イベント管理サービス",
    version="0.1.0",
    root_path=os.getenv("FASTAPI_ROOT_PATH", "")  # ← ここだけ
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        print("WebSocket disconnected")
        await ws_manager.disconnect(websocket)
        
app.include_router(session_controller)
app.include_router(user_controller)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
