from app.api.work_tracker_client import send_in_command

async def handle_in_command(user_name: str, content: str):
    """
    Twitchチャットから受け取った `/in` コマンドをパースして送信
    例:
        /in                → 作業名なし
        /in 資料作成       → work_name="資料作成"
        /in 勉強 90        → work_name="勉強", planned_minutes=90
    """
    parts = content.strip().split(maxsplit=2)
    work_name = None
    planned_minutes = 120  # デフォルト値

    if len(parts) >= 2:
        work_name = parts[1]
    if len(parts) == 3 and parts[2].isdigit():
        planned_minutes = int(parts[2])

    return await send_in_command(user_name, work_name, planned_minutes)
