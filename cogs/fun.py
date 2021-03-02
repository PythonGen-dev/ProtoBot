import discord
import json
import random
import requests
from discord.ext import commands
from modules import storage

unsplashclientid = 'unsplash client id'
translates = storage("./locals/langs.lang")
langsdb = storage("./database/langsdb.db")


def getlang(ctx):
    try:
        guildlang = langsdb.get(str(ctx.guild.id))
        if guildlang == '0': guildlang = 'EN'
    except:
        guildlang = 'EN'
    return guildlang


class FunCog(commands.Cog, name="Fun module"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="minecraft")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def minecraft(self, ctx, arg=None):
        guildlang = getlang(ctx = ctx)
        footer_image = "https://static.wikia.nocookie.net/minecraft_ru_gamepedia/images/e/e5/%D0%94%D1%91%D1%80%D0%BD.png/revision/latest/scale-to-width-down/160?cb=20200518110227"
        if arg is None:
            await ctx.send(
                embed=discord.Embed(color=0x5E924E, title="Error: No arguments").set_footer(icon_url=footer_image, text="Minecraft command"))
        else:
            try:
                response = requests.get("https://api.mojang.com/users/profiles/minecraft/" + arg)
                json_data = json.loads(response.text)
                await ctx.send(embed=discord.Embed(color=0x5E924E, title=translates.get("username"+guildlang)+' '+json_data["name"], description="\r\n**UUID:** " + json_data["id"] + "\r\n\r\n {} ".format(translates.get("skin"+guildlang))).set_thumbnail(url="https://crafatar.com/renders/body/" + json_data["id"] + ".png").set_image(url="https://crafatar.com/skins/" + json_data["id"] + "?size=4.png").set_footer(icon_url=footer_image, text="Minecraft command"))
            except json.JSONDecodeError: await ctx.send(embed=discord.Embed(color=0x5E924E, title=translates.get("error"+guildlang), description=translates.get("notFound"+guildlang)[:-1]).set_footer(icon_url=footer_image, text="Minecraft command"))
            except: await ctx.send(embed=discord.Embed(color=0x5E924E, title=translates.get("randomErr"+guildlang)).set_footer(icon_url=footer_image, text="Minecraft command"))

    @commands.command(name="ascii")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def ascii(self, ctx, *, arg=None):
        guildlang = getlang(ctx = ctx)
        if arg is None: await ctx.send(embed=discord.Embed(color=0x5E924E, title=translates.get("ErrNotArg"+guildlang)).set_footer(text="ASCII command"))
        else:
            try: response = requests.get("https://artii.herokuapp.com/make?text=" + "+".join(arg[:12].split()), timeout=5); await ctx.send("**ASCII**\r\n```{}```".format(response.text))
            except: await ctx.send(embed=discord.Embed(color=0, title="Random error").set_footer(text="ASCII command"))

    @commands.command(name="meme")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def meme(self, ctx):
        response = requests.get("https://some-random-api.ml/meme")
        json_data = json.loads(response.text)
        await ctx.send(embed=discord.Embed(color=0xff9900, title="Meme", description=json_data["caption"]).set_image(url=json_data["image"]))

    @commands.command(name="lyrics")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def lyrics(self, ctx, *, arg=None):
        geniuslogo = 'https://s3.amazonaws.com/company-photo.theladders.com/52818/1c42e51c-3c2f-41eb-bda1-65b1525284cb.png'
        guildlang = getlang(ctx = ctx)
        try:
            json_data = json.loads(requests.get('https://some-random-api.ml/lyrics?title=' + "+".join(arg.split()), timeout=3).text)
            await ctx.send(embed=discord.Embed(color=0xff9900, title=json_data['title'], description=json_data['author']).add_field(name=translates.get('lyrics'+guildlang), value=json_data['lyrics'][:128], inline=False).set_footer(icon_url=geniuslogo, text="Lyrics command"))
        except requests.ReadTimeout: await ctx.send(embed=discord.Embed(color=0xff9900, title='Sorry', description='API DEAD :(').set_footer(icon_url=geniuslogo, text="Lyrics command"))
        except KeyError: await ctx.send(embed=discord.Embed(color=0xff9900, title=translates.get('error'+guildlang), description='"{0}" {1}'.format(arg.capitalize(), translates.get("notFound"+guildlang)[:-1].lower())).set_footer(icon_url=geniuslogo, text="Lyrics command"))

    @commands.command(name="headsandtails")
    async def headsandtails(self, ctx):
        randomint = str(random.choice(['Tails', 'Heads']))
        await ctx.send(embed=discord.Embed(color=0xff9900, title=randomint))

    @commands.command(name="image")
    async def image(self, ctx, *, arg=None):
        result = None
        if arg is None:
            result = str(requests.get('https://api.unsplash.com/photos/random?client_id={}'.format(unsplashclientid)).text.replace('{', '').replace('}', '').split(",")[0]).replace('"id":"', '').replace('"', ''); arg = 'Random'
        else:
            try:
                result = str(requests.get('https://api.unsplash.com/search/photos?query={1}&page={2}&per_page=1&client_id={0}'.format(unsplashclientid, arg, random.randint(1, int(str(requests.get('https://api.unsplash.com/search/photos?query={1}&per_page=1&client_id={0}'.format(unsplashclientid, arg)).text).replace('{', '').replace('}', '').split(",")[0].replace('"total":', ''))))).text.split(",")[2]).replace('"results":[{"id":"', '').replace('"', '')
            except ValueError:
                await ctx.send(embed=discord.Embed(color=0xff9900, title="Error", description='Not found').set_thumbnail(url='https://libapps-au.s3-ap-southeast-2.amazonaws.com/accounts/22196/images/UNSPLASH-NOW.png'))
        try:
            await ctx.send(embed=discord.Embed(color=0xff9900, title="Image", description=str(arg).capitalize()).set_image(url='https://source.unsplash.com/'+result).set_thumbnail(url='https://libapps-au.s3-ap-southeast-2.amazonaws.com/accounts/22196/images/UNSPLASH-NOW.png'))
        except UnboundLocalError: return


def setup(bot):
    bot.add_cog(FunCog(bot))
