import discord
from discord.ext import commands
import json
from modules import storage

prefix = json.load(open("config.json", "r"))["prefix"]
translates = storage("./locals/langs.lang")
langsdb = storage("./database/langsdb.db")
emotes = storage("./locals/emotes.lang")


def getlang(ctx):
    try:
        guildlang = langsdb.get(str(ctx.guild.id))
        if guildlang == '0': guildlang = 'EN'
    except:
        guildlang = 'EN'
    return guildlang


class HelpCog(commands.Cog, name="help command"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def help(self, ctx, page=1):
        guildlang = getlang(ctx=ctx)
        pages = 2
        embed = discord.Embed(title='Help', description='**{}** '.format(translates.get('prefix' + guildlang)) + str(prefix))
        if page >= pages: page = pages
        if page == 1:
            embed = embed.add_field(name=emotes.get('fun')+' {}:'.format(translates.get('funMenu' + guildlang)), value='> {0}ASCII - {1}\r\n> {0}image - {2}\r\n> {0}headsandtails - {3}\r\n> {0}lyrics - {4}\r\n> {0}meme - {5}\r\n> {0}minecraft - {6}'.format(
                                        prefix, translates.get('othersAscii' + guildlang), translates.get('othersImage' + guildlang), translates.get('othersheadsandtails' + guildlang), translates.get('othersLyrics' + guildlang), translates.get('othersMeme' + guildlang), translates.get('othersMinecraft' + guildlang)), inline=False)
            embed = embed.add_field(name=emotes.get('paw')+' {}:'.format(translates.get('wikifurMenu' + guildlang)),
                                    value='> {0}wikifur_search - {1}\r\n> {0}wikifur_display - {2}'.format(
                                        prefix, translates.get('wikifurSearchInfo' + guildlang), translates.get('wikifurDisplayInfo' + guildlang)), inline=False)
        elif page == 2:
            embed = embed.add_field(name=emotes.get('mod')+' {}:'.format(translates.get('settingsMenu' + guildlang)),
                                    value='> `{0}avatar` - {1}\r\n> `{0}userinfo` - {2}\r\n> `{0}guildinfo` - {3}\r\n> `{0}setlang <ru/en>` - {4}\r\n> `{0}about` - {5}\r\n> `{0}aboutme` - {6}'.format(
                                        prefix, translates.get('avatarhelp' + guildlang), translates.get('userinfohelp' + guildlang), translates.get('guildinfohelp' + guildlang), translates.get('setlang' + guildlang), translates.get('aboutcommand' + guildlang), translates.get('aboutmehelpdesc' + guildlang)), inline=False)
            embed = embed.add_field(name=emotes.get('senko')+' {}:'.format(translates.get('animeMenu' + guildlang)),
                                    value='> `{0}hug` - {1}\r\n> `{0}sad` - {2}\r\n> `{0}facepalm` - {3}\r\n> `{0}wink` - {4}\r\n> `{0}pat` - {5}\r\n> `{0}quote` - {6}'.format(
                                        prefix, translates.get('animehug' + guildlang), translates.get('animesad' + guildlang), translates.get('animefacepalm' + guildlang), translates.get('animewink' + guildlang), translates.get('animepet' + guildlang), translates.get('animequote' + guildlang)), inline=False)
        await ctx.send(embed=embed.set_footer(text='{0}: {1}/{2}'.format(translates.get('helppage'+guildlang), page, pages)))


def setup(bot):
    bot.remove_command("help")
    bot.add_cog(HelpCog(bot))
