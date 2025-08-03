import os, asyncio, logging, httpx
from twitchio.ext import commands
from dotenv import load_dotenv
from components.basic import Basic

load_dotenv()
TOKEN   = os.getenv("ACCESS_TOKEN")
CLIENT  = os.getenv("CLIENT_ID")
BOT_ID  = os.getenv("BOT_ID")
SECRET  = os.getenv("CLIENT_SECRET")
CHANNEL = os.getenv("CHANNELS", "").split(",")[0]
WORK_TRACKER = os.getenv("WORK_TRACKER_URL")

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=TOKEN,
            prefix="!",
            initial_channels=[CHANNEL],
            bot_id=BOT_ID,  
            client_id=CLIENT,
            client_secret=SECRET
        )
        self.tracker = httpx.AsyncClient(
            headers={"Authorization": f"Bearer {TOKEN}"}, timeout=10.0
        )

    async def setup_hook(self):
        # Basic コンポーネント（ping コマンド）を登録
        await self.add_component(Basic())

    async def event_ready(self):
        logging.info("Bot is ready")

    async def event_ready(self):
        logging.info("Bot is ready")

    async def event_channel_joined(self, channel):
        logging.info(f"[EVENT] Successfully joined channel: {channel.name}")

    async def event_channel_join_failure(self, channel_name: str):
        logging.error(f"[EVENT] Failed to join channel: {channel_name}")


    async def event_message(self, message):
        print(f"[DEBUG] message received from {message.author.name}: {message.content}")

        if message.echo:
            print("[DEBUG] echo message, ignoring")
            return
        await self.tracker.post(WORK_TRACKER, json={
            "user_name": message.author.name,
            "action":    "chat",
            "content":   message.content
        })
        await self.handle_commands(message)

if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    bot = Bot()
    bot.run()
