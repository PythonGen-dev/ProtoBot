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

        if isinstance(error, commands.errors.NSFWChannelRequired):
            await ctx.send(embed=discord.Embed(title=translates.get('error' + guildlang), description=translates.get('notNSFW' + guildlang)))

        if isinstance(error, commands.errors.CheckFailure):
            errdesc = str()
            if str(guildlang) == "RU": errdesc = "У вас нет прав на выполнение этой команды."
            else: errdesc = "You do not have permission to execute this command."
            await ctx.send(embed=discord.Embed(title=translates.get('error' + guildlang), description=errdesc)) 


def setup(bot):
    bot.add_cog(OnCommandErrorCog(bot))
