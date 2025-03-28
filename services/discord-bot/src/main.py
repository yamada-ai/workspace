import os, logging, httpx
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

WORK_URL = os.getenv("WORK_TRACKER_URL")

intents = discord.Intents.default()
intents.message_content = True     # メッセージ読み取り
intents.voice_states = True        # VC 状態監視

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logging.info(f"Discord Bot logged in as {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    action = None
    if before.channel is None and after.channel:
        action = "vc_join"
    elif before.channel and after.channel is None:
        action = "vc_leave"
    if action:
        payload = {"user_name": member.name, "action": action, "content": after.channel.name if after.channel else ""}
        async with httpx.AsyncClient() as client:
            await client.post(WORK_URL, json=payload)
        logging.info(f"[VC] {member.name} {action}")

bot.run(os.getenv("DISCORD_TOKEN"))
