import time

from discord.ext import commands


class PingCog(commands.Cog, name="ping command"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="boop")
    async def boop(self, ctx):
        before = time.monotonic()
        message = await ctx.send("OwO")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"UwU \r\n `{int(ping)} ms`")


def setup(bot):
    bot.add_cog(PingCog(bot))
