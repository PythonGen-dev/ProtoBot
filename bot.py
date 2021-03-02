import asyncio
import discord
import json
from discord.ext import commands

with open("config.json", "r") as configjson:
    configdata = json.load(configjson)
    token = configdata["token"]
    prefix = configdata["prefix"]
    configjson.close()


class Bot(commands.Cog):
    def __init__(self, bot): self.bot = bot


bot = commands.AutoShardedBot(prefix, case_insensitive=True, intents=discord.Intents.all())
cogs = ["cogs.help", "cogs.wikifur", "cogs.anime", "cogs.fun", "cogs.utilities", "cogs.ping"]


def loadcogs():
    print(" ╔═╗ Loading cogs ")
    for cog in cogs:
        bot.load_extension(cog), print(' ╟─> [SUCCES] ' + cog)
    print(' ╚═╝ Load done   ')


@bot.event
async def on_ready():
    print(f"Launch successful.\r\nBot name: {bot.user}")
    while True:
        await bot.change_presence(status=discord.Status.online, activity=discord.Game("with you"))
        await asyncio.sleep(15)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game("bot prefix is: " + prefix))
        await asyncio.sleep(15)



loadcogs()
bot.run(token)

