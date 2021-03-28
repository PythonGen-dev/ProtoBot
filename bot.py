import asyncio
import datetime
import json
import socket
import time

import discord
from discord.ext import commands

from modules import storage
cogs = ["cogs.help", "cogs.wikifur", "cogs.anime", "cogs.fun", "cogs.utilities", "cogs.ping", "jishaku"]
host = socket.gethostname()
with open("config.json", "r") as configjson:
    configdata = json.load(configjson)
    if host[:7] == 'DESKTOP' or host[:3] == 'WIN':
        token = configdata["tokenbeta"]
        prefix = configdata["prefixbeta"]
        print('running beta')
    else:
        cogs.append("cogs.onCommandError")
        token = configdata["token"]
        prefix = configdata["prefix"]
    configjson.close()


class Bot(commands.Cog):
    def __init__(self, bot): self.bot = bot

    async def is_owner(self, user: discord.User):
        if user.id == 171718:  # Implement your own conditions here
            return True
        else:

        # Else fall back to the original
            return False


bot = commands.AutoShardedBot(prefix, case_insensitive=True, intents=discord.Intents.all())



def loadcogs():
    print(" ╔═╗ Loading cogs")
    for cog in cogs:
        try:
            bot.load_extension(cog), print(' ╟─> [SUCCESS] ' + cog)
        except:
            print(' ╟─> [FAILED] ' + cog)
    print(' ╚═╝ Load done')


@bot.event
async def on_member_join(member):
    if str(member.guild.id) == '803522604820070440':
        badges = storage("./database/badges.db")
        badgesdata = str(badges.get(str(member.id)))
        badgeslist = badgesdata.split("$")
        if "300" in badgeslist:
            print("")
        else:
            if str(badges.get(str(id))) == '0':
                badges.set(str(id), '300')
            else:
                data = badges.get(str(id))
                badges.set(str(id), data + "$" + '300')


@bot.event
async def on_ready():
    start_time = time.time()
    print(f"Launch successful.\r\nBot name: {bot.user}")
    await bot.change_presence(status=discord.Status.online)
    while True:
        await bot.change_presence(activity=discord.Game("with you"))
        await asyncio.sleep(15)
        await bot.change_presence(activity=discord.Game('bot prefix is: "{}"'.format(prefix)))
        await asyncio.sleep(15)
        user_list = []
        for guild in bot.guilds:
            for member in guild.members:
                user_list.append(member)
        await bot.change_presence(activity=discord.Game('with {} users'.format(len(user_list))))
        await asyncio.sleep(15)
        await bot.change_presence(activity=discord.Game('with {} servers'.format(len(list(bot.guilds)))))
        await asyncio.sleep(15)
        current_time = time.time()
        difference = int(round(current_time - start_time))
        await bot.change_presence(
            activity=discord.Game('uptime {}'.format(str(datetime.timedelta(seconds=difference)))))
        await asyncio.sleep(15)


loadcogs()
bot.run(token)
