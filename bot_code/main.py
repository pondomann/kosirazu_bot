import discord  
from discord.ext import commands
from dotenv import load_dotenv
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True
intents.members = True

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
APP_ID = int(os.getenv("APPLICATION_ID"))

bot = commands.Bot(
    command_prefix="/",
    intents=intents,
    application_id=APP_ID
)


async def load_cogs():
    cogs = [
        "cogs.voice",
        "cogs.commands",
    ]

    for cog in cogs:
        await bot.load_extension(cog)


async def setup_hook():
    await load_cogs()
    await bot.tree.sync()


@bot.event
async def on_ready():
    print('オープン！')


bot.setup_hook = setup_hook

bot.run(TOKEN)