import discord
from discord.ext import commands
import yaml


from src.socketio_client import sio
from src.util import getLogger, prefix
from src.help import help


with open('data/token','r',encoding='utf-8')as f:
    TOKEN = f.read()
getLogger('discord',level='WARNING')
getLogger('sIO')
logger = getLogger('bot')
intents = discord.Intents.all()
intents.typing = False
bot = commands.Bot(
    command_prefix=prefix,
    intents=intents,
    help_command=help,
    )


@bot.event
async def on_ready():
    logger.info('login success')
    await bot.change_presence(activity=discord.Game('!help'))


bot.load_extension('src.extension')
sio.run()
bot.run(TOKEN)
