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

def filterbots(member):
    return member.bot
    
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

class InfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="userinfo", aliases=['юзер'])
    async def userinfo(self, ctx, userctx=None):
        guildlang = await aiogetlang(ctx)        
        try:
            if not userctx: member = ctx.author
            else: member = await MemberConverter().convert(ctx, userctx)
            try: colors = getcolorfromurl(member.avatar_url)
            except: colors= [0, 191, 255]
            embed = discord.Embed(color=discord.Colour.from_rgb(colors[0], colors[1], colors[2]), title=f"{translations(guildlang, 'infoAbout')} {await self.bot.fetch_user(member.id)}")
            if not member.bot:
                try: userdesc = (await aiopg.aiogetrow("userdescs", [["guildid", ctx.guild.id],["userid", member.id]]))[-1]
                except: userdesc = None
                if userdesc != None:
                    embed.add_field(name=translations(guildlang, 'userdescriptiontitle'), value=userdesc, inline=False)
                elif ctx.author == member:
                    prefix = await self.bot.command_prefix(self.bot, ctx.message)
                    embed.add_field(name=translations(guildlang, 'userdescriptiontitle'), value=translations(guildlang, 'userdescadd') + prefix + 'aboutme`!', inline=False)
                else:
                    embed.add_field(name=translations(guildlang, 'userdescriptiontitle'), value=translations(guildlang, 'userdontadddesc'), inline=False)
            memberroles = ', '.join([role.mention for role in member.roles[1:]])
            if memberroles == "": memberroles =  translations(guildlang, "noroles")
            usercreationdateformat = str(member.created_at.strftime("%d {0} %Y {1}, %H:%M:%S")).format(translations(guildlang, str(member.created_at.strftime("%m")) + 'month'), translations(guildlang, 'year'))
            userjoineddateformat = str(member.joined_at.strftime("%d {0} %Y {1}, %H:%M:%S")).format(translations(guildlang, str(member.joined_at.strftime("%m")) + 'month'),translations(guildlang, 'year'))
            embed.add_field(name=translations(guildlang, "basicInfo"), value=f'⬢** {translations(guildlang, "userInfoUsername")}**\r\n> {member}\r\n⬢** {translations(guildlang, "userinfoJoined")}**\r\n> {userjoineddateformat} ({getmonth(date=member.joined_at, lang=guildlang)})\r\n⬢** {translations(guildlang, "userinfoAccCreated")}**\r\n> {usercreationdateformat} ({getmonth(date=member.created_at, lang=guildlang)})\r\n⬢** {len(member.roles)-1} {translations(guildlang, "norolescount")}**\r\n> {memberroles}')
            for activity in member.activities:
                if isinstance(activity, discord.Spotify):
                    embed.add_field(name = f"{getcustomemote(self, 'spotify', ctx)} Spotify", value = f'> {translations(guildlang, "userStatusSpotify")} **[{activity.title}](https://open.spotify.com/track/{activity.track_id})** ')
                if isinstance(activity, discord.CustomActivity):
                    emoji = activity.emoji
                    if emoji.id is None: displayemoji = emoji.name
                    else:
                        if self.bot.get_emoji(emoji.id) is None: displayemoji = ""
                        else: displayemoji = self.bot.get_emoji(emoji.id)
                    embed.add_field(name = "⬢ "+translations(guildlang, "customactivity"), value = f'> {displayemoji} {activity.name}')
            embed.set_footer(text="ID: " + str(member.id))
            if str(member.avatar_url) != "": embed.set_thumbnail(url=member.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
        except discord.ext.commands.errors.MemberNotFound:
            embed = discord.Embed(title=translations(guildlang, "error"), description=translations(guildlang, "usernotfound"))
            await ctx.reply(embed=embed)



    @commands.command(name="guildinfo", aliases=['сервер', 'serverinfo'])
    async def guildinfo(self, ctx):
        async with ctx.typing():
            guildlang = await aiogetlang(ctx)
            botsinservercount = len(list(filter(lambda x: x.bot == True, ctx.guild.members)))
            try: colors = getcolorfromurl(ctx.guild.icon_url)
            except: colors= [0, 191, 255]
            embed = discord.Embed(color=discord.Colour.from_rgb(colors[0], colors[1], colors[2]), title=ctx.guild.name)
            embed.add_field(name=translations(guildlang, "usersNametag"), value=f"> **{getcustomemote(self, 'allusers', ctx) + translations(guildlang, 'allUsers')}** {ctx.guild.member_count}\r\n > **{getcustomemote(self, 'bot', ctx) + translations(guildlang, 'botUsers')}** {botsinservercount}\r\n > **{getcustomemote(self, 'human', ctx) + translations(guildlang, 'realUsers')}** {ctx.guild.member_count - botsinservercount}", inline=False)
            statusort = "> **"+getcustomemote(self, 'online', ctx)+translations(guildlang, "online")+"**: "+str(len(list(filter(lambda x: x.status == discord.Status.online, ctx.guild.members))))+"\r\n"
            statusort += "> **"+getcustomemote(self, 'idle', ctx)+translations(guildlang, "idle")+"**: "+str(len(list(filter(lambda x: x.status == discord.Status.idle, ctx.guild.members))))+"\r\n"
            statusort += "> **"+getcustomemote(self, 'dnd', ctx)+translations(guildlang, "dnd")+"**: "+str(len(list(filter(lambda x: x.status == discord.Status.dnd, ctx.guild.members))))+"\r\n"
            statusort += "> **"+getcustomemote(self, 'offline', ctx)+translations(guildlang, "offline")+"**: "+str(len(list(filter(lambda x: x.status == discord.Status.offline, ctx.guild.members))))        
            embed.add_field(name=translations(guildlang, "usersstatussort"), value = statusort, inline=False)
            embed.add_field(name=translations(guildlang, "Channels"), value=f"> **{getcustomemote(self, 'AllChannels', ctx) + translations(guildlang, 'allUsers')}** {len(ctx.guild.channels)}\r\n> **{getcustomemote(self, 'VoiceChannels', ctx) + translations(guildlang, 'VoiceChannels')}** {len(ctx.guild.voice_channels)}\r\n> **{getcustomemote(self, 'TextChannels', ctx) + translations(guildlang, 'TextChannels')}** {len(ctx.guild.text_channels)}\r\n> **{getcustomemote(self, 'categorychannels', ctx) + translations(guildlang, 'CategoriesChannels')}** {len(ctx.guild.categories)}", inline=False)
            embed.add_field(name=translations(guildlang, "serverInfoRegion"), value='> ' + getcustomemote(self, str(ctx.guild.region), ctx) + translations(guildlang, str(ctx.guild.region)), inline=False)
            embed.add_field(name=translations(guildlang, "serverInfoOwner"), value='> ' + getcustomemote(self, 'owner', ctx) + str((ctx.guild.owner).mention) +f" (`{ctx.guild.owner}`)", inline=False)
            embed.add_field(name=translations(guildlang, "VerificationLevel"), value='> ' + getcustomemote(self, str(ctx.guild.verification_level), ctx) + translations(guildlang, str(ctx.guild.verification_level)), inline=False)
            creationdateformat = str(ctx.guild.created_at.strftime("%d {0} %Y {1}, %H:%M:%S")).format(translations(guildlang, str(ctx.guild.created_at.strftime("%m")) + 'month'), translations(guildlang, 'year'))
            embed.add_field(name=translations(guildlang, "guildCreationDate"), value='> ' + str(creationdateformat), inline=False)
            if str(ctx.guild.icon_url) != "": embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_footer(text="ID: " + str(ctx.guild.id))
            await ctx.reply(embed=embed, mention_author=False)

def setup(bot):
    bot.add_cog(InfoCog(bot))
