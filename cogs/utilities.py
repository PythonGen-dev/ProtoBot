import datetime
import json
import random
import socket
from io import BytesIO

import discord
from PIL import Image
from discord.ext import commands
from discord.ext.commands import MemberConverter

from modules import storage

translates = storage("./locals/langs.lang")
import requests

emotes = storage("./locals/emotes.lang")

with open("config.json", "r") as configjson:
    configdata = json.load(configjson)
    discordbotsggtoken = configdata["discordbotsggtoken"]
    fetchusertoken = configdata["fetchusertoken"]
    configjson.close()


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
                            getcustomemote(self=self, emote='allusers', ctx=ctx) + translates.get(
                                "allUsers" + guildlang), ctx.guild.member_count,
                            getcustomemote(self=self, emote='bot', ctx=ctx) + translates.get("botUsers" + guildlang),
                            botsinservercount,
                            getcustomemote(self=self, emote='human', ctx=ctx) + translates.get("realUsers" + guildlang),
                            ctx.guild.member_count - botsinservercount,
                            inline=True))

        embed.add_field(name=translates.get("Channels" + guildlang),
                        value="> **{0}** {1}\r\n > **{2}** {3}\r\n > **{4}** {5}".format(
                            getcustomemote(self=self, emote='AllChannels', ctx=ctx) + translates.get(
                                "allUsers" + guildlang), all_channel_count,
                            getcustomemote(self=self, emote='VoiceChannels', ctx=ctx) + translates.get(
                                "VoiceChannels" + guildlang), voice_channel_count,
                            getcustomemote(self=self, emote='TextChannels', ctx=ctx) + translates.get(
                                "TextChannels" + guildlang), text_channel_count), inline=True)
        voiceregion = str(ctx.guild.region)
        verificationlvl = str(ctx.guild.verification_level)
        servowner = await self.bot.fetch_user(ctx.guild.owner_id)
        embed.add_field(name=translates.get("serverInfoRegion" + guildlang),
                        value='> ' + getcustomemote(self=self, emote=voiceregion, ctx=ctx) + translates.get(
                            voiceregion + guildlang),
                        inline=True)
        embed.add_field(name=translates.get("serverInfoOwner" + guildlang),
                        value='> ' + getcustomemote(self=self, emote='owner', ctx=ctx) + str(servowner), inline=True)
        embed.add_field(name=translates.get("VerificationLevel" + guildlang),
                        value='> ' + getcustomemote(self=self, emote=verificationlvl, ctx=ctx) + translates.get(
                            verificationlvl + guildlang),
                        inline=True)
        creationmonth = str(ctx.guild.created_at.strftime("%m"))
        creationdate = str(ctx.guild.created_at.strftime(
            "%d " + translates.get(creationmonth + "month" + guildlang) + " %Y" + translates.get(
                "year" + guildlang) + ", %H:%M:%S"))
        embed.add_field(name=translates.get("guildCreationDate" + guildlang), value='> ' + str(creationdate),
                        inline=True)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text="ID: " + str(ctx.guild.id))
        await ctx.send(embed=embed)

    @commands.command(name="setlang")
    @commands.has_permissions(administrator=True)
    async def setlang(self, ctx, arg=None):
        language = None
        if arg is None:
            await ctx.send(embed=discord.Embed(description='No arguments', title='Error'))
            return ()
        elif arg == "en":
            language = "EN"
        elif arg == "ru":
            language = "RU"
        if language is not None:
            langsdb = storage("./database/langsdb.db")
            langsdb.set(str(ctx.guild.id), language)
            await ctx.send(embed=discord.Embed(description='Language set to: ' + language, title='Successful'))
        else:
            await ctx.send(embed=discord.Embed(description='Invalid argument', title='Error'))

    @commands.command(name="devsetlang")
    async def devsetlang(self, ctx, arg=None):
        if str(ctx.author.id) == "605354959310946306":
            language = None
            if arg is None:
                await ctx.send(embed=discord.Embed(description='No arguments', title='Error'))
                return ()
            elif arg == "en":
                language = "EN"
            elif arg == "ru":
                language = "RU"
            if language is not None:
                langsdb = storage("./database/langsdb.db")
                langsdb.set(str(ctx.guild.id), language)
                await ctx.send(embed=discord.Embed(description='Language set to: ' + language, title='Successful'))
            else:
                await ctx.send(embed=discord.Embed(description='Invalid argument', title='Error'))

    @commands.command(name="userinfo")
    async def userinfo(self, ctx, userctx=None):
        guildlang = getlang(ctx=ctx)
        try:

            spotify = "0"

            if not userctx:
                member = ctx.author
            else:
                member = await MemberConverter().convert(ctx, userctx)

            if not member.bot:

                userid = member.id
                userinf = await self.bot.fetch_user(userid)
                embed = discord.Embed(color=0xff9900,
                                      title=translates.get("infoAbout" + guildlang) + ' ' + str(userinf))
                usersdesc = storage("./database/usersdesc.db")
                descvalue = usersdesc.get(str(ctx.author.id) + str(ctx.guild.id))
                if ctx.author.id == userid:
                    if descvalue == '0':
                        embed.add_field(name=translates.get('userdescriptiontitle' + guildlang),
                                        value=translates.get('userdescadd' + guildlang) + prefix + 'aboutme`!',
                                        inline=False)
                    else:
                        embed.add_field(name=translates.get('userdescriptiontitle' + guildlang), value=descvalue,
                                        inline=False)
                else:
                    if descvalue == '0':
                        embed.add_field(name=translates.get('userdescriptiontitle' + guildlang),
                                        value=translates.get('userdontadddesc' + guildlang), inline=False)
                    else:
                        embed.add_field(name=translates.get('userdescriptiontitle' + guildlang), value=descvalue,
                                        inline=False)

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

                usercreationdate = member.created_at.strftime("%d {0} %Y {1}, %H:%M:%S")
                usercreationdateformat = str(usercreationdate).format(
                    translates.get(str(member.created_at.strftime("%m")) + 'month' + guildlang),
                    translates.get('year' + guildlang))
                userjoineddate = member.joined_at.strftime("%d {0} %Y {1}, %H:%M:%S")
                userjoineddateformat = str(userjoineddate).format(
                    translates.get(str(member.joined_at.strftime("%m")) + 'month' + guildlang),
                    translates.get('year' + guildlang))
                if spotify == '1':
                    activityemote = getcustomemote(self=self, emote='spotify', ctx=ctx)
                else:
                    activityemote = getcustomemote(self=self, emote=str(member.status), ctx=ctx)

                if customactivitystr == 'None':
                    customactivitystr = translates.get("userActivityNone" + guildlang)

                if customactivitystr is None:
                    customactivitystr = translates.get("userActivityNone" + guildlang)

                embed.add_field(name=translates.get("basicInfo" + guildlang),
                                value='⬢** {0}**\r\n > {1}\r\n⬢** {2}**\r\n > {3} ({4})\r\n⬢** {5}**\r\n > {6} ({7})\r\n⬢** {8}**\r\n > {9}\r\n⬢** {10}**\r\n > {11}'.format(
                                    translates.get("userInfoUsername" + guildlang), userinf,
                                    translates.get("userinfoJoined" + guildlang), userjoineddateformat,
                                    getmonth(date=member.joined_at, lang=guildlang),
                                    translates.get("userinfoAccCreated" + guildlang), usercreationdateformat,
                                    getmonth(date=member.created_at, lang=guildlang),
                                    translates.get("userinfoStatus" + guildlang), activityemote + str(status),

                                    translates.get("customactivity" + guildlang), customactivitystr), inline=False)
                embed.set_footer(text="ID: " + str(userid))
                embed.set_thumbnail(url=member.avatar_url)
                badges = storage("./database/badges.db")
                badgesdata = str(badges.get(str(userid)))

                if badgesdata != "0":
                    badgeslist = badgesdata.split("$")
                    badgesstr = ''
                    for i in badgeslist:
                        if badgesstr == '':
                            badgesstr = badgesstr + "> " + getcustomemote(self=self, emote=i + 'badge',
                                                                          ctx=ctx) + ' ' + translates.get(
                                i + 'badge' + guildlang)
                        else:
                            badgesstr = badgesstr + "\r\n" + '> ' + getcustomemote(self=self, emote=i + 'badge',
                                                                                   ctx=ctx) + ' ' + translates.get(
                                i + 'badge' + guildlang)
                    embed = embed.add_field(name='⬢** {0}**'.format(translates.get('badges' + guildlang)),
                                            value=badgesstr)
                roles = ', '.join([role.mention for role in member.roles[1:]])
                if roles != '':
                    embed.add_field(
                        name='⬢ **{0} {1}**'.format(len(member.roles) - 1, translates.get('norolescount' + guildlang)),
                        value=roles + '.', inline=True)
                else:
                    embed.add_field(name='⬢ **' + translates.get('roles' + guildlang) + "** ",
                                    value=translates.get('noroles' + guildlang) + '.', inline=True)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(color=0xff9900, title=translates.get("infoAboutBotErr" + ' ' + guildlang))
                await ctx.send(embed=embed)
        except discord.ext.commands.errors.MemberNotFound:
            embed = discord.Embed(title=translates.get("error" + guildlang),
                                  description=translates.get("usernotfound" + guildlang))
            await ctx.send(embed=embed)

    @commands.command(name="addbadge")
    async def addbadge(self, ctx, arg, userctx=None):
        id = ctx.author.id
        if str(id) == '605354959310946306':
            guildlang = getlang(ctx=ctx)
            badges = storage("./database/badges.db")
            embed = discord.Embed(title='Added', description=getcustomemote(self=self, emote=arg + 'badge',
                                                                            ctx=ctx) + ' ' + translates.get(
                arg + 'badge' + guildlang))

            if not userctx:
                member = ctx.author
            else:
                member = await MemberConverter().convert(ctx, userctx)
                embed.set_author(name=member.id, icon_url=member.avatar_url)
            id = member.id
            badgesdata = str(badges.get(str(id)))
            badgeslist = badgesdata.split("$")
            if arg not in badgeslist:
                if str(badges.get(str(id))) == '0':
                    badges.set(str(id), arg)
                else:
                    data = badges.get(str(id))
                    badges.set(str(id), data + "$" + arg)

            await ctx.send(embed=embed)

    @commands.command(name="avatar")
    async def avatar(self, ctx, userctx: discord.Member = None):
        guildlang = getlang(ctx=ctx)
        member = ctx.author if not userctx else userctx
        userinf = await self.bot.fetch_user(member.id)
        img = Image.open(requests.get(member.avatar_url, stream=True).raw)
        width, height = Image.open(BytesIO(requests.get(member.avatar_url).content)).size
        colors = img.getpixel((round(width / 2), round(height / 2)))
        if member.is_avatar_animated():
            embed = discord.Embed(color=0xff9900, title=translates.get("userAvatar" + guildlang) + ' ' + str(userinf))
        else:
            embed = discord.Embed(color=discord.Colour.from_rgb(colors[0], colors[1], colors[2]),
                                  title=translates.get("userAvatar" + guildlang) + ' ' + str(userinf))
        embed = embed.set_footer(
            text=translates.get("width" + guildlang) + ': ' + str(width) + "\r\n" + translates.get(
                "height" + guildlang) + ': ' + str(height) + "\r\n" + translates.get(
                "filesize" + guildlang) + ': ' + requests.get(member.avatar_url, stream=True).headers['Content-length'])

        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="PyPI")
    async def pypi(self, ctx, *, arg=None):
        guildlang = getlang(ctx=ctx)
        name = None
        api = requests.get('https://pypi.python.org/pypi/{}/json'.format(arg.replace(' ', '-'))).json()
        try:
            name = api['info']['name']
        except:
            name = None
        versions = 0
        pypiversion = 0
        latestversion = '0'
        for i in api['releases']: versions = versions + 1
        for i in api['releases']:
            pypiversion = pypiversion + 1
            if pypiversion == versions: latestversion = i
        if name != None:
            embed = discord.Embed(title=name, url='https://pypi.org/project/' + name).set_author(name='PyPI',
                                                                                                 icon_url='https://pbs.twimg.com/profile_images/909757546063323137/-RIWgodF_400x400.jpg')
            embed = embed.add_field(name=translates.get('pypisummary' + guildlang), value=api['info']['summary'])
            embed = embed.add_field(name=translates.get('pypilicense' + guildlang), value=api['info']['license'],
                                    inline=False)
            embed = embed.add_field(name=translates.get('owner' + guildlang), value=api['info']['author'], inline=False)
            embed = embed.add_field(name=translates.get('pypiversion' + guildlang), value=latestversion, inline=False)
            embed = embed.add_field(name=translates.get('pypisetup' + guildlang),
                                    value='```' + 'pip install ' + api['info']['name'] + '```',
                                    inline=False)

            await ctx.send(embed=embed)

    @commands.command(name="aboutme")
    async def aboutme(self, ctx, *, args=None):
        guildlang = getlang(ctx=ctx)
        if args is None:
            await ctx.send(embed=discord.Embed(title=translates.get('ErrNotArg' + guildlang)))
        else:
            usersdesc = storage("./database/usersdesc.db")
            usersdesc.set(str(ctx.author.id) + str(ctx.guild.id), args[:256])
            embed = discord.Embed(title=translates.get('userdescriptionsetted' + guildlang),
                                  description=str(args[:256]))
            await ctx.send(embed=embed)

    @commands.command(name="discordbots")
    async def discordbots(self, ctx, arg=None):
        guildlang = getlang(ctx=ctx)
        TOKEN = discordbotsggtoken
        embed = discord.Embed(title='discord.bots.gg', url='https://discord.bots.gg/')
        embed.set_author(icon_url='https://discord.bots.gg/img/logo_transparent.png', name='discord.bots.gg')
        embed.set_thumbnail(url='https://discord.bots.gg/img/logo_transparent.png')
        if arg is None:
            count = \
                requests.get(url='https://discord.bots.gg/api/v1/bots?limit=1',
                             headers={"Authorization": TOKEN}).json()[
                    'count']
            ranges: int = round(count / 5)
            randomranges: int = random.randrange(1, ranges)
            r = requests.get(url='https://discord.bots.gg/api/v1/bots?limit=5&page={0}'.format(str(randomranges)),
                             headers={"Authorization": TOKEN})
            embed.set_footer(text="Page " + str(randomranges) + "/" + str(ranges))
            for i in r.json()['bots']:
                embed = embed.add_field(name='`' + i['username'] + '`', value='**Description:** ' + i[
                    'shortDescription'] + ' \r\n**LINK:** https://discord.bots.gg/bots/' + i[
                                                                                  'userId'] + ' \r\n**ID:** ' + i[
                                                                                  'userId'], inline=False)
        else:
            r = requests.get(url='https://discord.bots.gg/api/v1/bots/' + arg, headers={"Authorization": TOKEN})
            print(r.text)
            if r.text == '{"message":"An invalid user ID was specified."}':
                embed.add_field(name=translates.get('error' + guildlang), value=translates.get('unkarg' + guildlang))
            elif r.text == '{"message":"The provided user ID points to an unknown bot."}':
                embed.add_field(name=translates.get('error' + guildlang),
                                value=translates.get("notFound" + guildlang)[:-1])
            else:
                for i in r.json():
                    if i in ['clientId', 'userId', 'coOwners', 'verified', 'deleted', 'longDescription', 'addedDate',
                             'inGuild', 'online', 'avatarURL', 'openSource', 'owner', 'username', 'discriminator',
                             'supportInvite', 'website', 'helpCommand', 'status', 'shardCount', 'botInvite']:
                        if i == 'username':
                            embed.add_field(name=translates.get('botname' + guildlang),
                                            value=r.json()['username'] + '#' + r.json()['discriminator'], inline=False)
                        elif i == 'owner':
                            embed.add_field(name=translates.get('serverOwner' + guildlang),
                                            value=r.json()['owner']['username'] + '#' + r.json()['owner'][
                                                'discriminator'], inline=False)
                        elif i == 'status':
                            embed.add_field(name=translates.get('userinfoStatus' + guildlang),
                                            value=getcustomemote(self=self, emote=r.json()[i],
                                                                 ctx=ctx) + translates.get(r.json()[i] + guildlang),
                                            inline=False)
                        elif i == 'botInvite':
                            embed.add_field(name=translates.get('botinvite' + guildlang),
                                            value=translates.get('clickhere' + guildlang) + '(' + r.json()[i] + ')',
                                            inline=False)
                    else:
                        if i == 'prefix':
                            embed.add_field(name=translates.get('prefix' + guildlang), value=r.json()[i], inline=False)
                        elif i == 'libraryName':
                            embed.add_field(name=translates.get('library' + guildlang), value=r.json()[i], inline=False)
                        elif i == 'guildCount':
                            embed.add_field(name=translates.get('totalguilds' + guildlang), value=r.json()[i],
                                            inline=False)
                        elif i == 'shortDescription':
                            embed.add_field(name=translates.get('description' + guildlang), value=r.json()[i],
                                            inline=False)
                        else:
                            embed.add_field(name=i, value=r.json()[i], inline=False)
                embed.set_thumbnail(url=r.json()['avatarURL'])
        await ctx.send(embed=embed)

    @commands.command(name="topcord")
    async def topcord(self, ctx, arg=None):
        id = arg
        guildlang = getlang(ctx=ctx)

        url = "http://bots.topcord.ru/api/"
        r = requests.get(url + str(id)).json()
        try:
            embed = discord.Embed(title='bots.topcord.ru', url='https://bots.topcord.ru/')
            embed.set_author(icon_url='https://bots.topcord.ru/assets/logo.png', name='bots.topcord.ru')
            embed.set_thumbnail(url='https://bots.topcord.ru/assets/logo.png')
            e = r['error']
            embed.add_field(name=translates.get('error' + guildlang),
                            value=translates.get("notFound" + guildlang)[:-1])
        except:
            embed = discord.Embed(title='bots.topcord.ru', url='https://bots.topcord.ru/bots/'+id)
            embed.set_author(icon_url='https://bots.topcord.ru/assets/logo.png', name='bots.topcord.ru')
            embed.set_thumbnail(url='https://bots.topcord.ru/assets/logo.png')
            for i in r:
                if i in ['customInvite', 'bot', 'owner', 'botWebsite', 'date', 'botTags', 'upvotes']:
                    if i == 'bot':
                        fetchuser = requests.get(url='https://discordapp.com/api/v6/users/' + str(r[i]['id']), headers={'authorization': 'Bot ' + fetchusertoken})
                        embed.add_field(name=translates.get('botname' + guildlang), value=fetchuser.json()['username'] + '#' + fetchuser.json()['discriminator'], inline=False)
                        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/'+str(r[i]['id'])+'/'+fetchuser.json()['avatar']+".png")

                    elif i == 'owner':
                        fetchuser = requests.get(url='https://discordapp.com/api/v6/users/' + str(r[i]['id']), headers={'authorization': 'Bot ' + fetchusertoken})
                        embed.add_field(name=translates.get('serverOwner' + guildlang), value=fetchuser.json()['username'] + '#' + fetchuser.json()['discriminator'], inline=False)
                    elif i == 'customInvite':
                        embed.add_field(name=translates.get('botinvite' + guildlang), value=translates.get('clickhere' + guildlang) + '(' + r[i] + ')', inline=False)
                    elif i == 'botTags':
                        if str(r[i]) != "[]":
                            tags = ""
                            for t in r[i]:
                                if tags == "": tags = translates.get(t+"tag"+guildlang) + ", "
                                else: tags = tags + translates.get(t+"tag"+guildlang) +", "
                            if tags[-2] == ',': tags = tags[:-2]
                            embed.add_field(name=translates.get('tags' + guildlang), value=tags, inline=False)
                    elif i == 'upvotes':
                        embed.add_field(name=translates.get('upvotes' + guildlang), value=r[i], inline=False)
                    elif i == 'date':
                        for t in r[i]:
                            date = str(str(r[i][t]).split(' ')[0]).split("-")
                            date = date[2] +' '+ translates.get(date[1] +'month'+ guildlang) +' '+ date[0]+' '+translates.get('year'+guildlang)
                            embed.add_field(name=translates.get(t +'topcord' + guildlang), value=date, inline=False)
                else:
                    if i == 'prefix':
                        embed.add_field(name=translates.get('prefix' + guildlang), value=r[i], inline=False)
                    elif i == 'shortDesc':
                        embed.add_field(name=translates.get('description' + guildlang), value=r[i],
                                        inline=False)
                    else:
                        embed.add_field(name=i, value=r[i], inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="about")
    async def about(self, ctx):
        global prefix
        host = socket.gethostname()
        if host[:7] == 'DESKTOP':
            host = getcustomemote(self=self, emote='desktop', ctx=ctx) + ' Windows 10 Pro'
        elif host[:3] == 'WIN':
            host = getcustomemote(self=self, emote='desktop', ctx=ctx) + ' Windows Server 2019'
        else:
            host = getcustomemote(self=self, emote='hosticon', ctx=ctx) + ' Heroku'
        guildlang = getlang(ctx=ctx)
        servers = list(self.bot.guilds)
        embed = discord.Embed(color=0xff9900, title=self.bot.user.name + ' ' + translates.get('bot' + guildlang),
                              description=translates.get('aboutdesc' + guildlang) + '\r\n\r\n' + translates.get(
                                  'helplistend' + guildlang).replace('!=', str(prefix)) + '\r\n')
        embed.add_field(name=translates.get('owner' + guildlang),
                        value=getcustomemote(self=self, emote='botowner', ctx=ctx) + 'PythonGen#9053', inline=True)
        embed.add_field(name=translates.get('library' + guildlang), value=getcustomemote(self=self, emote='libraryicon',
                                                                                         ctx=ctx) + "[discord.py {}](https://pypi.org/project/discord.py/)".format(
            str(discord.__version__)), inline=True)
        embed.add_field(name=translates.get('prefix' + guildlang), value='`' + prefix + '`', inline=True)
        embed.add_field(name=translates.get('host' + guildlang), value=host, inline=True)
        embed.add_field(name=translates.get('totalguilds' + guildlang), value=str(len(servers)), inline=True)
        embed.add_field(name=translates.get('botversion' + guildlang), value='ReWrite 1.0 alpha', inline=True)
        embed.add_field(name=translates.get('used' + guildlang),
                        value='[[Wikipedia]](https://pypi.org/project/wikipedia/)', inline=True)
        embed.add_field(name=translates.get('supportserver' + guildlang),
                        value=translates.get('clickhere' + guildlang) + "(https://discord.gg/tRQbVUgKqw)", inline=True)
        embed.add_field(name=translates.get('botinvite' + guildlang),
                        value=translates.get('clickhere' + guildlang) + "(http://bit.ly/furprotobot)", inline=True)

        embed.set_footer(text='PythonGen © 2021 All rights reserved')
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(UtilitiesCog(bot))
