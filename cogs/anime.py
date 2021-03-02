import discord
from discord.ext import commands
import requests
import json
import random
from modules import storage
translates = storage("./locals/langs.lang")
langsdb = storage("./database/langsdb.db")

def getlang(ctx):
    try:
        guildlang = langsdb.get(str(ctx.guild.id))
        if guildlang == '0': guildlang = 'EN'
    except:
        guildlang = 'EN'
    return guildlang


winklist = ['https://i.pinimg.com/originals/1a/3e/80/1a3e80b2d8b08e39d3a7355dc23a88db.gif',
            'https://thumbs.gfycat.com/TinySoftApe-small.gif',
            'https://media.tenor.com/images/03519b3a7338e728afab670f71202000/tenor.gif',
            'https://media1.giphy.com/media/ErZ8hv5eO92JW/200.gif',
            'https://data.whicdn.com/images/43924273/original.gif',
            'https://i.kym-cdn.com/photos/images/newsfeed/001/144/366/74e.gif',
            'https://data.whicdn.com/images/244721484/original.gif',
            'https://thumbs.gfycat.com/ElegantFixedGermanpinscher-size_restricted.gif',
            'https://i.pinimg.com/originals/03/a0/1b/03a01bea6b5af2fb478ec1a1bc551ec5.gif',
            'https://media1.tenor.com/images/7e7d7a6a6084c741804e29b6c46b1b5d/tenor.gif?itemid=12003936',
            'https://media1.tenor.com/images/1a1032f8d931626a1a2c98df904f0b84/tenor.gif?itemid=5373683',
            'https://media1.tenor.com/images/db862a20099cefcde250c816172ec9a9/tenor.gif?itemid=6372984',
            'https://thumbs.gfycat.com/CavernousAbleGallinule-small.gif',
            'https://thumbs.gfycat.com/IcyConstantFly-small.gif',
            'https://media1.tenor.com/images/e3471fed7bef8f7b737b5ffa0204feb5/tenor.gif?itemid=16242471',
            'https://media1.tenor.com/images/208d8b368122334e627d3bd0f0aafa65/tenor.gif?itemid=18441165']
patlist = ['https://media.tenor.com/images/ad8357e58d35c1d63b570ab7e587f212/tenor.gif',
           'https://i.gifer.com/origin/a6/a68b167d7e9c8a47df7720a2cda1adfe.gif',
           'https://pa1.narvii.com/6847/b1fe3eb0240f8f1b0ca0f8b6d1fe3752c5988d1e_hq.gif',
           'https://media1.tenor.com/images/c0bcaeaa785a6bdf1fae82ecac65d0cc/tenor.gif?itemid=7453915',
           'https://thumbs.gfycat.com/ParchedBlueIberianmole-size_restricted.gif',
           'https://i.pinimg.com/originals/d7/c3/26/d7c326bd43776f1e0df6f63956230eb4.gif',
           'https://cdn.discordapp.com/emojis/678297046020784180.gif?v=1',
           'https://thumbs.gfycat.com/TautInformalIndianjackal-small.gif',
           'https://thumbs.gfycat.com/SpottedBothJellyfish.webp',
           'https://media1.tenor.com/images/0444a1b1e7af31dde95dc67c44c18ce7/tenor.gif?itemid=14368378']
huglist = ['https://i.pinimg.com/originals/06/dd/8f/06dd8f976b7353d69aec173b44927ef4.gif',
           'https://i.imgur.com/r9aU2xv.gif?noredirect',
           'https://37.media.tumblr.com/f2a878657add13aa09a5e089378ec43d/tumblr_n5uovjOi931tp7433o1_500.gif',
           'https://media1.tenor.com/images/684efd91473dcfab34cb78bf16d211cf/tenor.gif?itemid=14495459',
           'https://i.imgur.com/VgP2ONn.gif',
           'https://media.tenor.com/images/2e1d34d002d73459b6119d57e6a795d6/tenor.gif',
           'https://cutewallpaper.org/21/anime-sad-hug/Anime-sad-hug-gif-12-At-GIF-Images-Download.gif',
           'https://cdn.lowgif.com/small/66af32a828a3fa7d-.gif',
           'https://cutewallpaper.org/21/hugs-anime/Hugs-for-everyone-3-image-Anime-Fans-of-DBolical-Indie-DB.gif',
           'https://media1.giphy.com/media/ArLxZ4PebH2Ug/200.gif', ]
