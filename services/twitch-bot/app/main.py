import os
import asyncio
import logging
import httpx

from dotenv import load_dotenv
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.type import AuthScope

from app.commands.in_command import handle_in_command

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
log = logging.getLogger("bot")

CLIENT_ID       = os.environ["CLIENT_ID"]
CLIENT_SECRET   = os.environ["CLIENT_SECRET"]
USER_TOKEN      = os.environ["ACCESS_TOKEN"]
REFRESH_TOKEN   = os.environ.get("REFRESH_TOKEN")
BROADCASTER_LOGIN = os.environ["CHANNELS"]

SEND_CHAT_URL = "https://api.twitch.tv/helix/chat/messages"

async def send_chat(client: httpx.AsyncClient, broadcaster_id: str, sender_id: str, message: str, reply_to: str | None = None):
    body = {"broadcaster_id": broadcaster_id, "sender_id": sender_id, "message": message}
    if reply_to:
        body["reply_parent_message_id"] = reply_to
    r = await client.post(SEND_CHAT_URL, json=body)
    r.raise_for_status()  # 4xx/5xxなら例外
    return r.json()

async def main():
    # 1) Twitchクライアント起動 & User認可を適用
    twitch = await Twitch(CLIENT_ID, CLIENT_SECRET)
    await twitch.set_user_authentication(
        USER_TOKEN,
        [
            AuthScope.USER_READ_CHAT,   # 受信
            AuthScope.USER_WRITE_CHAT,  # 送信
            AuthScope.USER_BOT          # 送信要件の一つ
        ],
        REFRESH_TOKEN
    )

    # 2) ID解決：bot本人(me) と 配信者(broadcaster)
    me = await first(twitch.get_users())  # ← アクセストークンのユーザー
    if me is None:
        raise RuntimeError("get_users() でbotユーザーを取得できませんでした。")
    broadcaster = await first(twitch.get_users(logins=[BROADCASTER_LOGIN]))
    if broadcaster is None:
        raise RuntimeError(f"チャンネル {BROADCASTER_LOGIN} が見つかりません。")

    bot_user_id = me.id
    broadcaster_id = broadcaster.id
    log.info(f"me={me.display_name}({bot_user_id}) broadcaster={broadcaster.display_name}({broadcaster_id})")

    # 3) 返信用 HTTP クライアント
    http = httpx.AsyncClient(headers={
        "Client-Id": CLIENT_ID,
        "Authorization": f"Bearer {USER_TOKEN}",
        "Content-Type": "application/json"
    }, timeout=10.0)

    # 4) EventSub WebSocket
    es = EventSubWebsocket(twitch)
    es.start()

    # 5) チャットメッセージ購読を一件貼る（接続直後に貼るのがコツ）
    async def on_chat(ev):
        # ev.event.message.text など（pyTwitchAPIの型更新で名称が変わる可能性があるのでフォールバック）
        msg = getattr(ev.event.message, "text", None) or getattr(ev.event, "message", None)
        user_name = getattr(ev.event, "chatter_user_name", None) or getattr(ev.event, "user_name", None)
        message_id = getattr(ev.event, "message_id", None)
        log.info(f"[{broadcaster.display_name}] {user_name}: {msg}")

        if isinstance(msg, str) and msg.strip().lower() == "!ping":
            try:
                await send_chat(http, broadcaster_id, bot_user_id, "pong", reply_to=message_id)
            except httpx.HTTPStatusError as e:
                # 401/403 の場合はスコープ不足か bot/mod 条件未達（channel:bot 付与 or モデレーター化）
                log.exception(f"send_chat failed: {e.response.text}")
        
        if msg.startswith("!in"):
            await handle_in_command(user_name, msg)

    await es.listen_channel_chat_message(
        broadcaster_user_id=broadcaster_id,
        user_id=bot_user_id,              # ← “読むユーザー”はボット本人
        callback=on_chat
    )
    log.info("Subscribed to channel.chat.message")

    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        await es.stop()
        await http.aclose()
        await twitch.close()

if __name__ == "__main__":
    asyncio.run(main())
