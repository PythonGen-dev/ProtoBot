from discord.ext import commands
import discord, datetime, asyncio 
from utils.modules import aiogetlang, translations
blocklist_servers = list()
blocklist_users = list()
ban_config={"user_limit": 30, "guild_limit": 200} 

class cmd_cache(object):
    def __init__(self):
        self._cache = {"guilds":{}, "users":{}}
    def invoke(self, message):
        if message.guild.id not in self._cache["guilds"]:
            self._cache["guilds"][message.guild.id]=1
        else:
            self._cache["guilds"][message.guild.id]+=1
            if self._cache["guilds"][message.guild.id] >= ban_config["guild_limit"] and message.guild not in blocklist_servers:
                blocklist_servers.append(message.guild)
                print(f"Everyone from {message.guild} welcome to the blacklist :tada:")
        if message.author.id not in self._cache["users"]:
            self._cache["users"][message.author.id]=1
        else:
            self._cache["users"][message.author.id]+=1
            if self._cache["users"][message.author.id] >= ban_config["user_limit"] and message.author not in blocklist_users:
                blocklist_users.append(message.author)
                print(f"{message.author} welcome to the blacklist :tada:")
    def clear_cache(self):
        self._cache = {"guilds":{}, "users":{}}

async def use_cache(bot, message, cache):
    context = await bot.get_context(message)
    if context.command is not None: cache.invoke(message)

class commands_handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pizdabol_cache = cmd_cache()
        
    @commands.Cog.listener()
    async def on_ready(self):
        global blocklist_servers
        global blocklist_users
        while True:
            for none in range(15):
                await asyncio.sleep(60)
                self.pizdabol_cache.clear_cache()
            if blocklist_servers != list():
                print ("This servers removed from blacklist:", ", ".join([f"{i}" for i in blocklist_servers]))
                blocklist_servers = list()
            if blocklist_users != list():
                print ("This users removed from blacklist:", ", ".join([f"{i}" for i in blocklist_users]))
                blocklist_users = list()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author not in blocklist_users and message.guild not in blocklist_servers:
            await self.bot.process_commands(message)
            await use_cache(self.bot, message, self.pizdabol_cache)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author not in blocklist_users and after.guild not in blocklist_servers:
            timespent =(datetime.datetime.utcnow()-before.created_at).total_seconds()
            if timespent < 60:
                await use_cache(self.bot, after, self.pizdabol_cache)
                await self.bot.process_commands(after)

def setup(bot):
    bot.add_cog(commands_handler(bot))
