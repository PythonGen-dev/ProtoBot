import json

import discord
from discord.ext import commands

from modules import storage

prefix = json.load(open("config.json", "r"))["prefix"]
translates = storage("./locals/langs.lang")

emotes = storage("./locals/emotes.lang")


def getcustomemote(self, emote, ctx):
    user = ctx.guild.get_member(803522872814731264)
    perms = user.guild_permissions
    if perms.use_external_emojis:
        return emotes.get(emote)
    else:
        return ''


def getlang(ctx):
    langsdb = storage("./database/langsdb.db")

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
    async def help(self, ctx, page=1):
        guildlang = getlang(ctx=ctx)
        pages = 2
        embed = discord.Embed(title='Help',
                              description='**{}** '.format(translates.get('prefix' + guildlang)) + '`' + str(
                                  prefix) + '`')
        if page >= pages: page = pages
        if page == 1:
            embed = embed.add_field(name=getcustomemote(self=self, emote='fun', ctx=ctx) + ' {}:'.format(
                translates.get('funMenu' + guildlang)),
                                    value='> {0}ASCII - {1}\r\n> {0}image - {2}\r\n> {0}lyrics - {4}\r\n> {0}meme - {5}\r\n> {0}minecraft - {6}\r\n> {0}getemoji - {7}'.format(
                                        prefix, translates.get('othersAscii' + guildlang),
                                        translates.get('othersImage' + guildlang),
                                        translates.get('othersheadsandtails' + guildlang),
                                        translates.get('othersLyrics' + guildlang),
                                        translates.get('othersMeme' + guildlang),
                                        translates.get('othersMinecraft' + guildlang),
                                        translates.get('othershetemoji' + guildlang)), inline=False)
            embed = embed.add_field(name=getcustomemote(self=self, emote='paw', ctx=ctx) + ' {}:'.format(
                translates.get('wikifurMenu' + guildlang)),
                                    value='> {0}wikifur_search - {1}\r\n> {0}wikifur_display - {2}'.format(
                                        prefix, translates.get('wikifurSearchInfo' + guildlang),
                                        translates.get('wikifurDisplayInfo' + guildlang)), inline=False)
            embed = embed.add_field(name=getcustomemote(self=self, emote='nsfw', ctx=ctx) + ' {}:'.format('NSFW'),
                                    value='> {0}rule34 - {1}'.format(
                                        prefix, translates.get('rule34desc' + guildlang)), inline=False)
        elif page == 2:
            embed = embed.add_field(name=getcustomemote(self=self, emote='mod', ctx=ctx) + ' {}:'.format(
                translates.get('settingsMenu' + guildlang)),
                                    value='> `{0}avatar` - {1}\r\n> `{0}userinfo` - {2}\r\n> `{0}guildinfo` - {3}\r\n> `{0}setlang <ru/en>` - {4}\r\n> `{0}about` - {5}\r\n> `{0}aboutme` - {6}\r\n> `{0}boop` - {7}'.format(
                                        prefix, translates.get('avatarhelp' + guildlang),
                                        translates.get('userinfohelp' + guildlang),
                                        translates.get('guildinfohelp' + guildlang),
                                        translates.get('setlang' + guildlang),
                                        translates.get('aboutcommand' + guildlang),
                                        translates.get('aboutmehelpdesc' + guildlang),
                                        translates.get('boopdesc' + guildlang)), inline=False)
            embed = embed.add_field(name=getcustomemote(self=self, emote='senko', ctx=ctx) + ' {}:'.format(
                translates.get('animeMenu' + guildlang)),
                                    value='> `{0}hug` - {1}\r\n> `{0}sad` - {2}\r\n> `{0}facepalm` - {3}\r\n> `{0}wink` - {4}\r\n> `{0}pat` - {5}\r\n> `{0}quote` - {6}'.format(
                                        prefix, translates.get('animehug' + guildlang),
                                        translates.get('animesad' + guildlang),
                                        translates.get('animefacepalm' + guildlang),
                                        translates.get('animewink' + guildlang), translates.get('animepet' + guildlang),
                                        translates.get('animequote' + guildlang)), inline=False)

        await ctx.send(
            embed=embed.set_footer(text='{0}: {1}/{2}'.format(translates.get('helppage' + guildlang), page, pages)))


def setup(bot):
    bot.remove_command("help")
    bot.add_cog(HelpCog(bot))
