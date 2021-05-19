from discord.ext import commands
import aiohttp
import io
import random
import discord
import utils.aiopg as aiopg
from discord.ext.commands import MemberConverter
import json
from utils.modules import aiogetlang, translations

with open("config.json", "r") as configjson:
    configdata = json.load(configjson)
    srapitoken = configdata["srapitoken"]
cardtemplate = 1

def getlevel(xp, range = 100, difficult=1.1):
    lvl=int()
    while xp>range:
        xp-=range
        lvl+=1
        range=range*difficult
    return int(xp), int(range), lvl

class CanvasCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="card", aliases=['ранг', 'rank'])
    async def card(self, ctx, userctx=None):
        if not userctx: member = ctx.author
        else: member = await MemberConverter().convert(ctx, userctx)
        if not member.bot:
            async with ctx.typing():
                try:
                    userxp = (await aiopg.aiogetrow("userxp", [["guildid", ctx.guild.id],["userid", member.id]]))[-1]
                except: userxp = 0
                xpnow, range, lvl = getlevel(userxp)
                rank = int()
                rankdata = await aiopg.aioorderfetch("userxp", [["guildid", ctx.guild.id]], [["value", "desc"]])
                for row in rankdata:
                    rank+=1
                    if row[-2]==member.id: break
                avatarurl = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(member)
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://some-random-api.ml/premium/rankcard/{cardtemplate}?username={member.name}&rank={rank}&cbg=23272A&cbar=4e5d94&ccxp=7289DA&discriminator={member.discriminator}&cxp={xpnow}&nxp={range}&level={lvl}&avatar={avatarurl}&key={srapitoken}") as resp:
                        buffer = io.BytesIO(await resp.read())
                file = discord.File(buffer, 'card.png')
                embed = discord.Embed(color=0x7289DA)
                embed.set_image(url="attachment://card.png")
                await ctx.reply(file=file, embed = embed, mention_author=False)
        else:
            guildlang = await aiogetlang(ctx)
            await ctx.reply(embed = discord.Embed(color=0xff0000, title=translations(guildlang, "infoAboutBotErr")))


    @commands.command(name="leaders", aliases=['лидеры'])
    async def leaderboard(self, ctx, page=None):
        try:page = int(page)
        except:page = 1
        async with ctx.typing():
            guildlang = await aiogetlang(ctx)
            leaders = await aiopg.aioorderfetch("userxp", [["guildid", ctx.guild.id]], [["value", "desc"]])
            displaylist = leaders.copy()
            if page<1:page=1
            if page>(len(leaders)/10)+1: page = int((len(leaders)/10)+1)
            del displaylist[:(page-1)*10]
            embed = discord.Embed(title=translations(guildlang, "leaderstitle"), color=0x7289DA)
            for fld in displaylist[:10]:
                user = self.bot.get_user(fld[1])
                embed.add_field(name =f"{(leaders.index(fld))+1}. {user}", value = f"{fld[-1]} xp", inline = False)
            embed.set_footer(text=f"{translations(guildlang, 'page')}{int((len(leaders)/10)+1)}")
            await ctx.reply(embed=embed, mention_author = False)




def setup(bot):
    bot.add_cog(CanvasCog(bot))
 
