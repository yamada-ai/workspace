# WorkSpace 作業部屋プロトタイプ

## 概要

作業部屋システムのプロトタイプ開発環境
TwitchやDiscordのボットがユーザーのイベントを取得し、バックエンドに通信。
APIはDB(PostgreSQL)でデータ管理を行い、最終的にブラウザを介してOBSから配信

---

## 構成

```
workspace/
├── services/                 # バックエンドモジュール
│   ├── twitch-bot/          # Twitchチャット取得Bot
│   ├── discord-bot/         # Discord VCモニターBot
│   └── work-tracker/        # FastAPI端: Botのイベントを受けてDB管理
├── frontend/                # OBSに表示するWebUI
├── infra/                   # Docker設定やDBスクリプト
│   ├── docker-compose.yml
│   └── nginx.conf
└── README.md                # この説明
```

---

## 技術構成

| モジュール        | 技術要素                       | 用途 |
|----------------|----------------------------------|------|
| twitch-bot     | Python + TwitchIO + dotenv      | Twitch IRCメッセージの取得と投稿 |
| discord-bot    | Python + discord.py             | VC参加ユーザーのモニタリング |
| work-tracker   | Python + FastAPI + asyncpg      | BotのイベントをAPIで受けてDBへ |
| frontend       | HTML + JS (or React)            | OBSに表示するUI |
| nginx          |  nginx                          | リバースプロキシ + APIルーティング|
| db             | PostgreSQL                       | 全サービスのデータ保存 |

---

## 起動方法