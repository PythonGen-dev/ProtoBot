from discord.ext import commands
import json, socket, asyncio, time, discord, datetime, aiohttp, itertools
import utils.aiopg as aiopg

heart_anim=itertools.cycle(["♥️", "🧡", "💛", "💚", "💙", "💜"])
clock_anim=itertools.cycle(['🕐','🕑','🕒','🕓','🕔','🕕','🕖','🕗','🕘','🕙','🕚','🕛'])

with open("config.json", "r") as configjson:
    configdata = json.load(configjson)
    host = socket.gethostname()
    if host[:7] == 'DESKTOP' or host[:3] == 'WIN': prefix = configdata["prefixbeta"]
    else:prefix = configdata["prefix"]
    configjson.close()

def getallmembers(self):
    user_list = list()
    for guild in self.bot.guilds:
        for member in guild.members:
            user_list.append(member)
    return len(user_list)

class bot_event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        start_time = time.time()
        print('Ready!')
        print('Logged in as:', self.bot.user)
        print('ID:', self.bot.user.id)
        print("Cogs:")
        for cog in self.bot.cogs: print(cog)
        while True:
            messages = [
            f"uptime {datetime.timedelta(seconds=int(round(time.time()-start_time)))} {next(clock_anim)}",
            f"with you {next(heart_anim)}",
            f"global bot prefix is: '{prefix}'",
            "#BringBackBlurple!",
            f"with {getallmembers(self)} users 😃",
            f"with {len(self.bot.guilds)} servers 😘",
            "Discord: Now 10% uglier.",

            ]
            for msg in messages:
                await self.bot.change_presence(activity=discord.Game(msg))
                await asyncio.sleep(60/len(messages))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        region = str(guild.region)
        if region != "russia":
            await aiopg.aioupsertrow("langs", [["value", "'EN'"],["guildid", guild.id]], [["guildid", guild.id]])


def setup(bot):
    bot.add_cog(bot_event(bot))