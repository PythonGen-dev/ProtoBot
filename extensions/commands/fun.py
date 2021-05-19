import json
import random
import xmltodict
import art
import discord
import asyncpraw
import requests
from PIL import Image
from discord.ext import commands
from discord.ext.commands import MemberConverter
from langdetect import detect
from transliterate import translit
import utils.aiopg as aiopg
import io
import vk_api
from utils.checks import *
import aiohttp
from random import randint
from utils.modules import getcolorfromurl, aiogetlang, translations
from utils.exceptions import NoPremiumException

with open("config.json", "r") as configjson:
    configdata = json.load(configjson)
    unsplashclientid = configdata["unsplashclientid"]
    pixabayapikey = configdata["pixabayapikey"]
    redditclientid = configdata["redditclientid"]
    redditclientsecret = configdata["redditclientsecret"]
    vk_app_id = configdata["vk_app_id"]
    vk_app_token = configdata["vk_app_token"]
    configjson.close()

is_premium = commands.check(checkpremium)

    
reddit = asyncpraw.Reddit(client_id=redditclientid, client_secret=redditclientsecret, user_agent="protobotfun")

def vk_api_login():
    vk_session = vk_api.VkApi(app_id=vk_app_id, token=vk_app_token)
    vk = vk_session.get_api()
    return vk    
def get_posts_count(domain):
    count = vk_api_login().wall.get(count=1, domain = domain)["count"]
    return count
def get_random_post(domain):
    count = get_posts_count(domain)-1
    offset = randint (0, count)
    post = vk_api_login().wall.get(count=1, offset = offset, domain = domain)
    return post["items"][0]
def get_random_post_no_ads(domain):
    post = get_random_post(domain)
    loop = True
    if str(post["marked_as_ads"]) == "1":
        while loop == True:
            post = get_random_post(domain)
            if str(post["marked_as_ads"]) == "0":
                return post
    else: 
        return post
def get_random_post_attachment_no_ads(domain):
    post = get_random_post_no_ads(domain)
    loop = True
    if len(post["attachments"]) != 1:
        while loop == True:
            post = get_random_post(domain)
            if len(post["attachments"]) == 1:
                return post
    else: 
        return post
def get_photo_max_scale(post):
    data = post["attachments"][0]["photo"]["sizes"][-1]
    return data["url"]


