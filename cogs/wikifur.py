from random import randint

import discord
from discord.ext import commands

import modules

translates = modules.storage("./locals/langs.lang")
langsdb = modules.storage("./database/langsdb.db")

def getlang(ctx):
    try:
        guildlang = langsdb.get(str(ctx.guild.id))
        if guildlang == '0': guildlang = 'EN'
    except:
        guildlang = 'EN'
    return guildlang

class WikifurCog(commands.Cog, name="wikifur command"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="wikifur_search")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def wikifur_search(self, ctx, *, arg):
        guildlang = getlang(ctx=ctx)
        try:

            wikifurcontent = modules.wikifursearch(arg, results=10, suggestion=False)
            if not wikifurcontent:
                wikifurcontent = translates.get('none'+guildlang) + arg
                embed = discord.Embed(title=translates.get('wikiFsearchresults'+guildlang), color=0xe74c3c, description=wikifurcontent)
                embed.set_thumbnail(url='https://i.imgur.com/yitOWpO.png')
                embed.set_footer(icon_url='https://i.imgur.com/yitOWpO.png', text='wikifur command')
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title=translates.get('wikiFsearchresults'+guildlang), color=discord.Colour.from_rgb(67, 69, 156),
                                      description="\n".join(wikifurcontent))
                embed.set_thumbnail(url='https://i.imgur.com/yitOWpO.png')
                embed.set_footer(icon_url='https://i.imgur.com/yitOWpO.png', text='wikifur command')
                await ctx.send(embed=embed)
        except:
            await ctx.send()

    @commands.command(name="wikifur_display")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def wikifur_display(self, ctx, *, arg):
        guildlang = getlang(ctx=ctx)
        try:
            wikifurpage = modules.wikifurpage(arg)
            pagetext = modules.wikifursummary(arg, sentences=5)
            embed = discord.Embed(title=arg.capitalize(), color=discord.Colour.from_rgb(67, 69, 156),
                                  description=pagetext + "\n\n" + translates.get('readFurther'+guildlang) + "({})".format(wikifurpage.url))
            embed.set_footer(icon_url='https://i.imgur.com/yitOWpO.png', text='wikifur commmand')
            try:
                thumbnail = wikifurpage.images[randint(0, len(wikifurpage.images))]
                embed.set_image(url=thumbnail)
            except:
                embed.set_thumbnail(url='https://i.imgur.com/yitOWpO.png')
            embed.set_footer(icon_url='https://i.imgur.com/yitOWpO.png', text='wikifur command')
            await ctx.send(embed=embed)
        except modules.DisambiguationError:
            await ctx.send(embed=discord.Embed(title=translates.get('badarg'+guildlang), color=0xe74c3c,
                                               description=translates.get("NotSpecificargErrorMessage"+guildlang)).set_footer(
                icon_url='https://i.imgur.com/yitOWpO.png', text='wikifur command'))
        except modules.PageError:
            await ctx.send(
                embed=discord.Embed(title=translates.get('notFound'+guildlang), color=0xe74c3c, description=translates.get("NoResultErrorMessage"+guildlang)).set_footer(
                    icon_url='https://i.imgur.com/yitOWpO.png', text='wikifur command'))
        except:
            await ctx.send(
                embed=discord.Embed(title=translates.get('error'+guildlang), color=0xe74c3c, description=translates.get("RandomErrorMessage"+guildlang)).set_footer(
                    icon_url='https://i.imgur.com/yitOWpO.png', text='wikifur command'))


def setup(bot):
    bot.add_cog(WikifurCog(bot))
