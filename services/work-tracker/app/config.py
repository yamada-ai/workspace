import os
from dotenv import load_dotenv

load_dotenv()  # カレントディレクトリの .env を読み込む

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in .env")
