import json
import random
from glitch_this import ImageGlitcher
import art
import discord
import praw
import requests
from PIL import Image
from discord.ext import commands
from discord.ext.commands import MemberConverter
from langdetect import detect
from transliterate import translit
import modules
import vk_api
from random import randint
from modules import getcolorfromurl, storage, getlang

with open("config.json", "r") as configjson:
    configdata = json.load(configjson)
    unsplashclientid = configdata["unsplashclientid"]
    pixabayapikey = configdata["pixabayapikey"]
    redditclientid = configdata["redditclientid"]
    redditclientsecret = configdata["redditclientsecret"]
    vk_app_id = configdata["vk_app_id"]
    vk_app_token = configdata["vk_app_token"]

    configjson.close()
reddit = praw.Reddit(client_id=redditclientid, client_secret=redditclientsecret, user_agent='protobot',
                     check_for_async=False)
translates = storage("./locals/langs.lang")

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

    @commands.command(name="minecraft")
    async def minecraft(self, ctx, arg=None):
        guildlang = getlang(ctx=ctx)
        footer_image = "https://static.wikia.nocookie.net/minecraft_ru_gamepedia/images/e/e5/%D0%94%D1%91%D1%80%D0%BD.png/revision/latest/scale-to-width-down/160?cb=20200518110227"
        if arg is None:
            await ctx.send(
                embed=discord.Embed(color=0x5E924E, title="Error: No arguments").set_footer(icon_url=footer_image,
                                                                                            text="Minecraft command"))
        else:
            try:
                response = requests.get("https://api.mojang.com/users/profiles/minecraft/" + arg)
                json_data = json.loads(response.text)

                skin = "https://crafatar.com/skins/" + json_data["id"] + "?size=4.png"
                head = "https://crafatar.com/renders/head/" + json_data["id"] + ".png"
                colors = getcolorfromurl(head)
                await ctx.send(embed=discord.Embed(color=discord.Colour.from_rgb(colors[0], colors[1], colors[2]),
                                                   title=translates.get("username" + guildlang) + ' ' + json_data[
                                                       "name"], description="\r\n**UUID:** " + json_data[
                        "id"] + "\r\n\r\n {} ".format(translates.get("skin" + guildlang))).set_thumbnail(
                    url="https://crafatar.com/renders/body/" + json_data["id"] + ".png").set_image(
                    url=skin).set_footer(
                    icon_url=head, text="Minecraft command"))
            except json.JSONDecodeError:
                await ctx.send(embed=discord.Embed(color=0x5E924E, title=translates.get("error" + guildlang),
                                                   description=translates.get("notFound" + guildlang)[:-1]).set_footer(
                    icon_url=footer_image, text="Minecraft command"))
            except:
                await ctx.send(
                    embed=discord.Embed(color=0x5E924E, title=translates.get("randomErr" + guildlang)).set_footer(
                        icon_url=footer_image, text="Minecraft command"))

    @commands.command(name="getemoji")
    async def getemoji(self, ctx, arg: discord.Emoji = None):
        try:
            guildlang = getlang(ctx=ctx)
            if arg is None:
                await ctx.send(embed=discord.Embed(title=translates.get('ErrNotArg' + guildlang)))
            else:
                colors = getcolorfromurl(arg.url)
                if arg.animated:
                    embed = discord.Embed(title=arg.name).set_image(url=arg.url)
                else:
                    embed = discord.Embed(title=arg.name,
                                          color=discord.Colour.from_rgb(colors[0], colors[1], colors[2])).set_image(
                        url=arg.url)
                embed = embed.set_footer(
                    text=translates.get("filesize" + guildlang) + ': ' + requests.get(arg.url, stream=True).headers[
                        'Content-length'])
                await ctx.send(embed=embed)
        except discord.ext.commands.errors.EmojiNotFound:
            embed = discord.Embed(title=translates.get("error" + guildlang),
                                  description=translates.get("notFound" + guildlang)[:-1])
            await ctx.send(embed=embed)
        except AttributeError:
            embed = discord.Embed(title=translates.get("error" + guildlang),
                                  description=translates.get("unkarg" + guildlang))
            await ctx.send(embed=embed)



    @commands.command(name="pixelate")
    async def pixelate(self, ctx, arg=None):
        guildlang = getlang(ctx=ctx)
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
            await ctx.send(embed=discord.Embed(title=translates.get('error' + guildlang), description=translates.get('thisisnotimage' + guildlang), color=0xFF0000))
            return
        except requests.exceptions.MissingSchema:
            await ctx.send(embed=discord.Embed(title=translates.get('error' + guildlang), description=translates.get('thisisnotimage' + guildlang), color=0xFF0000))
            return
        pixelsize = 8
        width, height = img.size
        imgSmall = img.resize((round(width/pixelsize), round(height/pixelsize)),resample=Image.BILINEAR)
        result = imgSmall.resize(img.size,Image.NEAREST)
        
        result.save('./temp/pixelate.png')
        file = discord.File("./temp/pixelate.png")
        
        await ctx.send(file=file)


    @commands.command(name="ascii")
    async def ascii(self, ctx, *, arg=None):
        guildlang = getlang(ctx=ctx)
        cropped = ''
        if arg is None:
            await ctx.send(
                embed=discord.Embed(color=0x5E924E, title=translates.get("ErrNotArg" + guildlang)).set_footer(
                    text="ASCII command"))
        else:
            try:
                if detect(arg) == 'en':
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
            await ctx.send(text + '```')

    @commands.command(name="meme")
    async def meme(self, ctx):
        guildlang = getlang(ctx=ctx)
        if str(guildlang) == "EN":
            meme = reddit.subreddit("memes").random()
            await ctx.send(embed=discord.Embed(color=0xff9900, title="Meme", url='https://www.reddit.com' + str(meme.permalink), description=str(meme.title)).set_image(url=str(meme.url)))
        else:
            await ctx.send(embed=discord.Embed(color=0xff9900, title="Мем").set_image(url=str(get_photo_max_scale(get_random_post_attachment_no_ads("amfet1")))))




    @commands.command(name="glitch")
    async def glitch(self, ctx, arg=None, amount=None):
        guildlang = getlang(ctx=ctx)
        try: amount = float(amount)
        except:
            if amount is None: amount = 5.0
            else:
                await ctx.send(embed=discord.Embed(title=translates.get('error' + guildlang), description=translates.get('glitchvalueerr' + guildlang), color=0xFF0000))
                return
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
            await ctx.send(embed=discord.Embed(title=translates.get('error' + guildlang), description=translates.get('thisisnotimage' + guildlang), color=0xFF0000))
            return
        except requests.exceptions.MissingSchema:
            await ctx.send(embed=discord.Embed(title=translates.get('error' + guildlang), description=translates.get('thisisnotimage' + guildlang), color=0xFF0000))
            return
        try: glitch_img = ImageGlitcher().glitch_image(img, amount, color_offset=True)
        except ValueError:
            await ctx.send(embed=discord.Embed(title=translates.get('error' + guildlang), description=translates.get('glitchvalueerr' + guildlang), color=0xFF0000))
            return
        glitch_img.save('./temp/glitch.png')
        file = discord.File("./temp/glitch.png")
        await ctx.send(file=file)

    @commands.command(name="lyrics")
    async def lyrics(self, ctx, *, arg=None):
        guildlang = getlang(ctx=ctx)
        geniuslogo = 'https://s3.amazonaws.com/company-photo.theladders.com/52818/1c42e51c-3c2f-41eb-bda1-65b1525284cb.png'
        if arg is None:
            await ctx.send(embed=discord.Embed(title=translates.get('ErrNotArg' + guildlang)))
        else:
            try:
                test = ''
                json_data = json.loads(
                    requests.get('https://some-random-api.ml/lyrics?title=' + "+".join(arg.split()), timeout=7).text)
                lyricslist = str(json_data['lyrics']).split('\n')
                for l in range(0, 25):
                    try:
                        test = test + '\r\n' + lyricslist[l]
                    except:
                        pass
                await ctx.send(embed=discord.Embed(color=0xff9900, title=json_data['title'],
                                                   description=json_data['author']).add_field(
                    name=translates.get('lyrics' + guildlang), value='```' + test + '```', inline=False).set_footer(
                    icon_url=geniuslogo, text="Lyrics command"))
            except requests.ReadTimeout:
                await ctx.send(embed=discord.Embed(color=0xff9900, title='Sorry', description='API DEAD :(').set_footer(
                    icon_url=geniuslogo, text="Lyrics command"))
            except KeyError:
                await ctx.send(embed=discord.Embed(color=0xff9900, title=translates.get('error' + guildlang),
                                                   description='"{0}" {1}'.format(arg.capitalize(), translates.get(
                                                       "notFound" + guildlang)[:-1].lower())).set_footer(
                    icon_url=geniuslogo, text="Lyrics command"))

    @commands.command(name="compress")
    async def pix2msch(self, ctx):
        guildlang = getlang(ctx=ctx)
        imgurl = ctx.message.attachments[0].url
        img = Image.open(requests.get(imgurl, stream=True).raw)
        img = img.copy()
        message = await ctx.send("processing")
        img = modules.quantize(img, True, 127)
        img.save("./temp/mschpreview.png")
        await message.edit(content="completed")
        file = discord.File("./temp/mschpreview.png")
        await ctx.send(file=file)

    @commands.command(name="rule34")
    @commands.is_nsfw()
    async def rule34(self, ctx, *, arg=None):
        guildlang = getlang(ctx=ctx)
        
        if arg is None:
            await ctx.send(embed=discord.Embed(title=translates.get('ErrNotArg' + guildlang)))
        else:
            try:
                api = 'https://rule34.xxx/index.php?page=dapi&s=post&q=index&tags={}'.format('+'.join(arg.split()))
                xmldata = requests.get(api).text.split('>')
                post = str(xmldata[random.randint(2, len(xmldata) - 2)]).replace('\r', '').replace('\n', '')[1: -1]
                imageurl = post.split(' ')[3].split('"')[1]
                tags = str(post.split('"')[19])
                await ctx.send(embed=discord.Embed(color=0x336633).set_image(url=imageurl).set_footer(text=translates.get('tagspron' + guildlang) + '\r\n' + tags).set_author(name='rule34', icon_url='https://rule34.xxx/favicon.png'))
                    
            except IndexError:
                await ctx.send(embed=discord.Embed(title=translates.get("error" + guildlang),
                                                       description=translates.get("notFound" + guildlang)[:-1]))
        
    @commands.command(name="image")
    async def image(self, ctx, *, arg=None):
        guildlang = getlang(ctx=ctx)
        result = None
        if arg is None:
            result = 'https://source.unsplash.com/' + str(requests.get(
                'https://api.unsplash.com/photos/random?client_id={}'.format(unsplashclientid)).text.replace('{',
                                                                                                             '').replace(
                '}', '').split(",")[0]).replace('"id":"', '').replace('"', '');
            arg = translates.get('randomimage' + guildlang)
        else:
            try:
                result = requests.get('https://pixabay.com/api/?key=' + pixabayapikey + '&q=' + '+'.join(
                    arg.split()) + '&image_type=photo&per_page=3&page=' + str(random.randint(1, round(int(requests.get(
                    'https://pixabay.com/api/?key=' + pixabayapikey + '&q=' + '+'.join(
                        arg.split()) + '&image_type=photo&per_page=3').text.replace('{', '').replace('}', '').split(
                    ',')[1].replace('"totalHits":', '')) / 3) - 1))).text.split('[')[1].split('{')[
                    random.randint(1, 3)].split('",')[4].split(',')[2].replace('"webformatURL":"', '')
            except ValueError:
                await ctx.send(embed=discord.Embed(color=0xff9900, title=translates.get("error" + guildlang),
                                                   description=translates.get("notFound" + guildlang)[:-1]))
        try:
            await ctx.send(
                embed=discord.Embed(color=0xff9900, title=translates.get('imagetitle' + guildlang),
                                    description=str(arg).capitalize()).set_image(
                    url=result))
        except UnboundLocalError:
            return


def setup(bot):
    bot.add_cog(FunCog(bot))
