from discord.ext import commands
import discord, datetime
class commands_handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        timespent = (datetime.datetime.utcnow()-before.created_at).total_seconds()
        if timespent < 60:
            await self.bot.process_commands(after)

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.bot.process_commands(message)

def setup(bot):
    bot.add_cog(commands_handler(bot))
