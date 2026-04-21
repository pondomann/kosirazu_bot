import discord
from discord.ext import commands
from discord import app_commands

class CommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_voice(self):
        return self.bot.get_cog("VoiceCog")
    

    # --------------------
    # VC参加
    # --------------------
    @app_commands.command(name="join")
    async def join(self, interaction: discord.Interaction):
        await interaction.response.defer()

        voice = self.get_voice()

        if not voice:
            await interaction.followup.send("VoiceCogがないよ")
            return

        if interaction.user.voice is None:
            await interaction.followup.send("ボイスチャンネルに入って！")
            return

        try:
            await voice.connect(
                interaction.user.voice.channel,
                interaction.channel.id
            )

            await interaction.followup.send("接続したよ！")

        except Exception as e:
            await interaction.followup.send(str(e))


    # --------------------
    # VC退出
    # --------------------
    @app_commands.command(name="leave")
    async def leave(self, interaction: discord.Interaction):
        voice = self.get_voice()

        if not voice:
            await interaction.response.send_message("VoiceCogがないよ")
            return

        try:
            await voice.disconnect()
            await interaction.response.send_message("またね")

        except Exception as e:
            await interaction.response.send_message(str(e))


    # --------------------
    # スタイル変更コマンド
    # --------------------
    @app_commands.command(name="set_style", description="声音がかわるよ")
    async def set_style(self, interaction: discord.Interaction, new_style: str):
        voice = self.get_voice()

        if not voice:
            await interaction.response.send_message("VoiceCogがないよ")
            return

        if new_style in voice.style_options:
            voice.set_style(voice.style_options[new_style])
            await interaction.response.send_message(f"{new_style}スタイルだね！")
        else:
            await interaction.response.send_message("そのスタイルしらない…")


    # --------------------
    # スタイル入力候補
    # --------------------
    @set_style.autocomplete("new_style")
    async def style_autocomplete(
        self, 
        interaction: discord.Interaction,
        current: str
        ):

        voice = self.get_voice()

        if not voice:
            return []

        return [
            app_commands.Choice(name=style, value=style)
            for style in voice.style_options.keys()
            if current in style
        ]
    


async def setup(bot):
    await bot.add_cog(CommandCog(bot))