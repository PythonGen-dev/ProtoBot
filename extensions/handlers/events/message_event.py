from discord.ext import commands
import discord, aiohttp, json
import utils.aiopg as aiopg

blacklist = {
"guilds": [123456789, 101112],
"members":[123456789, 101112]
}

with open("config.json", "r") as configjson:
    configdata = json.load(configjson)
    globallogswebhook = configdata["logswebhook"]
    configjson.close()

class message_event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in blacklist["members"] or message.guild.id in blacklist["guilds"]:
            return
        else:
            if message.author == self.bot.user or message.author.bot == True: return
            try: xp = (await aiopg.aiogetrow("userxp", [["guildid", message.guild.id],["userid", message.author.id]]))[-1]
            except: xp = 0
            try:
                gainxp = len(message.content)
                if gainxp >= 100: gainxp = 100           
                await aiopg.aioupsertrow("userxp", [["value", xp + gainxp],["guildid", message.guild.id],["userid", message.author.id]], [["guildid", message.guild.id],["userid", message.author.id]])
            except: pass

def setup(bot):
    bot.add_cog(message_event(bot))