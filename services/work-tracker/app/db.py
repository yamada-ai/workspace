import os, asyncpg
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

async def init_db():
    for _ in range(30):
        try:
            conn = await asyncpg.connect(DATABASE_URL)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS work_events (
                    id SERIAL PRIMARY KEY,
                    user_name TEXT NOT NULL,
                    action TEXT NOT NULL,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT NOW()
                );
            """)
            await conn.close()
            return
        except Exception:
            await asyncio.sleep(1)
    raise RuntimeError("DB connection failed after retries")

async def save_event(user_name: str, action: str, content: str):
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute(
        "INSERT INTO work_events(user_name, action, content) VALUES($1, $2, $3)",
        user_name, action, content
    )
    await conn.close()

async def fetch_events():
    conn = await asyncpg.connect(DATABASE_URL)
    rows = await conn.fetch("SELECT * FROM work_events ORDER BY created_at DESC")
    await conn.close()
    return [dict(row) for row in rows]
