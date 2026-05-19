# Kosirazu Bot

Discordのボイスチャンネルでテキストを読み上げるBotのコードです。  
ローカルで起動したCOEIROINKのAPIと  
MYCOEIROINKトークモデル「コシラズ」を利用して音声合成します。

---

## ■ Features

* テキスト読み上げ（連続の投稿でない場合、発言者名も読み上げます）
* メンバーの入退室通知
* 話し方の変更（/set_style）
* キュー再生

---

## ■ Requirements
- Python 3.11

---

## ■ Setup

* Discord Developer Portal でBotを作成します。  
必要な権限（管理者とすれば不足はありません）を付与し、  
利用したいサーバーにBotを導入してください。

* COEIROINKと、MYCOEのコシラズをインストールします。  
（コシラズ以外の音声ライブラリを利用する場合はconfig.pyを編集してください。）

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

## ■ License

このプロジェクトのコードは MIT License のもとで公開されています。  

なお、本リポジトリには、COEIROINK本体および音声ライブラリは含まれていません。  
COEIROINK 本体および各音声ライブラリには、それぞれ個別の利用規約・ライセンスが適用されます。  
ご利用の際は、各配布元の規約をご確認ください。  

COEIROINK利用規約  
https://coeiroink.com/terms  

COEIROINK:コシラズ

---

## ■ Notes

* 現在は単一ギルド想定です
* Windows + VSCodeで動作確認
