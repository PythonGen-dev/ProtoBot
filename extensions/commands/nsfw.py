from discord.ext import commands
import aiohttp
import io
import random
import discord
import xmltodict
from discord.ext.commands import MemberConverter
import json
from utils.modules import aiogetlang, translations
import asyncpraw

with open("config.json", "r") as configjson:
    configdata = json.load(configjson)
    redditclientid = configdata["redditclientid"]
    redditclientsecret = configdata["redditclientsecret"]
    configjson.close()
reddit = asyncpraw.Reddit(client_id=redditclientid, client_secret=redditclientsecret, user_agent="protobotnsfw")


class NSFWCog(commands.Cog, name="NSFW cog"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="E621")
    @commands.cooldown(1, 3.5, commands.BucketType.user)
    @commands.is_nsfw()
    async def e621(self, ctx, *, arg=None):
        guildlang = await aiogetlang(ctx)
        if arg is None:
            await ctx.reply(embed=discord.Embed(title=translations(guildlang, "ErrNotArg"), color=0x002d56))
        else:
            try:
                e621api="https://e621.net/posts.json?tags={}".format("+".join(arg.split()))
                async with aiohttp.ClientSession(headers={"User-Agent": "pythongen/protobot-1.4"}) as ses:
                    async with ses.get(e621api) as r:
                       r = await r.json()
                posts = r["posts"]
                post = posts[random.randint(0, len(posts)-1)]
                footer = str(translations(guildlang, "tagspron"))+"\r\n"
                for i in ["general", "species", "artist", "character"]:
                    if post["tags"][i] != list(): footer+=translations(guildlang, i+"e621")+": {0}\r\n".format(", ".join(post["tags"][i])+".")
                await ctx.reply(embed=discord.Embed(color=0x002d56).set_image(url=post["file"]["url"]).set_footer(text=footer).set_author(name="E621", icon_url="https://en.wikifur.com/w/images/d/dd/E621Logo.png"), mention_author=False)
            except:
                await ctx.reply(embed=discord.Embed(title=translations(guildlang, "error"), description=translations(guildlang, "notFound")[:-1], color=0x002d56))

    @commands.command(name="gelbooru")
    @commands.cooldown(1, 3.5, commands.BucketType.user)
    @commands.is_nsfw()
    async def gelbooru(self, ctx, *, arg=None):
        guildlang = await aiogetlang(ctx)
        if arg is None:
            await ctx.reply(embed=discord.Embed(title=translations(guildlang, "ErrNotArg")))
        else:
            try:
                api = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags={}".format("+".join(arg.split()))
                async with aiohttp.ClientSession() as session:
                    async with session.get(api) as resp:
                        iodata = json.loads(json.dumps(xmltodict.parse(await resp.text())))
                post = random.choice(iodata["posts"]["post"])
                imageurl = post["@file_url"]
                
                if imageurl.split(".")[-1] in ["mp4", "webm"]:
                    videostring = str()
                    try:
                        source = post["@source"]
                        if source != "":
                            videostring += translations(guildlang, "source")+" <"+source+">\r\n"
                    except: pass
                    videostring += str(imageurl)
                    await ctx.reply(videostring, mention_author=False)
                else:
                    embed = discord.Embed(color=0x167cfc)
                    embed.set_image(url=imageurl)
                    embed.set_author(name="gelbooru", icon_url="https://gelbooru.com/favicon.png")
                    try:
                        tags = post["@tags"]
                        embed.set_footer(text=translations(guildlang, "tagspron") + "\r\n" + tags)
                    except: pass
                    try:
                        source = post["@source"]
                        if source != "":
                            embed.add_field(name = translations(guildlang, "source"), value=source)
                    except: pass
                    await ctx.reply(embed=embed, mention_author=False)
            except IndexError:
                await ctx.reply(embed=discord.Embed(title=translations(guildlang, "error"), description=translations(guildlang, "notFound")[:-1]))

    @commands.command(name="rule34")
    @commands.cooldown(1, 3.5, commands.BucketType.user)
    @commands.is_nsfw()
    async def rule34(self, ctx, *, arg=None):
        guildlang = await aiogetlang(ctx)   
        if arg is None:
            await ctx.reply(embed=discord.Embed(title=translations(guildlang, "ErrNotArg")))
        else:
            try:
                async with aiohttp.ClientSession() as session: 
                    api = "https://rule34.xxx/index.php?page=dapi&s=post&q=index&tags={}".format("+".join(arg.split()))
                    async with session.get(api) as resp:
                        data = json.loads(json.dumps(xmltodict.parse(await resp.text())))
                post = random.choice(data["posts"]["post"])
                imageurl = str(post["@file_url"])
                tags = str(post["@tags"])
                await ctx.reply(embed=discord.Embed(color=0x336633).set_image(url=imageurl).set_footer(text=translations(guildlang, "tagspron") + "\r\n" + tags).set_author(name="rule34", icon_url="https://rule34.xxx/favicon.png"), mention_author=False)
            except:
                await ctx.reply(embed=discord.Embed(title=translations(guildlang, "error"), description=translations(guildlang, "notFound")[:-1]))

    @commands.command(name="neko")
    @commands.cooldown(1, 3.5, commands.BucketType.user)
    @commands.is_nsfw()
    async def neko(self, ctx):
        nekoapi = "https://neko-love.xyz/api/v1/nekolewd"
        async with aiohttp.ClientSession() as ses:
            async with ses.get(nekoapi) as r:
                r = await r.json()
        await ctx.reply(embed=discord.Embed(title="Neko", color = 0xFF00FF).set_image(url=r["url"]), mention_author=False)

    @commands.command(name="yiff")
    @commands.cooldown(1, 3.5, commands.BucketType.user)
    @commands.is_nsfw()
    async def reddityiff(self, ctx):
        yiff = await reddit.subreddit("yiff")
        straight = False
        while straight == False:
            yiffpost = await yiff.random()
            if yiffpost.link_flair_text == "Straight":
                await ctx.send(embed=discord.Embed(color=0xff9900, title="Yiff", url="https://www.reddit.com" + str(yiffpost.permalink)).set_image(url=str(yiffpost.url)))
                return

    @commands.command(name="porngif")
    @commands.cooldown(1, 3.5, commands.BucketType.user)
    @commands.is_nsfw()
    async def porngif(self, ctx):
        porngifsubreddit = await reddit.subreddit("porngifsonly")
        porngifpost = await porngifsubreddit.random()
        await ctx.send(embed=discord.Embed(color=0xff9900, title="Porngif", url="https://www.reddit.com" + str(porngifpost.permalink)).set_image(url=str(porngifpost.url)))

        
def setup(bot):
    bot.add_cog(NSFWCog(bot))
 