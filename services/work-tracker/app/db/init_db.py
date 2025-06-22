from sqlmodel import SQLModel, create_engine
from sqlalchemy.engine import Engine
from app.config import DATABASE_URL
from app.db.models import WorkEvent

# create_engine は同期用。ここでは同期アクセスを想定
engine: Engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    """
    アプリ起動時に呼んでおきたい「テーブルを存在しなければ作成」する関数
    """
    SQLModel.metadata.create_all(engine)
