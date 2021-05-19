import contextlib
import datetime
import aiohttp
import io
import cloudscraper
import json
import shutil
import psutil
import random
from typing import Optional
from discord import TextChannel
import socket
import time
import discord
import utils.aiopg as aiopg
from discord.ext import commands
from discord.ext.commands import MemberConverter
from utils.modules import getcolorfromurl, aiogetlang, getcustomemote, translations, apifetchuser
import requests

with open("config.json", "r") as configjson:
    configdata = json.load(configjson)
    discordbotsggtoken = configdata["discordbotsggtoken"]
    fetchusertoken = configdata["fetchusertoken"]
    herokuapikey = configdata["herokuapikey"]
    boticordtoken = configdata["boticordtoken"]
    twitchclientid = configdata["twitchclientid"]
    configjson.close()




prefix = json.load(open("config.json", "r"))["prefix"]

partners = [
#["bot", "<:cupcake:844191415193698305> Cupcake", "https://discord.com/oauth2/authorize?client_id=839622807410573323&scope=bot&permissions=4027575551", "https://discord.gg/FwxBp6Mh3Z"], #памятка: Не разкомечивать, блинчик пидорас!!! 
["bot", "<:luna:844198363229454378> LunaBot", "https://discord.com/oauth2/authorize?client_id=791323269625282570&scope=bot&permissions=872411134", "https://discord.gg/u6Ec7puDnj"],
["server", "<:azurblau:844198509540671518> Ａｚｕｒｅ", "https://discord.gg/KacqeMr3Qp"], 
]

def getpartners(lang):
    string = str()
    for partner in partners:
        if partner[0] == "bot":
            string += f"{partner[1]} | [{translations(lang, 'partnerbotinvite')}]({partner[2]}) [{translations(lang, 'partnerbotserver')}]({partner[3]})\r\n"
        elif partner[0] == "server": 
            string += f"{partner[1]} | [{translations(lang, 'partnerserverinvite')}]({partner[2]})\r\n"
    return string

def getmonth(date, lang):
    try:
        month = list(str(datetime.datetime.now() - date).split(",")[0].split(" "))
        if month[1] == 'days':
            rounded = str(round(int(month[0]) / 30))
            if rounded == '1':
                return rounded + ' ' + translations(lang, 'monthlow')
            else:
                return rounded + ' ' + translations(lang, 'monthsmore')
        else:
            return '0 ' + translations(lang, 'monthsmore')
    except:
        return '0 ' + translations(lang, 'monthsmore')


