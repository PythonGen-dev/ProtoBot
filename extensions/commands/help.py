import json
import random
import discord
from discord.ext import commands

from utils.modules import aiogetlang, getcustomemote, translations

class HelpCog(commands.Cog, name="help command"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', aliases=['хелп'])
    async def help(self, ctx, arg = None):
        guildlang = await aiogetlang(ctx)
        commands = list()
        for command in self.bot.commands:
            if str(command) not in ["eval", "help", "jishaku"]: commands.append(command.name) # remove dev commands'
        if arg is None:
            anime = list(); utilities = list(); nsfw = list(); others = list(); fun = list()
            for command in commands:
                # anime
                if command in ["quote", "hug", "wink", "pat", "sad", "facepalm"]: anime.append(str(command))
                # utilities
                elif command in ["avatar", "idinfo", "roles-list", "emojis-list","aboutme", "about", "getemoji", "guildinfo", "userinfo", "boop", "setlang", "PyPI", "topcord", "discordbots", "boticord"]: utilities.append(str(command))
                #nsfw
                elif command in ["rule34", "E621", "gelbooru", "neko", "yiff", "porngif"]: nsfw.append(str(command))
                # fun
                elif command in ["minecraft", "card", "owoify", "ttt", "ascii", "meme", "twitch", "lyrics", "image", "pixelate", "wikifur_search", "wikifur_display"]: fun.append(str(command))
                # others
                else: others.append(str(command))
            embed=discord.Embed(title=getcustomemote(self, '?', ctx)+translations(guildlang, 'helpembedtitle'), description=translations(guildlang, 'allbotcommands'), color=0xffffff)
            embed.add_field(name=translations(guildlang, 'botprefix'), value=f"`{await self.bot.command_prefix(self.bot, ctx.message)}`", inline=True)
            embed.add_field(name=translations(guildlang, 'additionalcommandinfo'), value=f"`!=help {random.choice(commands)}`", inline=True)
            if anime != []: embed.add_field(name=getcustomemote(self, 'anime', ctx)+f"{translations(guildlang, 'animeMenu')}({len(anime)}):", value=", ".join(anime), inline=False)
            if utilities != []: embed.add_field(name=getcustomemote(self, 'mod', ctx)+f"{translations(guildlang, 'utilitiesMenu')}({len(utilities)}):", value=", ".join(utilities), inline=False)
            if fun != []: embed.add_field(name=getcustomemote(self, 'fun', ctx)+f"{translations(guildlang, 'funMenu')}({len(fun)}):", value=", ".join(fun), inline=False)
            if nsfw != []: embed.add_field(name=getcustomemote(self, 'nsfw', ctx)+f"NSFW({len(nsfw)}):", value=", ".join(nsfw), inline=False)
            embed.set_footer(text=f"{translations(guildlang, 'botcommandscount')} {len(commands)}")
            if others != []: embed.add_field(name=getcustomemote(self, 'test', ctx)+f"{translations(guildlang, 'othersMenu')}({len(others)}):", value=", ".join(others), inline=False)
            await ctx.reply(embed=embed, mention_author=False)

        else:
            if str(arg) not in commands:
                await ctx.reply(translations(guildlang, 'invalidbotcommand'))
            else:
                embed=discord.Embed(title=getcustomemote(self, '?', ctx)+translations(guildlang, 'helpembedtitle'), description=translations(guildlang, 'commandname')+str(arg), color=0xffffff)
                embed.add_field(name=translations(guildlang, 'description'), value=translations(guildlang, str(arg) + "_help_desc"), inline=True)
                await ctx.reply(embed = embed, mention_author=False)

def setup(bot):
    bot.remove_command("help")
    bot.add_cog(HelpCog(bot))
