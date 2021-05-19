import asyncio
import datetime
import utils.aiopg as aiopg
import json
import socket
import time
import os
import aiohttp
import discord
from discord.ext import commands
import logging
betamode = False 
extensions = [
#events
"extensions.handlers.events.bot_event",
"extensions.handlers.events.member_event",
"extensions.handlers.events.message_event",
#handlers
"extensions.handlers.commands_handler",
#"extensions.handlers.error_handler",
#commands
"extensions.commands.wikifur",
"extensions.commands.info",
"extensions.commands.anime",
"extensions.commands.fun",
"extensions.commands.help",
"extensions.commands.utilities",
"extensions.commands.ping",
"extensions.commands.canvas",
"extensions.commands.nsfw",
#others
"extensions.games.tictactoe",
"jishaku",
]

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

with open("config.json", "r") as configjson:
    host = socket.gethostname()
    configdata = json.load(configjson)
    if host[:7] == 'DESKTOP' or host[:3] == 'WIN' or betamode == True:
        token = configdata["tokenbeta"]
        prefix = configdata["prefixbeta"]
        print('Canary!!!')
    else:
        extensions.append("extensions.handlers.error_handler")
        token = configdata["token"]
        prefix = configdata["prefix"]
        print("Stable!!!")
    configjson.close()

async def get_prefix(bot, message):
    if betamode: return "!= "
    else:
        try:
            prefixget = (await aiopg.aiogetrow("prefix", [["guildid", message.guild.id]]))[-1]
        except:
            prefixget = prefix
        return prefixget
    
bot = commands.AutoShardedBot(command_prefix=get_prefix, case_insensitive=True, intents=discord.Intents.all())

def load_extensions():
    for cog in extensions:
        if betamode: bot.load_extension(cog)
        else:
            try: bot.load_extension(cog)
            except: pass

@bot.event
async def on_message(message): pass #block commands

load_extensions()
bot.run(token)
