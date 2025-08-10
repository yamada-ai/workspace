import os
import httpx
import logging

logger = logging.getLogger(__name__)

WORK_TRACKER_URL = os.getenv("WORK_TRACKER_URL")

async def send_in_command(user_name: str, work_name: str | None = None, planned_minutes: int = 120):
    """`/in` コマンドで作業セッションを作成する"""
    url = f"{WORK_TRACKER_URL}/sessions"
    payload = {
        "user_name": user_name,
        "work_name": work_name,
        "planned_minutes": planned_minutes
    }

    logger.info(f"POST {url} payload={payload}")

    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(url, json=payload)
            res.raise_for_status()
            logger.info(f"Session created: {res.json()}")
            return res.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"[IN失敗] {e.response.status_code} {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"[IN失敗] {e}")
            raise