facepalmlist = ['https://media1.tenor.com/images/bc3f3842afb1edcba095f9bf766405b2/tenor.gif?itemid=17778269',
                'https://media.tenor.com/images/1ca66a8af2d5177b032a81e291b79643/tenor.gif',
                'https://i.pinimg.com/originals/8d/22/4f/8d224fe698e128391249e3f31814b38d.gif',
                'https://media.tenor.com/images/4b4c46f0a4fdb4fc6ce484a8d441fa53/tenor.gif',
                'https://i.pinimg.com/originals/07/e8/9d/07e89dca8975361314ef38f719037892.gif',
                'https://i.pinimg.com/originals/46/5c/34/465c344e842fe1705fa88211a60b3134.gif',
                'https://gif-finder.com/wp-content/uploads/2016/02/Death-Note-Light-Yagami-Facepalm-Reaction.gif',
                'https://media3.giphy.com/media/h1QqXaLZ9KPW9dQhZ6/giphy.gif?cid=6c09b95240c803f3ff5ae23568d79369140e58b9c6ee523d&rid=giphy.gif']
sadlist = ['https://media1.tenor.com/images/253ecf34e5a1824cca18cd76ab675d34/tenor.gif?itemid=17647487',
           'https://i.pinimg.com/originals/73/b1/3b/73b13bcd2590cd93ca1ca9bbc7f917be.gif',
           'https://media1.tenor.com/images/d10e89407f0a5e6974b22a07a963e85f/tenor.gif?itemid=17647481',
           'https://media0.giphy.com/media/EcVASV8cplvj2/giphy.gif',
           'https://i.pinimg.com/originals/58/bd/4b/58bd4babf343b6d99c459845bb544fc2.gif',
           'https://media1.tenor.com/images/2bd485a5d2b8600a78ca0b82adbb2dde/tenor.gif?itemid=16156194',
           'https://i.imgur.com/OLSFcu5.gif',
           'http://33.media.tumblr.com/b123fbe52d558bac539dd9c46b0c958b/tumblr_mesbg2Txy71rt8ohzo1_500.gif', ]


class AnimeCog(commands.Cog, name="anime cog"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="facepalm")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def facepalm(self, ctx):
        guildlang = getlang(ctx = ctx)
        embed = discord.Embed(color=0xff9900, title=translates.get('facepalm'+guildlang))
        embed.set_image(url=random.choice(facepalmlist))
        await ctx.send(embed=embed)

    @commands.command(name="hug")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def hug(self, ctx):
        guildlang = getlang(ctx = ctx)
        embed = discord.Embed(color=0xff9900, title=translates.get('hug'+guildlang))
        embed.set_image(url=random.choice(huglist))
        await ctx.send(embed=embed)

    @commands.command(name="wink")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def wink(self, ctx):
        guildlang = getlang(ctx = ctx)
        embed = discord.Embed(color=0xff9900, title=translates.get('wink'+guildlang))
        embed.set_image(url=random.choice(winklist))
        await ctx.send(embed=embed)

    @commands.command(name="pat")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def pat(self, ctx):
        guildlang = getlang(ctx = ctx)
        embed = discord.Embed(color=0xff9900, title=translates.get('pat'+guildlang))
        embed.set_image(url=random.choice(patlist))
        await ctx.send(embed=embed)

    @commands.command(name="sad")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def sad(self, ctx):
        guildlang = getlang(ctx = ctx)
        embed = discord.Embed(color=0xff9900, title=translates.get('sad'+guildlang))
        embed.set_image(url=random.choice(sadlist))
        await ctx.send(embed=embed)

    @commands.command(name="quote")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def quote(self, ctx):
        guildlang = getlang(ctx = ctx)
        response = requests.get('https://some-random-api.ml/animu/quote', timeout=5)
        json_data = json.loads(response.text)
        embed = discord.Embed(color=0xff9900, title=json_data['anime'] + ' ' + translates.get('quote'+guildlang).casefold(),
                              description=translates.get('characther'+guildlang)+' '+json_data['characther'])
        embed.add_field(name=translates.get('quote'+guildlang), value=json_data['sentence'], inline=False, )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(AnimeCog(bot))
