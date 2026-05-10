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

## ■ Requirements
- Python 3.11

## ■ Setup

* Discord Developer Portal でBotを作成します。  
必要な権限（管理者とすれば不足はありません）を付与し、  
利用したいサーバーにBotを導入してください。

* COEIROINKと、MYCOEのコシラズをインストールします。  
（ローカルで起動する必要があるため）

```bash
git clone https://github.com/pondomann/kosirazu_bot.git
cd kosirazu_bot
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

* 現在は単一ギルド想定です
* Windows + VSCodeで動作確認