class UtilitiesCog(commands.Cog, name="Utilities Cog"):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="twitch", aliases=['твич'])
    async def twitch(self, ctx, user = None):
        guildlang = await aiogetlang(ctx)
        if user is None:
            await ctx.send(embed=discord.Embed(title=translations(guildlang, 'ErrNotArg' )))
            return
        headers = {"Accept": "application/vnd.twitchtv.v5+json", "Client-ID": twitchclientid}
        r=requests.get(url="https://api.twitch.tv/kraken/users?login="+user, headers=headers)
        jsondata=r.json()
        try:
            user = jsondata["users"][0]

        except IndexError:
            embed = discord.Embed(color = 0x6441a5, title = translations(guildlang, "twitchaccnotfound"+guildlang))
            await ctx.send(embed=embed)
            return
        logo = user["logo"]
        display_name = user["display_name"]
        id = user["_id"]
        r=requests.get(url="https://api.twitch.tv/kraken/streams/"+id, headers=headers)
        try:
            stream=r.json()["stream"]
            preview=stream["preview"]["large"]
        except:
            embed = discord.Embed(color = 0x6441a5, title = display_name+" "+translations(guildlang, "dontstreaming"+guildlang))
            embed = embed.set_author(icon_url = logo, name = display_name)
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(color = 0x6441a5, title = display_name+" "+translations(guildlang, "nowlive"+guildlang))
        embed = embed.set_author(icon_url = logo, name = display_name)
        embed = embed.add_field(name = translations(guildlang, "nowplaying"+guildlang), value=stream["game"])
        embed = embed.add_field(name = translations(guildlang, "spectators"+guildlang), value=stream["viewers"])
        embed = embed.set_image(url=preview)
        await ctx.send(embed = embed)


    @commands.command(name="boticord", aliases=['ботикорд'])
    async def boticord(self, ctx, arg= None):
        guildlang = await aiogetlang(ctx)
        if arg != None:
            try:
                bot = await MemberConverter().convert(ctx, arg)
                if bot.bot:
                    id = str(bot.id)
                else:
                    embed = discord.Embed(title='boticord.top', url='https://boticord.top/', description=translations(guildlang, "thisisnotbot" ), colour=0xFF0000)
                    embed.set_thumbnail(url='https://boticord.top/static/robot.png')
                    await ctx.send(embed=embed)
                    return
            except:
                id = str(arg)
            try:
                scraper = cloudscraper.create_scraper()
                r = scraper.get(url="https://boticord.top/api/v1/bot/"+id,  headers={'authorization': boticordtoken})
                boticord_api = r.json()
            except:
                embed = discord.Embed(title='boticord.top', url='https://boticord.top/', description='Failed to establish a new connection.', colour=0xFF0000)
                embed.set_thumbnail(url='https://boticord.top/static/robot.png')
                await ctx.send(embed=embed)
                return
            #набор того что нам пригодится в будущем
            try:
                info = boticord_api["information"]
                stats = info ["stats"]
                links = info["links"]
            except:
                embed = discord.Embed(title='boticord.top', url='https://boticord.top')
                embed.set_thumbnail(url='https://boticord.top/static/robot.png')
                embed.add_field(name=translations(guildlang, 'error' ), value=translations(guildlang, "notFound" )[:-1])

                await ctx.send(embed = embed)
                return
            #инфа от ботикорда
            boticord_url = boticord_api["links"][0]
            id = boticord_api["id"]
            invite = "https://discord.com/oauth2/authorize?client_id={0[id]}&permissions={0[information][permissions]}&scope=bot". format (boticord_api)
            shortdesc = info["description"]["short"]
            library = info["library"]
            prefix = info["prefix"]
            bumps = info["bumps"]
            #инфа о боте с discord api
            fetchbot = await apifetchuser(id)
            bot_created_at = datetime.datetime.utcfromtimestamp(((int(id) >> 22) + 1420070400000) / 1000).replace(tzinfo=None)
            bot_name="{0[username]}#{0[discriminator]}".format(fetchbot, id)
            bot_avatar="https://cdn.discordapp.com/avatars/{0[id]}/{0[avatar]}.png?size=1024".format(fetchbot)
            #статистика
            servers = str(stats["servers"])
            shards = str(stats["shards"])
            users = str(stats["users"])
            statistic=str()
            if servers != "0" and shards != "'0" and users != "'0":
                if servers != "'0": statistic += translations(guildlang, 'totalguilds' )+" "+servers+"\r\n"
                if shards != "'0": statistic += translations(guildlang, 'boticordshards' )+" "+shards+"\r\n"
                if users != "'0": statistic += translations(guildlang, 'boticordusers' )+" "+users+"\r\n"
            else: statistic = translations(guildlang, 'nostatistic' )
            #разрабы бота
            developers = str()
            for devid in info["developers"]:
                developers += "{0[username]}#{0[discriminator]}(ID: {1}), ".format(await apifetchuser(devid), devid)
            developers = developers[:-2]+"."
            if len(info["developers"]) == 1:
                devname = translations(guildlang, 'boticorddeveloper' )
            else: devname = translations(guildlang, 'boticorddevelopers' )

            colors = getcolorfromurl(bot_avatar)
            embed = discord.Embed(title=fetchbot["username"] + " boticord.top", url=boticord_url, color=discord.Colour.from_rgb(colors[0], colors[1], colors[2]))
            embed.add_field(name=translations(guildlang, 'botname' ), value=bot_name, inline=False)
            embed.add_field(name=devname, value=developers, inline=False)
            embed.add_field(name=translations(guildlang, 'upvotes' ), value=bumps, inline=False)
            embed.add_field(name=translations(guildlang, 'prefix' ), value=prefix, inline=False)
            embed.add_field(name=translations(guildlang, 'description' ), value=shortdesc, inline=False)
            embed.add_field(name=translations(guildlang, 'createdAttopcord' ), value=bot_created_at, inline=False)
            embed.add_field(name=translations(guildlang, 'library' ), value=library, inline=False)
            embed.add_field(name=translations(guildlang, 'statistics' ), value=statistic, inline=False)
            embed.add_field(name=translations(guildlang, 'botinvite' ), value=translations(guildlang, 'clickhere' ) + '(' + invite + ')', inline=False)
            embed.set_thumbnail(url=bot_avatar)
            embed.set_author(icon_url="https://boticord.top/static/robot.png", name='boticord.top')
            await ctx.send(embed = embed)
        else:
            await ctx.send(embed=discord.Embed(title=translations(guildlang, 'ErrNotArg' )))



    @commands.command()
    async def eval(self, ctx, *, code):
        if ctx.author.id == 605354959310946306:
            a = datetime.datetime.now()

            commandtext = str(ctx.message.content).replace("!= eval ", "").replace("!=eval ", "")
            str_obj = io.StringIO()
            try:
                with contextlib.redirect_stdout(str_obj):
                    exec(code)
            except Exception as e:
                c = datetime.datetime.now() - a
                embed = discord.Embed(title='EVAL', description="**Time:** `" + str(c.microseconds) + "ms`").add_field(
                    name='Input:', value=f"""```py\r\n{commandtext}\r\n```""", inline=False).add_field(name='Error:',
                                                                                                       value=f"""```py\r\n{e.__class__.__name__}: {e}```""")
                return await ctx.send(embed=embed)
            c = datetime.datetime.now() - a
            result = str_obj.getvalue()
            embed = discord.Embed(title='EVAL', description="**Time:** `" + str(c.microseconds) + "ms`").add_field(
                name='Input:', value=f"""```py\r\n{commandtext}\r\n```""", inline=False).set_thumbnail(
                url="https://upload.wikimedia.org/wikipedia/commons/f/f3/Termux_2.png")
            if len(result) > 1024:
                result = result[:1012]
                embed = embed.set_footer(text="The result is more than 1024 characters !!!")
            embed = embed.add_field(name='Result:', value=f"""```py\r\n{result}\r\n```""").set_thumbnail(
                url="https://upload.wikimedia.org/wikipedia/commons/f/f3/Termux_2.png")
            await ctx.send(embed=embed)

    @commands.command(name="setlang", aliases=['язык'])
    @commands.has_permissions(administrator=True)
    async def setlang(self, ctx, arg=None):
        language = None

        if arg is None:
            await ctx.send(embed=discord.Embed(description='No arguments', title='Error'))
            return ()
        elif str(arg).lower() == "en":
            language = "EN"
        elif str(arg).lower() == "ru":
            language = "RU"
        elif str(arg).lower() == "owo":
            language = "owo"
        if language is not None:
            await aiopg.aioupsertrow("langs", [["value", "'{}'".format(language)],["guildid", ctx.guild.id]], [["guildid", ctx.guild.id]])
            await ctx.send(embed=discord.Embed(description='Language set to: ' + language, title='Successful'))
        else:
            await ctx.send(embed=discord.Embed(description='Invalid argument', title='Error'))

    @commands.command(name="prefix", aliases=['префикс'])
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, arg=None):
        if arg is None:
            await ctx.send(embed=discord.Embed(description='No arguments', title='Error'))
            return
        newprefix = arg[:10]
        await aiopg.aioupsertrow("prefix", [["value", "'{}'".format(newprefix)],["guildid", ctx.guild.id]], [["guildid", ctx.guild.id]])
        await ctx.send(embed=discord.Embed(description='Prefix set to: ' + newprefix, title='Prefix'))


    @commands.command(name="welcome", aliases=['hewwo', 'приветики'])
    async def welcome(self, ctx, channel: Optional[TextChannel], *, message=None):
        channel = channel or ctx.channel
        guildlang = await aiogetlang(ctx)
        if message != None:
            embed = discord.Embed(title = "Welcome", color = 0x00FF00)
            embed.add_field(name = translations(guildlang, 'channel'), value = channel.mention)
            embed.add_field(value = str(message), name = translations(guildlang, 'notifytextinfo'))
            await aiopg.aioupsertrow("welcome", [["value", "'{}'".format(str(message))],["guildid", ctx.guild.id],["channelid", channel.id]], [["guildid", ctx.guild.id]])
            await ctx.reply(embed=embed, mention_author=False)
        else:
            await ctx.reply(embed=discord.Embed(title=translations(guildlang, 'ErrNotArg' )), mention_author=False)


    @commands.command(name="goodbye", aliases=['прощания'])
    async def goodbye(self, ctx, channel: Optional[TextChannel], *, message=None):
        channel = channel or ctx.channel
        guildlang = await aiogetlang(ctx)
        if message != None:
            embed = discord.Embed(title = "Goodbye", color = 0xFF0000)
            embed.add_field(name = translations(guildlang, 'channel'), value = channel.mention)
            embed.add_field(value = str(message), name = translations(guildlang, 'notifytextinfo'))
            await aiopg.aioupsertrow("goodbye", [["value", "'{}'".format(str(message))],["guildid", ctx.guild.id],["channelid", channel.id]], [["guildid", ctx.guild.id]])
            await ctx.reply(embed=embed, mention_author=False)
        else:
            await ctx.reply(embed=discord.Embed(title=translations(guildlang, 'ErrNotArg' )), mention_author=False)



    @commands.command(name="idinfo", aliases=['юзерайди'])
    async def userinfobyid(self, ctx, userid = None):
        guildlang = await aiogetlang(ctx)
        if userid is None:
            await ctx.send(embed=discord.Embed(description='No arguments', title='Error'))
        else:
            try:
                data = await apifetchuser(userid)
                avatarurl = "https://cdn.discordapp.com/avatars/{0[id]}/{0[avatar]}.png?size=1024".format(data)
                username = "{0[username]}#{0[discriminator]}".format(data)
                created_at = datetime.datetime.utcfromtimestamp(((int(data["id"]) >> 22) + 1420070400000) / 1000).replace(tzinfo=None)
                colors = getcolorfromurl(avatarurl)
                usercreationdate = created_at.strftime("%d {0} %Y {1}, %H:%M:%S")
                usercreationdateformat = str(usercreationdate).format(translations(guildlang, str(created_at.strftime("%m")) + 'month' ), translations(guildlang, 'year' ))
                embed = discord.Embed(color=discord.Colour.from_rgb(colors[0], colors[1], colors[2]), title=translations(guildlang, "infoAbout" ) + ' ' + str(username))
                embed = embed.add_field(name=translations(guildlang, "basicInfo" ), value='⬢** {0}**\r\n > {1}\r\n⬢** {2}**\r\n > {3} ({4})'.format(translations(guildlang, "userInfoUsername" ), username, translations(guildlang, "userinfoAccCreated" ), usercreationdateformat, getmonth(date=created_at, lang=guildlang)), inline=False)
                embed.set_footer(text="ID: " + str(userid))
                embed.set_thumbnail(url=avatarurl)
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(title=translations(guildlang, "error" ), description=translations(guildlang, "notFound" )[:-1])
                await ctx.send(embed=embed)
                            
            



    @commands.command(name="avatar", aliases=['аватар', 'аватарка'])
    async def avatar(self, ctx, userctx: discord.Member = None):
        guildlang = await aiogetlang(ctx)
        member = ctx.author if not userctx else userctx
        userinf = await self.bot.fetch_user(member.id)
        colors = getcolorfromurl(member.avatar_url)
        if member.is_avatar_animated():
            embed = discord.Embed(color=0xff9900, title=translations(guildlang, "userAvatar" ) + ' ' + str(userinf))
        else:
            embed = discord.Embed(color=discord.Colour.from_rgb(colors[0], colors[1], colors[2]),
                                  title=translations(guildlang, "userAvatar" ) + ' ' + str(userinf))
        embed = embed.set_footer(
            text=translations(guildlang, "filesize" ) + ': ' + requests.get(member.avatar_url, stream=True).headers[
                'Content-length'])
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="PyPI")
    async def pypi(self, ctx, *, arg=None):
        guildlang = await aiogetlang(ctx)
        name = None

        try:
            api = requests.get('https://pypi.python.org/pypi/{}/json'.format(arg.replace(' ', '-'))).json()     
            name = api['info']['name']
        except:
            name = None
        versions = 0
        pypiversion = 0
        latestversion = '0'
        if name != None:
            for i in api['releases']: versions = versions + 1
            for i in api['releases']:
                pypiversion = pypiversion + 1
                if pypiversion == versions: latestversion = i
            embed = discord.Embed(title=name, url='https://pypi.org/project/' + name).set_author(name='PyPI',
                                                                                                 icon_url='https://pbs.twimg.com/profile_images/909757546063323137/-RIWgodF_400x400.jpg')
            embed = embed.add_field(name=translations(guildlang, 'pypisummary' ), value=api['info']['summary'])
            embed = embed.add_field(name=translations(guildlang, 'pypilicense' ), value=api['info']['license'],
                                    inline=False)
            embed = embed.add_field(name=translations(guildlang, 'owner' ), value=api['info']['author'], inline=False)
            embed = embed.add_field(name=translations(guildlang, 'pypiversion' ), value=latestversion, inline=False)
            embed = embed.add_field(name=translations(guildlang, 'pypisetup' ),
                                    value='```' + 'pip install ' + api['info']['name'] + '```',
                                    inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=discord.Embed(title=translations(guildlang, 'ErrNotArg' )))

    @commands.command(name="aboutme", aliases=['осебе'])
    async def aboutme(self, ctx, *, args=None):
        guildlang = await aiogetlang(ctx)
        if args is None:
            await ctx.send(embed=discord.Embed(title=translations(guildlang, 'ErrNotArg' )))
        else:
            await aiopg.aioupsertrow("userdescs", [["value", "'{}'".format(args[:256])],["guildid", ctx.guild.id], ["userid", ctx.author.id]], [["guildid", ctx.guild.id], ["userid", ctx.author.id]])
            embed = discord.Embed(title=translations(guildlang, 'userdescriptionsetted' ),
                                  description=str(args[:256]))
            await ctx.send(embed=embed)

    @commands.command(name="discordbots")
    async def discordbots(self, ctx, arg=None):
        guildlang = await aiogetlang(ctx)
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
            if r.text == '{"message":"An invalid user ID was specified."}':
                embed.add_field(name=translations(guildlang, 'error' ), value=translations(guildlang, 'unkarg' ))
            elif r.text == '{"message":"The provided user ID points to an unknown bot."}':
                embed.add_field(name=translations(guildlang, 'error' ),
                                value=translations(guildlang, "notFound" )[:-1])
            else:
                for i in r.json():
                    if i in ['clientId', 'userId', 'coOwners', 'verified', 'deleted', 'longDescription', 'addedDate',
                             'inGuild', 'online', 'avatarURL', 'openSource', 'owner', 'username', 'discriminator',
                             'supportInvite', 'website', 'helpCommand', 'status', 'shardCount', 'botInvite']:
                        if i == 'username':
                            embed.add_field(name=translations(guildlang, 'botname' ),
                                            value=r.json()['username'] + '#' + r.json()['discriminator'], inline=False)
                        elif i == 'owner':
                            embed.add_field(name=translations(guildlang, 'serverOwner' ),
                                            value=r.json()['owner']['username'] + '#' + r.json()['owner'][
                                                'discriminator'], inline=False)
                        elif i == 'status':
                            embed.add_field(name=translations(guildlang, 'userinfoStatus' ),
                                            value=getcustomemote(self, r.json()[i],
                                                                 ctx) + translations(guildlang, r.json()[i] ),
                                            inline=False)
                        elif i == 'botInvite':
                            embed.add_field(name=translations(guildlang, 'botinvite' ),
                                            value=translations(guildlang, 'clickhere' ) + '(' + r.json()[i] + ')',
                                            inline=False)
                    else:
                        if i == 'prefix':
                            embed.add_field(name=translations(guildlang, 'prefix' ), value=r.json()[i], inline=False)
                        elif i == 'libraryName':
                            embed.add_field(name=translations(guildlang, 'library' ), value=r.json()[i], inline=False)
                        elif i == 'guildCount':
                            embed.add_field(name=translations(guildlang, 'totalguilds' ), value=r.json()[i],
                                            inline=False)
                        elif i == 'shortDescription':
                            embed.add_field(name=translations(guildlang, 'description' ), value=r.json()[i],
                                            inline=False)
                        else:
                            embed.add_field(name=i, value=r.json()[i], inline=False)
                embed.set_thumbnail(url=r.json()['avatarURL'])
        await ctx.send(embed=embed)


    @commands.command(name="topcord", aliases=['топкорд', 'топорик'])
    async def topcord(self, ctx, *, arg=None):
        guildlang = await aiogetlang(ctx)
        if arg != None:
            try:
                bot = await MemberConverter().convert(ctx, arg)
                if bot.bot:
                    id = str(bot.id)
                else:
                    embed = discord.Embed(title='bots.topcord.ru', url='https://bots.topcord.ru/',
                                          description=translations(guildlang, "thisisnotbot" ), colour=0xFF0000)
                    embed.set_author(icon_url='https://bots.topcord.ru/assets/logo.png', name='bots.topcord.ru')
                    embed.set_thumbnail(url='https://bots.topcord.ru/assets/logo.png')
                    await ctx.send(embed=embed)
                    return

            except:
                id = str(arg)
            url = "http://bots.topcord.ru/api/"
            try:
                async with aiohttp.ClientSession() as ses:
                    async with ses.get(url+str(id)) as r:
                       r = await r.json()
            except:
                embed = discord.Embed(title='bots.topcord.ru', url='https://bots.topcord.ru/',
                                      description='Failed to establish a new connection.', colour=0xFF0000)
                embed.set_author(icon_url='https://bots.topcord.ru/assets/logo.png', name='bots.topcord.ru')
                embed.set_thumbnail(url='https://bots.topcord.ru/assets/logo.png')
                await ctx.send(embed=embed)
                return
            try:
                embed = discord.Embed(title='bots.topcord.ru', url='https://bots.topcord.ru/')
                embed.set_author(icon_url='https://bots.topcord.ru/assets/logo.png', name='bots.topcord.ru')
                embed.set_thumbnail(url='https://bots.topcord.ru/assets/logo.png')
                e = r['error']
                embed.add_field(name=translations(guildlang, 'error' ),
                                value=translations(guildlang, "notFound" )[:-1])
            except:
                fetchuser = await apifetchuser(r['bot']['id'])
                avatar = 'https://cdn.discordapp.com/avatars/' + str(r['bot']['id']) + '/' + fetchuser[
                    'avatar'] + ".png"
                colors = getcolorfromurl(avatar)
                embed = discord.Embed(title=fetchuser['username'] + ' bots.topcord.ru',
                                      url='https://bots.topcord.ru/bots/' + id,
                                      color=discord.Colour.from_rgb(colors[0], colors[1], colors[2]))
                embed.set_author(icon_url='https://bots.topcord.ru/assets/logo.png', name='bots.topcord.ru')
                embed.set_thumbnail(url='https://bots.topcord.ru/assets/logo.png')
                for i in r:
                    if i in ['customInvite', 'bot', 'owner', 'botWebsite', 'date', 'botTags', 'upvotes']:
                        if i == 'bot':
                            embed.add_field(name=translations(guildlang, 'botname' ),
                                            value="<@{0}> `(".format(fetchuser['id'])+fetchuser['username'] + '#' + fetchuser['discriminator']+")`",
                                            inline=False)
                            embed.set_thumbnail(url=avatar)
                        elif i == 'owner':
                            fetchuser = await apifetchuser(r[i]['id'])
                            embed.add_field(name=translations(guildlang, 'serverOwner' ),
                                            value="<@{0}> `(".format(fetchuser['id'])+fetchuser['username'] + '#' + fetchuser['discriminator']+")`",
                                            inline=False)
                        elif i == 'customInvite':
                            embed.add_field(name=translations(guildlang, 'botinvite' ),
                                            value=translations(guildlang, 'clickhere' ) + '(' + r[i] + ')', inline=False)
                        elif i == 'botTags':
                            if str(r[i]) != "[]":
                                tags = ""
                                for t in r[i]:
                                    if tags == "":
                                        tags = translations(guildlang, t + "tag" ) + ", "
                                    else:
                                        tags = tags + translations(guildlang, t + "tag" ) + ", "
                                if tags[-2] == ',': tags = tags[:-2]
                                embed.add_field(name=translations(guildlang, 'tags' ), value=tags, inline=False)
                        elif i == 'upvotes':
                            embed.add_field(name=translations(guildlang, 'upvotes' ), value=r[i], inline=False)
                        elif i == 'date':
                            for t in r[i]:
                                date = str(str(r[i][t]).split(' ')[0]).split("-")
                                date = date[2] + ' ' + translations(guildlang, date[1] + 'month' ) + ' ' + date[
                                    0] + ' ' + translations(guildlang, 'year' )
                                embed.add_field(name=translations(guildlang, t + 'topcord' ), value=date, inline=False)
                    else:
                        if i == 'prefix':
                            embed.add_field(name=translations(guildlang, 'prefix' ), value="`"+str(r[i])+"`", inline=False)
                        elif i == 'shortDesc':
                            embed.add_field(name=translations(guildlang, 'description' ), value=r[i],
                                            inline=False)
                        else:
                            embed.add_field(name=i, value=r[i], inline=False)
            await ctx.send(embed=embed)
        else:
            try:
                before = time.monotonic()
                async with aiohttp.ClientSession() as ses:
                    async with ses.get('https://bots.topcord.ru/api') as r:
                       r = await r.json()
                ping = (time.monotonic() - before) * 1000
                desc = str()
                desc += translations(guildlang, 'totalbots' )+" {0}\r\n".format(r["bots"])
                desc += translations(guildlang, 'parciseping' )+" {0}ms\r\n".format(r["botping"])
                desc += translations(guildlang, 'apilatency' )+" {0}ms\r\n".format(str(int(ping)))

                desc += translations(guildlang, 'apiver' )+" {0}\r\n".format(r["version"])

                embed = discord.Embed(title=translations(guildlang, 'topcordstats' ), url='https://bots.topcord.ru/', description=desc, color = 0x7289DA)
                embed.set_author(icon_url='https://bots.topcord.ru/assets/logo.png', name='bots.topcord.ru')
                embed.set_thumbnail(url='https://bots.topcord.ru/assets/logo.png')

                await ctx.send(embed=embed)
                

            except:
                embed = discord.Embed(title='bots.topcord.ru', url='https://bots.topcord.ru/',
                                      description='Failed to establish a new connection.', colour=0xFF0000)
                embed.set_author(icon_url='https://bots.topcord.ru/assets/logo.png', name='bots.topcord.ru')
                embed.set_thumbnail(url='https://bots.topcord.ru/assets/logo.png')
                await ctx.send(embed=embed)
                return


    @commands.command(name="emojis-list", aliases=['allemojis', 'всеэмодзи'])
    async def allemotes(self, ctx):
        emotes = list()
        for I in ctx.guild.emojis: emotes.append(str(I))
        embed = discord.Embed(title = len(emotes), description="".join(emotes), color = 0xFF00FF)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="roles-list", aliases=['allroles', 'всероли'])
    async def allroles(self, ctx):
        roles = ', '.join([role.mention for role in ctx.guild.roles[1:]])
        embed = discord.Embed(title = len(ctx.guild.roles), description=roles, color = 0xFF00FF)
        await ctx.reply(embed=embed, mention_author=False)




    @commands.command(name="about", aliases=['бот', 'bot'])
    async def about(self, ctx):
        prefix = await self.bot.command_prefix(self.bot, ctx.message)
        host = socket.gethostname()
        if host[:7] == 'DESKTOP':
            host = getcustomemote(self, 'desktop', ctx) + ' Windows 10 Pro'
        elif host[:3] == 'WIN':
            host = getcustomemote(self, 'desktop', ctx) + ' Windows Server 2019'
        else:
            host = getcustomemote(self, 'hosticon', ctx) + ' Heroku'
        guildlang = await aiogetlang(ctx)
        servers = list(self.bot.guilds)
        embed = discord.Embed(color=0xffffff, title=self.bot.user.name, description=translations(guildlang, 'aboutdesc' ) + '\r\n\r\n' + translations(guildlang, 'helplistend' ).replace('!=', str(prefix)) + '\r\n')
        embed.add_field(name=translations(guildlang, 'owner' ),value=getcustomemote(self, 'botowner', ctx) + 'PythonGen#9053', inline=True)
        embed.add_field(name=translations(guildlang, 'library' ), value=getcustomemote(self, 'libraryicon', ctx) + "[discord.py {}](https://pypi.org/project/discord.py/)".format(str(discord.__version__)), inline=True)
        embed.add_field(name=translations(guildlang, 'prefix' ), value=f"`{prefix}`", inline=True)
        embed.add_field(name=translations(guildlang, 'totalguilds' ), value=str(len(servers)), inline=True)
        embed.add_field(name=translations(guildlang, 'botversion' ), value='rewrite 1.3.6', inline=True)
        embed.add_field(name=translations(guildlang, 'supportserver' ), value=translations(guildlang, 'clickhere' ) + "(https://discord.gg/99SeJhG9Ed)", inline=True)
        embed.add_field(name=translations(guildlang, 'botinvite' ), value=translations(guildlang, 'clickhere' ) + "(http://bit.ly/furprotobot)", inline=True)
        embed.add_field(name=translations(guildlang, 'partnerbotcategory'), value=getpartners(guildlang), inline=True)
        embed.add_field(name=translations(guildlang, 'specialthanksabout'), value="Pancake | Ａｚ✨#7846\r\nK1ng Of Protogen | Ａｚ ✨#8467", inline=True)
        try:
            embed.add_field(name=translations(guildlang, 'cpuusage' ), value=getcustomemote(self, 'cpu', ctx) + "{0}%". format(psutil.cpu_percent()), inline=True)
            embed.add_field(name=translations(guildlang, 'ramusage' ), value=getcustomemote(self, 'ram', ctx) + "{0}/{1} GB".format(round(psutil.virtual_memory().used / (1024.0 ** 3), 1),round(psutil.virtual_memory(). total / (1024.0 ** 3), 1)), inline=True)
            embed.add_field(name=translations(guildlang, 'storageusage' ), value=getcustomemote(self, 'storage', ctx) + "{0}/{1} GB".format(round(shutil.disk_usage("/").used / (1024.0 ** 3), 1),round(shutil.disk_usage("/").total / (1024.0 ** 3), 1)), inline=True)
        except: pass
        embed.set_footer(text='PythonGen © 2021 All rights reserved')
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)



def setup(bot):
    bot.add_cog(UtilitiesCog(bot))
