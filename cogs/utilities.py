import discord
from discord.ext import commands
from modules import storage
import datetime
import json
import socket


translates = storage("./locals/langs.lang")
langsdb = storage("./database/langsdb.db")
emotes = storage("./locals/emotes.lang")
usersdesc = storage("./database/usersdesc.db")

def getlang(ctx):
    try:
        guildlang = langsdb.get(str(ctx.guild.id))
        if guildlang == '0': guildlang = 'EN'
    except:
        guildlang = 'EN'
    return guildlang

def filterbots(member):
    return member.bot


prefix = json.load(open("config.json", "r"))["prefix"]


def getmonth(date, lang):
    month = list(str(datetime.datetime.now() - date).split(",")[0].split(" "))
    if month[1] == 'days':
        rounded = str(round(int(month[0]) / 30))
        if rounded == '1':
            return rounded + ' ' + translates.get('monthlow' + lang)
        else:
            return rounded + ' ' + translates.get('monthsmore' + lang)
    else:
        return '0 ' + translates.get('monthsmore' + lang)


class UtilitiesCog(commands.Cog, name="Utilities Cog"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="guildinfo")
    async def guildinfo(self, ctx):
        guildlang = getlang(ctx=ctx)
        guildlang = getlang(ctx=ctx)
        text_channel_list = []
        voice_channel_list = []
        for channel in ctx.guild.text_channels:
            text_channel_list.append(channel)
        for channel in ctx.guild.voice_channels:
            voice_channel_list.append(channel)
        voice_channel_count = len(voice_channel_list)
        text_channel_count = len(text_channel_list)
        all_channel_count = text_channel_count + voice_channel_count
        membersinserver = ctx.guild.members
        botsinserver = list(filter(filterbots, membersinserver))
        botsinservercount = len(botsinserver)
        embed = discord.Embed(color=0xff9900,
                              title=ctx.guild.name + " " + translates.get("serverWord" + guildlang))
        embed.add_field(name=translates.get("usersNametag" + guildlang),
                        value="> **{0}** {1}\r\n > **{2}** {3}\r\n > **{4}** {5}".format(
                            emotes.get('allusers')+translates.get("allUsers" + guildlang), ctx.guild.member_count,
                            emotes.get('bot')+translates.get("botUsers" + guildlang), botsinservercount,
                            emotes.get('human')+translates.get("realUsers" + guildlang), ctx.guild.member_count - botsinservercount,
                            inline=True))

        embed.add_field(name=translates.get("Channels" + guildlang),
                        value="> **{0}** {1}\r\n > **{2}** {3}\r\n > **{4}** {5}".format(
                            emotes.get('AllChannels')+translates.get("allUsers" + guildlang), all_channel_count,
                            emotes.get('VoiceChannels')+translates.get("VoiceChannels" + guildlang), voice_channel_count,
                            emotes.get('TextChannels')+translates.get("TextChannels" + guildlang), text_channel_count), inline=True)
        voiceregion = str(ctx.guild.region)
        verificationlvl = str(ctx.guild.verification_level)
        servowner = await self.bot.fetch_user(ctx.guild.owner_id)
        embed.add_field(name=translates.get("serverInfoRegion" + guildlang),
                        value='> '+emotes.get(voiceregion)+translates.get(voiceregion + guildlang),
                        inline=True)
        embed.add_field(name=translates.get("serverInfoOwner" + guildlang),
                        value='> '+emotes.get('owner')+str(servowner), inline=True)
        embed.add_field(name=translates.get("VerificationLevel" + guildlang),
                        value='> '+emotes.get(verificationlvl)+translates.get(verificationlvl + guildlang),
                        inline=True)
        creationmonth = str(ctx.guild.created_at.strftime("%m"))
        creationdate = str(ctx.guild.created_at.strftime(
            "%d " + translates.get(creationmonth + "month" + guildlang) + " %Y" + translates.get(
                "year" + guildlang) + ", %H:%M:%S"))
        embed.add_field(name=translates.get("guildCreationDate" + guildlang), value='> '+str(creationdate), inline=True)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text="ID: " + str(ctx.guild.id))
        await ctx.send(embed=embed)

    @commands.command(name="setlang")
    @commands.has_permissions(administrator=True)
    async def setlang(self, ctx, arg=None):
        language = None
        if arg is None:
            await ctx.send(embed=discord.Embed(description='No arguments', title='Error')); return ()
        elif arg == "en":
            language = "EN"
        elif arg == "ru":
            language = "RU"
        if language is not None:
            langsdb.set(str(ctx.guild.id), language)
            await ctx.send(embed=discord.Embed(description='Language set to: ' + language, title='Successful'))
        else:
            await ctx.send(embed=discord.Embed(description='Invalid argument', title='Error'))

    @commands.command(name="userinfo")
    async def userinfo(self, ctx, userctx: discord.Member = None):
        guildlang = getlang(ctx=ctx)
        spotify = "0"
        member = ctx.author if not userctx else userctx
        if not member.bot:
            userid = member.id
            userinf = await self.bot.fetch_user(userid)
            embed = discord.Embed(color=0xff9900, title=translates.get("infoAbout" + guildlang) + ' ' + str(userinf))
            descvalue = usersdesc.get(str(ctx.author.id)+str(ctx.guild.id))
            if ctx.author.id == userid:
                if descvalue == '0': embed.add_field(name=translates.get('userdescriptiontitle'+guildlang), value=translates.get('userdescadd'+guildlang)+prefix+'aboutme`!', inline=False)
                else: embed.add_field(name=translates.get('userdescriptiontitle' + guildlang), value=descvalue, inline=False)
            else:
                if descvalue == '0': embed.add_field(name=translates.get('userdescriptiontitle'+guildlang), value=translates.get('userdontadddesc'+guildlang), inline=False)
                else: embed.add_field(name=translates.get('userdescriptiontitle'+guildlang), value=descvalue, inline=False)

            if str(member.activity)[:15] == "<Activity type=":
                customactivitystr = translates.get("userActivityNone" + guildlang)
            elif str(member.activity) == "Spotify":
                customactivitystr = translates.get("userActivityNone" + guildlang)
                spotify = "1"

            else:
                customactivitystr = str(member.activity)
            if spotify == "1":
                status = translates.get("userStatusSpotify" + guildlang) + ' ' + "Spotify"
            else:
                status = translates.get(str(member.status) + guildlang)
            usercreationdate = str(member.created_at.strftime("%d " + translates.get(
                str(member.created_at.strftime("%m")) + "month" + guildlang) + " %Y" + translates.get(
                "year" + guildlang) + ", %H:%M:%S"))
            userjoineddate = str(member.joined_at.strftime("%d " + translates.get(
                str(member.joined_at.strftime("%m")) + "month" + guildlang) + " %Y" + translates.get(
                "year" + guildlang) + ", %H:%M:%S"))
            if spotify == '1':
                activityemote = emotes.get('spotify')
            else: activityemote = emotes.get(str(member.status))
            embed.add_field(name=translates.get("basicInfo" + guildlang),
                            value='⬢** {0}**\r\n > {1}\r\n⬢** {2}**\r\n > {3} ({4})\r\n⬢** {5}**\r\n > {6} ({7})\r\n⬢** {8}**\r\n > {9}\r\n⬢** {10}**\r\n > {11}'.format(
                                translates.get("userInfoUsername" + guildlang), userinf,
                                translates.get("userinfoJoined" + guildlang), userjoineddate,
                                getmonth(date=member.joined_at, lang=guildlang),
                                translates.get("userinfoAccCreated" + guildlang), usercreationdate,
                                getmonth(date=member.created_at, lang=guildlang),
                                translates.get("userinfoStatus" + guildlang), activityemote + str(status),

                                translates.get("customactivity" + guildlang), customactivitystr), inline=False)
            embed.set_footer(text="ID: " + str(userid))
            embed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=0xff9900, title=translates.get("infoAboutBotErr" + ' ' + guildlang))
            await ctx.send(embed=embed)

    @commands.command(name="avatar")
    async def avatar(self, ctx, userctx: discord.Member = None):
        guildlang = getlang(ctx=ctx)
        member = ctx.author if not userctx else userctx
        userinf = await self.bot.fetch_user(member.id)
        embed = discord.Embed(color=0xff9900, title=translates.get("userAvatar" + guildlang) + str(userinf))
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="aboutme")
    async def aboutme(self, ctx, *, args):
        try:
            guildlang = langsdb.get(str(ctx.guild.id))
            if guildlang == "0": guildlang = "EN"
        except: guildlang = "EN"
        usersdesc.set(str(ctx.author.id)+str(ctx.guild.id), args[:256])
        embed = discord.Embed(title=translates.get('userdescriptionsetted'+guildlang), description=str(args[:256]))
        await ctx.send(embed=embed)

    @commands.command(name="about")
    async def about(self, ctx):
        global prefix
        host = socket.gethostname()
        print(str(host))
        if host[:7] == 'DESKTOP':
            host = emotes.get('desktop')+host
        else: host = emotes.get('hosticon')+'Heroku'
        guildlang = getlang(ctx=ctx)
        servers = list(self.bot.guilds)
        embed = discord.Embed(color=0xff9900, title=self.bot.user.name +' '+ translates.get('bot' + guildlang),
                              description=translates.get('aboutdesc' + guildlang) + '\r\n\r\n' + translates.get(
                                  'helplistend' + guildlang).replace('!=', str(prefix)) + '\r\n')
        embed.add_field(name=translates.get('owner' + guildlang), value=emotes.get('botowner')+'PythonGen#9053', inline=True)
        embed.add_field(name=translates.get('library' + guildlang),
                        value=emotes.get('libraryicon')+"[discord.py {}](https://pypi.org/project/discord.py/)".format(str(discord.__version__)),
                        inline=True)
        embed.add_field(name=translates.get('prefix' + guildlang), value='`'+prefix+'`', inline=True)
        embed.add_field(name=translates.get('host' + guildlang), value=host, inline=True)
        embed.add_field(name=translates.get('totalguilds' + guildlang), value=str(len(servers)), inline=True)
        embed.add_field(name=translates.get('botversion' + guildlang), value='ReWrite 1.0 alpha', inline=True)
        embed.add_field(name=translates.get('botname' + guildlang), value=self.bot.user.name, inline=True)
        embed.add_field(name=translates.get('ping' + guildlang),
                        value=str(round(self.bot.latency, 2)) + translates.get('ms' + guildlang), inline=True)
        embed.add_field(name=translates.get('used' + guildlang),
                        value='[[Wikipedia]](https://pypi.org/project/wikipedia/)', inline=True)
        embed.add_field(name=translates.get('supportserver' + guildlang),
                        value=translates.get('clickhere' + guildlang) + "(https://discord.gg/tRQbVUgKqw)",
                        inline=True)
        embed.add_field(name=translates.get('botinvite' + guildlang),
                        value=translates.get('clickhere' + guildlang) + "(http://bit.ly/furprotobot)", inline=True)

        embed.add_field(name='GitHub',
                        value=emotes.get('github')+translates.get('clickhere' + guildlang) + "(https://github.com/PythonGen-dev/ProtoBot)",
                        inline=True)
        embed.set_footer(text='PythonGen © 2021 All rights reserved')
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(UtilitiesCog(bot))
