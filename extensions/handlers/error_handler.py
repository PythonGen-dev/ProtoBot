import discord
from discord.ext import commands
from utils.modules import aiogetlang, translations

class OnCommandErrorCog(commands.Cog, name="on command error"):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        guildlang = await aiogetlang(ctx)
        if isinstance(error, commands.CommandOnCooldown):
            if str(guildlang) == "RU": await ctx.send('Эта команда под кулдауном, повторите попытку через {:.2f} секунд'.format(error.retry_after))
            else: await ctx.send('This command is ratelimited, please try again in {:.2f}s'.format(error.retry_after))
        if isinstance(error, commands.errors.EmojiNotFound):
            embed = discord.Embed(title=translations (guildlang, "error"), description=translations (guildlang, "notFound")[:-1])
            await ctx.reply(embed=embed)
        if isinstance(error, commands.errors.NSFWChannelRequired):
            await ctx.reply(embed=discord.Embed(title=translations (guildlang, 'error'), description=translations (guildlang, 'notNSFW')))
        elif isinstance(error, commands.errors.CheckFailure):
            if str(error.args[0]) == "no_premium":
                await ctx.reply("You don't have a premium!")
            else:
                if str(guildlang) == "RU": errdesc = "У вас нет прав на выполнение этой команды."
                else: errdesc = "You do not have permission to execute this command."
                await ctx.send(embed=discord.Embed(title=translations (guildlang, 'error'), description=errdesc)) 

def setup(bot):
    bot.add_cog(OnCommandErrorCog(bot))
