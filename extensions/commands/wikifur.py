from random import randint

import discord
from discord.ext import commands

from utils.modules import aiogetlang, translations
import utils.modules as modules

class WikifurCog(commands.Cog, name="wikifur command"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="wikifur_search")
    async def wikifur_search(self, ctx, *, arg=None):
        guildlang = await aiogetlang(ctx)
        if arg is None:
            await ctx.send(embed=discord.Embed(title=translations(guildlang, 'ErrNotArg'),
                                               color=discord.Colour.from_rgb(67, 69, 156)))
        else:
            try:
                wikifurcontent = modules.wikifursearch(arg, results=10, suggestion=False)
                if not wikifurcontent:
                    wikifurcontent = translations(guildlang, 'none') + arg
                    embed = discord.Embed(title=translations(guildlang, 'wikiFsearchresults'), color=0xe74c3c,
                                          description=wikifurcontent)
                    embed.set_thumbnail(url='https://i.imgur.com/yitOWpO.png')
                    embed.set_footer(icon_url='https://i.imgur.com/yitOWpO.png', text='wikifur command')
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title=translations(guildlang, 'wikiFsearchresults'),
                                          color=discord.Colour.from_rgb(67, 69, 156),
                                          description="\n".join(wikifurcontent))
                    embed.set_thumbnail(url='https://i.imgur.com/yitOWpO.png')
                    embed.set_footer(icon_url='https://i.imgur.com/yitOWpO.png', text='wikifur command')
                    await ctx.send(embed=embed)
            except:
                await ctx.send()

    @commands.command(name="wikifur_display")
    async def wikifur_display(self, ctx, *, arg=None):
        guildlang = await aiogetlang(ctx)
        if arg is None:
            await ctx.send(embed=discord.Embed(title=translations(guildlang, 'ErrNotArg'),
                                               color=discord.Colour.from_rgb(67, 69, 156)))
        else:
            try:
                wikifurpage = modules.wikifurpage(arg)
                pagetext = modules.wikifursummary(arg, sentences=5)
                embed = discord.Embed(title=arg.capitalize(), color=discord.Colour.from_rgb(67, 69, 156),
                                      description=pagetext + "\n\n" + translations(guildlang, 
                                          'readFurther') + "({})".format(wikifurpage.url))
                embed.set_footer(icon_url='https://i.imgur.com/yitOWpO.png', text='wikifur commmand')
                try:
                    thumbnail = wikifurpage.images[randint(0, len(wikifurpage.images))]
                    embed.set_image(url=thumbnail)
                except:
                    embed.set_thumbnail(url='https://i.imgur.com/yitOWpO.png')
                embed.set_footer(icon_url='https://i.imgur.com/yitOWpO.png', text='wikifur command')
                await ctx.send(embed=embed)
            except modules.DisambiguationError:
                await ctx.send(embed=discord.Embed(title=translations(guildlang, 'badarg'), color=0xe74c3c,
                                                   description=translations(guildlang, 
                                                       "NotSpecificargErrorMessage")).set_footer(
                    icon_url='https://i.imgur.com/yitOWpO.png', text='wikifur command'))
            except modules.PageError:
                await ctx.send(
                    embed=discord.Embed(title=translations(guildlang, 'notFound'), color=0xe74c3c,
                                        description=translations(guildlang, "NoResultErrorMessage")).set_footer(
                        icon_url='https://i.imgur.com/yitOWpO.png', text='wikifur command'))
            except:
                await ctx.send(
                    embed=discord.Embed(title=translations(guildlang, 'error'), color=0xe74c3c,
                                        description=translations(guildlang, "RandomErrorMessage")).set_footer(
                        icon_url='https://i.imgur.com/yitOWpO.png', text='wikifur command'))


def setup(bot):
    bot.add_cog(WikifurCog(bot))