class FunCog(commands.Cog, name="Fun module"):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="minecraft", aliases=["майн", "майнкрафт"])
    async def minecraft(self, ctx, arg=None):
        guildlang = await aiogetlang(ctx)
        footer_image = "https://static.wikia.nocookie.net/minecraft_ru_gamepedia/images/e/e5/%D0%94%D1%91%D1%80%D0%BD.png/revision/latest/scale-to-width-down/160?cb=20200518110227"
        if arg is None: await ctx.send(embed=discord.Embed(color=0x5E924E, title="Error: No arguments").set_footer(icon_url=footer_image,text="Minecraft command"))
        else:
            try:
                async with aiohttp.ClientSession() as ses:
                    async with ses.get("https://api.mojang.com/users/profiles/minecraft/" + arg) as r:
                       json_data = await r.json()
                skin = "https://crafatar.com/skins/" + json_data["id"] + "?size=4.png"
                head = "https://crafatar.com/renders/head/" + json_data["id"] + ".png"
                colors = getcolorfromurl(head)
                await ctx.send(embed=discord.Embed(color=discord.Colour.from_rgb(colors[0], colors[1], colors[2]), title=translations(guildlang, "username") + " " + json_data["name"], description="\r\n**UUID:** " + json_data["id"] + "\r\n\r\n {} ".format(translations(guildlang, "skin"))).set_thumbnail(url="https://crafatar.com/renders/body/" + json_data["id"] + ".png").set_image(url=skin).set_footer(icon_url=head, text="Minecraft command"))
            except:
                tlskin = f"https://tlauncher.org/upload/all/nickname/tlauncher_{arg}.png"
                tlrender = f"https://tlauncher.org/skin.php?username_catalog=nickname&username_file=tlauncher_{arg}.png"
                async with aiohttp.ClientSession(headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}) as ses:
                    async with ses.get(tlskin) as sesget:
                        if sesget.status == 200: scode = True
                        else: scode = False
                if scode == False:
                    await ctx.send(embed=discord.Embed(color=0x5E924E, title=translations(guildlang, "error"),description=translations(guildlang, "notFound")[:-1]).set_footer(icon_url=footer_image, text="Minecraft command"))
                    return
                await ctx.send(embed=discord.Embed(title=translations(guildlang, "username") + " " + str(arg), description="\r\n\r\n\r\n {} ".format(translations(guildlang, "skin"))).set_thumbnail(url=tlrender).set_image(url=tlskin).set_footer(text="Minecraft command"))
    @commands.command(name="getemoji", aliases=["эмодзи", "эмоция", "emoji"])
    async def getemoji(self, ctx, arg: discord.Emoji = None):
        try:
            guildlang = await aiogetlang(ctx)
            if arg is None:
                await ctx.send(embed=discord.Embed(title=translations(guildlang, "ErrNotArg")))
            else:
                colors = getcolorfromurl(arg.url)
                if arg.animated:
                    embed = discord.Embed(title=arg.name).set_image(url=arg.url)
                else:
                    embed = discord.Embed(title=arg.name,
                                          color=discord.Colour.from_rgb(colors[0], colors[1], colors[2])).set_image(
                        url=arg.url)
                embed = embed.set_footer(
                    text=translations(guildlang, "filesize") + ": " + requests.get(arg.url, stream=True).headers["Content-length"])
                await ctx.send(embed=embed)
        except discord.ext.commands.errors.EmojiNotFound:
            embed = discord.Embed(title=translations(guildlang, "error"),
                                  description=translations(guildlang, "notFound")[:-1])
            await ctx.send(embed=embed)
        except AttributeError:
            embed = discord.Embed(title=translations(guildlang, "error"),
                                  description=translations(guildlang, "unkarg"))
            await ctx.send(embed=embed)



    @commands.command(name="pixelate", aliases=["pixel", "пиксель"])
    async def pixelate(self, ctx, arg=None):
        guildlang = await aiogetlang(ctx)
        imgurl = ""
        if arg is None:
            try: imgurl = ctx.message.attachments[0].url
            except IndexError: imgurl = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(ctx.author)
        else:
            try: imgurl = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(await MemberConverter().convert(ctx, arg))
            except:
                if str(arg)[:4] == "http": imgurl = arg
        try:
            img = Image.open(requests.get(imgurl, stream=True).raw)
            img = img.copy()
        except Image.UnidentifiedImageError:
            await ctx.send(embed=discord.Embed(title=translations(guildlang, "error"), description=translations(guildlang, "thisisnotimage"), color=0xFF0000))
            return
        except requests.exceptions.MissingSchema:
            await ctx.send(embed=discord.Embed(title=translations(guildlang, "error"), description=translations(guildlang, "thisisnotimage"), color=0xFF0000))
            return
        pixelsize = 8
        width, height = img.size
        imgSmall = img.resize((round(width/pixelsize), round(height/pixelsize)),resample=Image.BILINEAR)
        result = imgSmall.resize(img.size,Image.NEAREST)
        buffer = io.BytesIO()
        result.save(buffer, format='PNG')
        buffer.seek(0)
        file = discord.File(buffer, "pixelate.png")
        embed = discord.Embed()
        embed.set_image(url="attachment://pixelate.png")

        await ctx.reply(file=file, embed = embed)


    @commands.command(name="ascii")
    async def ascii(self, ctx, *, arg=None):
        guildlang = await aiogetlang(ctx)
        cropped = ""
        if arg is None:
            await ctx.send(
                embed=discord.Embed(color=0x5E924E, title=translations(guildlang, "ErrNotArg")).set_footer(text="ASCII command"))
        else:
            try:
                if detect(arg) == "en":
                    cropped = arg[:30]
                else:
                    cropped = translit(arg, reversed=True)[:30]
            except:
                try:
                    cropped = arg
                except:
                    pass
            razbitoe = [cropped[i:i + 10] for i in range(0, len(cropped), 10)]
            text = "**ASCII**\r\n```"
            for i in razbitoe:
                text = text + art.text2art(i)
            await ctx.send(text + "```")

    @commands.command(name="meme", aliases=["мем", "мемы"])
    @commands.cooldown(1, 7.5, commands.BucketType.user)
    async def meme(self, ctx):
        guildlang = await aiogetlang(ctx)
        if str(guildlang) != "RU":
            memer = await reddit.subreddit("memes")
            meme = await memer.random()
            await ctx.send(embed=discord.Embed(color=0xff9900, title="Meme", url="https://www.reddit.com" + str(meme.permalink), description=str(meme.title)).set_image(url=str(meme.url)))
        else:
            await ctx.send(embed=discord.Embed(color=0xff9900, title="Мем").set_image(url=str(get_photo_max_scale(get_random_post_attachment_no_ads("amfet1")))))

    @commands.command(name="lyrics", aliases=["песня"])
    async def lyrics(self, ctx, *, arg=None):
        guildlang = await aiogetlang(ctx)
        geniuslogo = "https://s3.amazonaws.com/company-photo.theladders.com/52818/1c42e51c-3c2f-41eb-bda1-65b1525284cb.png"
        if arg is None:
            await ctx.send(embed=discord.Embed(title=translations(guildlang, "ErrNotArg")))
        else:
            try:
                test = str()
                async with aiohttp.ClientSession() as ses:
                    async with ses.get("https://some-random-api.ml/lyrics?title=" + "+".join(arg.split())) as r:
                       json_data = await r.json()
                lyricslist = str(json_data["lyrics"]).split("\n")
                for l in range(0, 25):
                    try:
                        test = test + "\r\n" + lyricslist[l]
                    except:
                        pass
                await ctx.send(embed=discord.Embed(color=0xff9900, title=json_data["title"],
                                                   description=json_data["author"]).add_field(
                    name=translations(guildlang, "lyrics"), value="```" + test + "```", inline=False).set_footer(
                    icon_url=geniuslogo, text="Lyrics command"))
            except KeyError:
                await ctx.send(embed=discord.Embed(color=0xff9900, title=translations(guildlang, "error"),
                                                   description="'{0}' {1}".format(arg.capitalize(), translations(guildlang, "notFound")[:-1].lower())).set_footer(
                    icon_url=geniuslogo, text="Lyrics command"))

    @commands.command(name="image", aliases=["пикча", "картинка"])
    async def image(self, ctx, *, arg=None):
        guildlang = await aiogetlang(ctx)
        result = None
        if arg is None:
            async with aiohttp.ClientSession() as ses:
                async with ses.get("https://api.unsplash.com/photos/random?client_id={}".format(unsplashclientid)) as r:
                    r = await r.json()
                    result = r["urls"]["raw"]
            arg = translations(guildlang, "randomimage")
        else:
            try:
                async with aiohttp.ClientSession() as ses:
                    async with ses.get(f"https://pixabay.com/api/?key={pixabayapikey}&q={'+'.join(arg.split())}&image_type=photo") as r:
                        r = await r.json()
                        result = random.choice(r["hits"])["largeImageURL"]
            except ValueError: await ctx.send(embed=discord.Embed(color=0xff9900, title=translations(guildlang, "error"), description=translations(guildlang, "notFound")[:-1]))
        await ctx.send(embed=discord.Embed(color=0xff9900, title=translations(guildlang, "imagetitle"), description=str(arg).capitalize()).set_image(url=result))
    @commands.command(name="owoify", aliases=["owo"])
    async def owoify(self, ctx, *, arg=None):
        if arg is None:
            guildlang = await aiogetlang(ctx)
            await ctx.reply(embed=discord.Embed(title=translations(guildlang, "ErrNotArg")))
        else:
            async with aiohttp.ClientSession() as ses:
                async with ses.get("https://nekos.life/api/v2/owoify?text="+"%20".join(arg.split())[:200]) as r:
                    r = await r.json()
                    await ctx.reply(r["owo"], mention_author=False)
                    await ses.close()

def setup(bot):
    bot.add_cog(FunCog(bot))
