from fastapi import FastAPI
from app.api import router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(router)
