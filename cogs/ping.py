import discord
from discord.ext import commands
import time


class PingCog(commands.Cog, name="ping command"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping",
                      usage="",
                      description="Display the bot's ping.")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def ping(self, ctx):
        before = time.monotonic()
        message = await ctx.send("Please wait.")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Ping is `{int(ping)} ms`")


def setup(bot):
    bot.add_cog(PingCog(bot))
