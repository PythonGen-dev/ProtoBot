from discord.ext import commands
import discord, aiohttp
import utils.aiopg as aiopg

class member_event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        try:
            guildid, channelid, text = await aiopg.aiogetrow("goodbye", [["guildid", guild.id]])
        except: return
        channel = self.bot.get_channel(channelid)
        text = text.replace("{{member.mention}}", member.mention)
        text = text.replace("{{member.name}}", str(member.name))
        text = text.replace("{{member.discriminator}}", str(member.discriminator))
        text = text.replace("{{member.id}}", str(member.id))
        text = text.replace("{{guild.name}}", str(guild.name))
        embed = discord.Embed(description=text, color=0xFF0000)
        embed = embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=guild.name, icon_url = guild.icon_url)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        try:
            guildid, channelid, text = await aiopg.aiogetrow("welcome", [["guildid", guild.id]])
        except: return
        channel = self.bot.get_channel(channelid)
        text = text.replace("{{member.mention}}", member.mention)
        text = text.replace("{{member.name}}", str(member.name))
        text = text.replace("{{member.discriminator}}", str(member.discriminator))
        text = text.replace("{{member.id}}", str(member.id))
        text = text.replace("{{guild.name}}", str(guild.name))
        embed = discord.Embed(description=text, color=0x00FF00)
        embed = embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=guild.name, icon_url = guild.icon_url)
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(member_event(bot))