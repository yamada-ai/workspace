import os
import asyncio
import logging
import httpx

from dotenv import load_dotenv
from twitchio.ext import commands
from twitchAPI.twitch import Twitch
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.helper import first
from twitchAPI.type import AuthScope

from components.basic import Basic  # あなたの Basic コンポーネント

# ─── 環境変数ロード ───────────────────────────────────────
load_dotenv()
APP_ID         = os.getenv("CLIENT_ID")
APP_SECRET     = os.getenv("CLIENT_SECRET")
USER_TOKEN     = os.getenv("ACCESS_TOKEN")
REFRESH_TOKEN  = os.getenv("REFRESH_TOKEN")
BOT_ID         = os.getenv("BOT_ID")
CHANNELS       = os.getenv("CHANNELS", "").split(",")
WORK_TRACKER   = os.getenv("WORK_TRACKER_URL")

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

# ─── Bot 定義 ────────────────────────────────────────────
class Bot(commands.Bot):
    def __init__(self, twitch: Twitch, eventsub: EventSubWebsocket):
        super().__init__(
            token=USER_TOKEN,
            prefix="!",
            client_id=APP_ID,
            client_secret=APP_SECRET,
            bot_id=BOT_ID,
        )
        self.twitch = twitch
        self.eventsub = eventsub
        self.tracker = httpx.AsyncClient(
            headers={"Authorization": f"Bearer {USER_TOKEN}"}, timeout=10.0
        )

    async def setup_hook(self):
        # コンポーネント登録
        await self.add_component(Basic(self))

        # EventSub WebSocket 接続スタート
        self.eventsub.start()

        log = logging.getLogger("twitch-bot")
        # チャネルごとにサブスクライブ
        for ch in CHANNELS:
            user = await first(self.twitch.get_users(logins=[ch]))
            if not user:
                continue
            broadcaster_id = user.id

            # ← ここを chat_notification から chat_message に変更
            await self.eventsub.listen_channel_chat_message(
                broadcaster_id,  # 配信者
                BOT_ID,          # BOT のユーザー ID
                self.on_chat_event
            )
            logging.getLogger("twitch-bot").info(
                "Subscribed to chat messages for %s", ch
            )
            
    async def on_chat_event(self, data):
        # 受信したチャットを POST
        await self.tracker.post(WORK_TRACKER, json={
            "user_name": data.event.user_name,
            "action":    "chat",
            "content":   data.event.message
        })

async def main():
    # 1) Twitch クライアントを生成 (App Access Token 自動取得) :contentReference[oaicite:0]{index=0}
    twitch = await Twitch(APP_ID, APP_SECRET)

    # 2) User Access Token をセット (User API 呼び出し用) :contentReference[oaicite:1]{index=1}
    await twitch.set_user_authentication(
        USER_TOKEN,
        [AuthScope.USER_READ_CHAT],
        REFRESH_TOKEN
    )

    # 3) EventSubWebsocket インスタンス生成
    eventsub = EventSubWebsocket(twitch)

    # 4) Bot を起動
    bot = Bot(twitch, eventsub)
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())
