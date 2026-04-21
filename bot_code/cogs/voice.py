import discord
from discord.ext import commands
from collections import deque
import os
import uuid
import asyncio

import tts
import utils


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
AUDIO_DIR = os.path.join(ROOT_DIR, "audio")

os.makedirs(AUDIO_DIR, exist_ok=True)

class VoiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = deque()
        self.is_playing = False
        self.vc = None  # VoiceClient
        self.text_channel_id = None
        self.last_speaker = None
        self.style_id = 194063739

        self.style_options = {
            "通常": "194063739",
            "ふきげん": "194063741",
            "よろこび": "194063742",
            "いじわる": "194063744",
            "へろへろ": "194063745",
        }



    # --------------------
    # ボット入室時の手続き
    # --------------------
    async def connect(self, channel, text_channel_id):
        if self.vc and self.vc.is_connected():
            raise Exception("既に接続中")

        self.vc = await channel.connect()
        self.text_channel_id = text_channel_id

        self.queue.clear()
        self.is_playing = False
        self.last_speaker = None


    # --------------------
    # ボット退室時の手続き
    # --------------------
    async def disconnect(self):
        if not self.vc or not self.vc.is_connected():
            raise Exception("接続していない")

        await self.vc.disconnect()

        self.vc = None
        self.text_channel_id = None
        self.queue.clear()
        self.is_playing = False
        self.last_speaker = None



    # --------------------
    # メッセージ受信
    # --------------------
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if not self.vc or not self.vc.is_connected():
            return
        
        if message.channel.id != self.text_channel_id:
            return

        processed_message = utils.process_message(message.content)
        display_name = message.author.display_name

        if display_name == self.last_speaker:
            text_to_speak = processed_message
        else:
            text_to_speak = f"{display_name}: {processed_message}"

        await self.speak(text_to_speak)

        self.last_speaker = display_name


    # --------------------
    # メンバー入退室
    # --------------------
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        if not self.vc or not self.vc.is_connected():
            return

        display_name = member.display_name

        if before.channel is None and after.channel is not None:
            if after.channel == self.vc.channel:
                await self.speak(f"いまきたのは{display_name}だよ")

        elif before.channel is not None and after.channel is None:
            if before.channel == self.vc.channel:
                await self.speak(f"ばいばい{display_name}")

    # --------------------
    # 読み上げ
    # --------------------
    async def speak(self, text):
        if not self.vc:
            return

        audio_data = tts.talk(text, self.style_id)

        filename = f"{uuid.uuid4()}.wav"
        file_path = os.path.join(AUDIO_DIR, filename)

        with open(file_path, "wb") as f:
            if hasattr(audio_data, "read"):
                f.write(audio_data.read())
            else:
                f.write(audio_data)

        self.queue.append(file_path)

        if not self.is_playing:
            await self.play_next()

    # --------------------
    # 再生
    # --------------------
    async def play_next(self):
        if not self.queue:
            self.is_playing = False
            return

        self.is_playing = True
        path = self.queue.popleft()

        def after_play(e):
            if e:
                print(f"[PLAY ERROR] {e}")

            try:
                os.remove(path)
            except Exception as e:
                print(f"[DELETE ERROR] {e}")


            fut = asyncio.run_coroutine_threadsafe(
                self.play_next(),
                self.bot.loop
            )
            try:
                fut.result()
            except Exception as e:
                print(f"[NEXT ERROR] {e}")

        self.vc.play(
            discord.FFmpegPCMAudio(path),
            after=after_play
        )


    # --------------------
    # スタイル変更時
    # --------------------
    def set_style(self, style_id):
        self.style_id = style_id



async def setup(bot):
    cog = VoiceCog(bot)
    await bot.add_cog(cog)
