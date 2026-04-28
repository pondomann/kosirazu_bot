import discord
from discord.ext import commands
from collections import deque
import os
import uuid
import asyncio
import aiohttp

import tts
import utils
from config import DEFAULT_STYLE_ID


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
AUDIO_DIR = os.path.join(ROOT_DIR, "audio")

os.makedirs(AUDIO_DIR, exist_ok=True)


class VoiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.queue = deque()
        self.is_playing = False
        self.vc = None  # VoiceClient
        self.text_channel_id = None
        self.last_speaker = None
        self.style_id = DEFAULT_STYLE_ID
        self.semaphore = asyncio.Semaphore(2)


    # --------------------
    # ボット終了時の手続き
    # --------------------
    async def cog_unload(self):
        print("Session closing...")
        await self.session.close()


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

        await self.request_speech(text_to_speak)

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
                await self.request_speech(f"いまきたのは{display_name}だよ")

        elif before.channel is not None and after.channel is None:
            if before.channel == self.vc.channel:
                await self.request_speech(f"ばいばい{display_name}")


    # --------------------
    # 読み上げの入口
    # --------------------
    async def request_speech(self, text):
        if not self.vc:
            return
        
        if len(self.queue) >= 4:
            print("キュー上限")
            
            channel = self.bot.get_channel(self.text_channel_id)
            if channel:
                await channel.send("もう少し時間をおいてね")

            return

        asyncio.create_task(self._handle_tts_request(text))


    # --------------------
    # 読み上げ関数の制御
    # --------------------
    async def _handle_tts_request(self, text):
        audio_data = await self._generate_audio(text)

        if not audio_data:
            return

        self._enqueue_audio(audio_data)

        if not self.is_playing:
            await self.play_from_queue()


    # --------------------
    # TTS生成（読み上げ）
    # --------------------
    async def _generate_audio(self, text):
        async with self.semaphore:
            try:
                audio_data = await tts.talk(self.session, text, self.style_id)
                return audio_data

            except Exception as e:
                print(f"TTS error: {e}")
                return None


    # --------------------
    # キューに追加（読み上げ）
    # --------------------
    def _enqueue_audio(self, audio_data):
        filename = f"{uuid.uuid4()}.wav"
        file_path = os.path.join(AUDIO_DIR, filename)

        with open(file_path, "wb") as f:
            if hasattr(audio_data, "read"):
                f.write(audio_data.read())
            else:
                f.write(audio_data)

        self.queue.append(file_path)


    # --------------------
    # 再生（読み上げ）
    # --------------------
    async def play_from_queue(self):
        if not self.queue:
            self.is_playing = False
            return
        
        if not self.vc or not self.vc.is_connected():
            print("VC not connected (play_next)")
            self.is_playing = False
            return

        self.is_playing = True
        path = self.queue.popleft()

        def after_play(e):
            if e:
                print(f"[PLAY ERROR] {e}")
            else:
                print("再生完了")

            try:
                os.remove(path)
            except Exception as e:
                print(f"[DELETE ERROR] {e}")


            asyncio.run_coroutine_threadsafe(
                self.play_from_queue(),
                self.bot.loop
            )


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
