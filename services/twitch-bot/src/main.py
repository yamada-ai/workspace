import os
import logging
import asyncio

from dotenv import load_dotenv
import httpx
from twitchio.ext import commands
from twitchio.eventsub import ChatMessageSubscription
from twitchio.payloads import EventErrorPayload, TokenRefreshedPayload
from twitchio import InvalidTokenException

from components.basic import Basic

# ─── 設定読み込み ─────────────────────────────────────────────────────────────
load_dotenv()
CLIENT_ID        = os.getenv("CLIENT_ID")
CLIENT_SECRET    = os.getenv("CLIENT_SECRET")
BOT_ID           = os.getenv("BOT_ID")
ACCESS_TOKEN     = os.getenv("ACCESS_TOKEN")
REFRESH_TOKEN    = os.getenv("REFRESH_TOKEN")
CHANNELS         = os.getenv("CHANNELS", "").split(",")
WORK_TRACKER_URL = os.getenv("WORK_TRACKER_URL")

for var in ("CLIENT_ID","CLIENT_SECRET","BOT_ID","ACCESS_TOKEN","REFRESH_TOKEN","WORK_TRACKER_URL"):
    if not globals()[var]:
        raise RuntimeError(f"{var} が .env に設定されていません")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger("twitch-bot")

def save_tokens(access_token: str, refresh_token: str):
    with open("tokens.env", "w") as f:
        f.write(f"ACCESS_TOKEN={access_token}\n")
        f.write(f"REFRESH_TOKEN={refresh_token}\n")
    logger.info("トークンを tokens.env に保存しました")

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            bot_id=BOT_ID,
            prefix="!",
            initial_channels=CHANNELS
        )
        # Work Tracker API 用 HTTP クライアント
        self.tracker = httpx.AsyncClient(
            timeout=10.0,
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        )

    async def setup_hook(self):
        await self.add_component(Basic(self)) 
        # Bot 起動時に一度だけトークンを登録して自動リフレッシュ対応
        await self.add_token(ACCESS_TOKEN, refresh=REFRESH_TOKEN)

        for channel in CHANNELS:
            users = await self.fetch_users(logins=[channel])
            if not users:
                logger.warning("ユーザー情報が取得できませんでした: %s", channel)
                continue
            broadcaster = users[0]
            subscription = ChatMessageSubscription(
                broadcaster_user_id=broadcaster.id,
                user_id=BOT_ID
            )
            await self.subscribe_websocket(payload=subscription)   
        

    async def event_ready(self):
        # v3では self.user.name がBotの名前
        logger.info(f"Logged in as {self.user.name}")

    async def event_message(self, message):
        logging.info("Received message: %s", message.content)
        if message.echo:
            return

        user = message.author.name
        text = message.content
        logger.info(f"<{user}> {text}")

        # Work Tracker に送信
        try:
            resp = await self.tracker.post(
                WORK_TRACKER_URL,
                json={"user_name": user, "action": "chat", "content": text}
            )
            resp.raise_for_status()
        except Exception as e:
            logger.error("Tracker POST 失敗: %s", e)

        await self.handle_commands(message)

    async def event_token_refreshed(self, payload: TokenRefreshedPayload):
        """
        トークンが自動リフレッシュされたときに呼ばれる。
        payload.access_token, payload.refresh_token を永続化。
        """
        new_access  = payload.token
        new_refresh = payload.refresh_token 

        # HTTP クライアントのヘッダー更新
        self.tracker.headers.update({"Authorization": f"Bearer {new_access}"})

        # 新トークン登録（再リフレッシュ登録）
        await self.add_token(new_access, refresh=new_refresh)

        # 永続化
        save_tokens(new_access, new_refresh)

        logger.info("トークンを自動リフレッシュし、更新しました")

    async def event_error(self, payload: EventErrorPayload):
        """
        v3 の event_error では EventErrorPayload が渡される。
        payload.original に実際の例外オブジェクトが入っている。
        """
        exc = payload.original
        # トークン切れは自動リフレッシュで処理済みなので無視
        if isinstance(exc, InvalidTokenException):
            return
        
        listener = (
            payload.listener.__name__
            if hasattr(payload.listener, "__name__")
            else str(payload.listener)
        )
        logger.error("予期せぬエラー in %s: %s", listener, exc)

if __name__ == "__main__":
    try:
        bot = Bot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot を停止します")
