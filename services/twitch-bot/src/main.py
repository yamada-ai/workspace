import os, logging
import httpx
from twitchio.ext import commands
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

WORK_TRACKER_URL = os.environ["WORK_TRACKER_URL"]

def refresh_access_token():
    url = "https://id.twitch.tv/oauth2/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": os.environ["REFRESH_TOKEN"],
        "client_id": os.environ["CLIENT_ID"],
        "client_secret": os.environ["CLIENT_SECRET"]
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = httpx.post(url, data=data, headers=headers)
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        refresh_token = token_data["refresh_token"]
        logging.info("Access token refreshed")

        # 更新（環境変数だけ書き換える。ファイルは書き換えない）
        os.environ["ACCESS_TOKEN"] = access_token
        os.environ["REFRESH_TOKEN"] = refresh_token
        return access_token
    else:
        raise Exception(f"Failed to refresh token: {response.text}")

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=os.environ["ACCESS_TOKEN"],
            prefix="!",
            initial_channels=os.environ["CHANNELS"].split(",")
        )
        self.http = httpx.AsyncClient(timeout=5.0)

    async def event_ready(self):
        logging.info(f"Connected as {self.nick}")

    async def event_message(self, message):
        if message.echo:
            return

        logging.info(f"{message.author.name}: {message.content}")
        payload = {
            "user_name": message.author.name,
            "action": "chat",
            "content": message.content
        }

        try:
            r = await self.http.post(WORK_TRACKER_URL, json=payload)
            r.raise_for_status()
        except Exception as e:
            logging.error("Tracker POST failed: %s", e)

        if "こんにちは" in message.content:
            await message.channel.send(f"{message.author.name}さん、こんにちは！")
        await self.handle_commands(message)

    async def event_error(self, error, data=None):
        if "401 Unauthorized" in str(error):
            try:
                new_token = refresh_access_token()
                self._http.token = new_token  # BotのHTTPトークン更新
                logging.info("Retrying after token refresh...")
                self.run()
            except Exception as e:
                logging.error("Token refresh failed: %s", e)

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send("pong")

if __name__ == "__main__":
    try:
        Bot().run()
    except Exception as e:
        if "401" in str(e):
            new_token = refresh_access_token()
            os.environ["ACCESS_TOKEN"] = new_token
            Bot().run()
        else:
            raise
