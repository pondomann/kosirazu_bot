# Kosirazu Bot
### (Discord TTS Bot)

Discordのボイスチャンネルでテキストを読み上げるBotです。
COEIROINKを使用しています。

---

## ■ Features

* テキスト読み上げ（発言者がわかるよう、名前も読み上げます）
* メンバーの入退室通知
* 話し方（感情）変更（/set_style）
* キュー再生

---

## ■ Setup

Discord Developer Portal でBotを作成：
　必要な権限を設定します。管理者を付与すれば不足なく動作します。
　利用したいサーバーにBotを導入してください。

```bash
git clone <repo-url>
cd <repo-name>
python -m venv venv
python -m pip install -r requirements.txt
```

`.env` を作成：

```
DISCORD_TOKEN=your_token
# Discord Developer Portal で取得したもの
```

COEIROINKを起動してから実行：

```bash
python main.py
```

---

## ■ Commands

* /join
* /leave
* /set_style

---

## ■ Notes

* ローカルでCOEIROINKが必要です
* 現在は単一ギルド想定です
