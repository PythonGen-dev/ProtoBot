import discord
from discord.ext import commands

from modules import storage, getlang

translates = storage("./locals/langs.lang")


class OnCommandErrorCog(commands.Cog, name="on command error"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        guildlang = getlang(ctx=ctx)
        if isinstance(error, commands.errors.EmojiNotFound):
            embed = discord.Embed(title=translates.get("error" + guildlang),
                                  description=translates.get("notFound" + guildlang)[:-1])
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(OnCommandErrorCog(bot))
