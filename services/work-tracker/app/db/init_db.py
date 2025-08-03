from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.engine import Engine
from contextlib import contextmanager
from app.config import DATABASE_URL
import time
import psycopg2
from psycopg2 import OperationalError

# create_engine は同期用。ここでは同期アクセスを想定
engine: Engine = create_engine(DATABASE_URL, echo=True)

def wait_for_postgres(host: str, port: int, user: str, password: str, db: str, retries=10):
    """
    PostgreSQL が起動するまで待機する
    """
    for i in range(retries):
        try:
            conn = psycopg2.connect(
                host=host, port=port, user=user, password=password, dbname=db
            )
            conn.close()
            print("PostgreSQL is ready")
            return
        except OperationalError:
            print(f"Waiting for PostgreSQL... ({i+1}/{retries})")
            time.sleep(1)
    raise RuntimeError("PostgreSQL did not become ready in time.")

def init_db():
    """
    アプリ起動時に呼んでおきたい「テーブルを存在しなければ作成」する関数
    """
    wait_for_postgres("db", 5432, "postgres", "postgres", "workspace")  # docker-compose.yml に合わせる
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
