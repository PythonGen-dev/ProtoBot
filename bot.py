# -*- coding: utf8 -*-
import discord
from discord.ext import commands
from asyncio import sleep
import json
import pandas as pd
import sys
import requests
from random import randrange
import languagefile
import configfile
import images
from discord.ext.commands import has_permissions, MissingPermissions
from discord import Embed
from discord.ext.commands import Bot
import asyncio
import wikifur
from skingrabber import skingrabber
from random import randint
from datetime import datetime
import random
from db import database
languagesdatabase = database("./langsdb.db")
cookiesdatabase = database("./cookiesdb.db")
imagesdatabase = database("./imagesdb.db")

bot = commands.AutoShardedBot(command_prefix=configfile.settings['prefix'], case_insensitive=True, intents = discord.Intents.all())
client = discord.Client()
current_language = "en"
bot.remove_command('help')
@bot.event
async def on_ready():
    print("  /¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|\r\n ",'|                                                                                    |\r\n ','|                     ((@@@@//                        //%@@@@@((                     |\r\n ','|                (@@@@%.     (&&&&@@@@@@@@@@@@@@@@@@&&&#    .*@@@@@@&                |\r\n ','|           ,/@@@&& ,,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,. %@@@@@,.           |\r\n ','|          #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@/          |\r\n ','|         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&         |\r\n ','|        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%        |\r\n ','|       #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@/       |\r\n ','|      *@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.      |\r\n ','|     .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.     |\r\n ','|    ,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&,    |\r\n ','|    #@@@@@@@@@@@@@@@@@@@@(,    .,@@@@@@@@@@@@@@@@@@,.   ,/@@@@@@@@@@@@@@@@@@@@@/    |\r\n ','|   *@@@@@@@@@@@@@@@@@@@            @@@@@@@@@@@@@#           @@@@@@@@@@@@@@@@@@@@.   |\r\n ','|   @@@@@@@@@@@@@@@@@@&,             @@@@@@@@@@@              (@@@@@@@@@@@@@@@@@@@   |\r\n ','|   @@@@@@@@@@@@@@@@@@%              @@@@@@@@@@@              (@@@@@@@@@@@@@@@@@@@   |\r\n ','|  @@@@@@@@@@@@@@@@@@@@*             @@@@@@@@@@@@            ,@@@@@@@@@@@@@@@@@@@@%  |\r\n ','|  @@@@@@@@@@@@@@@@@@@@@@,        .%@@@@@@@@@@@@@@#         @@@@@@@@@@@@@@@@@@@@@@%  |\r\n ','| #@@@@@@@@@@@@@@@@@@@@@@@@@@##%@@@@@@@@@@@@@@@@@@@@@&###@@@@@@@@@@@@@@@@@@@@@@@@@@/ |\r\n ','| #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@/ |\r\n ','| #@@@@@@@@@@@@@@( ,#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&# %@@@@@@@@@@@@@@/ |\r\n ','|  *@@@@@@@@@@@@@@@@%    **@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#*,  .#@@@@@@@@@@@@@@@@,  |\r\n ','|     @@@@@@@@@@@@@@@@@@@#           @@@@@@@@@@@@@/          @@@@@@@@@@@@@@@@@@%     |\r\n ','|        %@@@@@@@@@@@@@@@@&                               .&@@@@@@@@@@@@@@@@(        |\r\n ','|            .**@@@@@@@@/                                    @@@@@@@@@**             |\r\n ','|                                                                                    |\r\n ','|                                                                                    |\r\n ',"|        ██████╗ ██████╗  ██████╗ ████████╗ ██████╗ ██████╗  ██████╗ ████████╗       |\r\n ","|        ██╔══██╗██╔══██╗██╔═══██╗╚══██╔══╝██╔═══██╗██╔══██╗██╔═══██╗╚══██╔══╝       |\r\n ","|        ██████╔╝██████╔╝██║   ██║   ██║   ██║   ██║██████╔╝██║   ██║   ██║          |\r\n ","|        ██╔═══╝ ██╔══██╗██║   ██║   ██║   ██║   ██║██╔══██╗██║   ██║   ██║          |\r\n ","|        ██║     ██║  ██║╚██████╔╝   ██║   ╚██████╔╝██████╔╝╚██████╔╝   ██║          |\r\n ","|        ╚═╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝          |\r\n ","|                                                                                    |\r\n ","|____________________________________________________________________________________/ ")
    print (configfile.logging['start'])   
    print (configfile.logging['atCenter'] + str(datetime.now()) + configfile.logging['info'] + "Launch: {}".format("Successful"))
    print (configfile.logging['atCenter'] + str(datetime.now()) + configfile.logging['info'] + "Bot name: {}".format(bot.user.name))
    print (configfile.logging['end'])
    while True:
          await bot.change_presence(status=discord.Status.online, activity=discord.Game("with you"))
          await sleep(15)
          await bot.change_presence(activity=discord.Streaming(name='bot prefix is: ' + configfile.settings['prefix'], url="https://media1.tenor.com/images/a97f3da82d52fc4cf66bd3eb425fd6c6/tenor.gif?itemid=18256940"))
          await sleep(15)
def openjson(guildID):
    try:
        lang = languagesdatabase.get(guildID)
    except:
        lang = configfile.settings['defaultlang']
    return lang
@bot.event
async def on_guild_join(guild):
    languagesdatabase.set(str(guild.id) , configfile.settings['defaultlang'])
intervals = (('weeks', 604800),('days', 86400),('hours', 3600),('minutes', 60),('seconds', 1))
def display_time(seconds, granularity=2):
    result = []
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])
@bot.command(pass_context=True)
async def wikifur_search(ctx):
    logInfo(commandname= 'wikifur_search', user = str(ctx.message.author.name), userid = str(ctx.author.id), guildID = str(ctx.message.guild.id))
    lang = openjson(guildID = str(ctx.message.guild.id))
    global current_language
    msg = ctx.message.content.split(" ")
    request = msg[2:]
    request = " ".join(request)
    error = None
    try:
        wikifurcontent = wikifur.search(request, results=20, suggestion=False)
        if not wikifurcontent:
            wikifurcontent = languagefile.languagepy['NoSearchresults'+lang] + request
            embed = discord.Embed(title=languagefile.languagepy['wikiFsearchresults'+lang], color=0xe74c3c, description=wikifurcontent)
            embed.set_thumbnail(url=configfile.wikifur_config['imageURL'])
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=languagefile.languagepy['wikiFsearchresults'+lang], color=discord.Colour.from_rgb(67, 69, 156), description="\n".join(wikifurcontent))
            embed.set_thumbnail(url=configfile.wikifur_config['imageURL'])
            await ctx.send(embed=embed)
    except Exception as error:
        error = str(error)
        await ctx.send(languagefile.languagepy['randomErr'+lang])
        logError(commandname= 'wikifur_search', user = str(ctx.message.author.name), userid = str(ctx.author.id), guildID = str(ctx.message.guild.id), error=error)
@bot.command(pass_context=True)
async def help(ctx, arg: str = None, arg2: str = None):
    logInfo(commandname= 'help', user = str(ctx.message.author.name), userid = str(ctx.author.id), guildID = str(ctx.message.guild.id))
    lang = openjson(guildID = str(ctx.message.guild.id))
    if not arg:
        embed = discord.Embed(color = 0xff9900, title = bot.user.name + languagefile.languagepy['commands'+lang], description = languagefile.languagepy['categories'+lang])
        embed.set_thumbnail(url = bot.user.avatar_url)
        embed.add_field(name=configfile.emojis['paw'] + languagefile.languagepy['wikifurMenu'+lang] + configfile.emojis['paw'], value= languagefile.languagepy['wikifurMenudesc'+lang]+ "``` " + configfile.settings['prefix']+ "help wikifur" + "```", inline=True,)
        embed.add_field(name=configfile.emojis['fun'] + languagefile.languagepy['funMenu'+lang] + configfile.emojis['fun'],value=languagefile.languagepy['funMenuDesc'+lang]+ "``` " + configfile.settings['prefix']+ "help fun" + "```",inline=True,)
        embed.add_field(name=configfile.emojis['mod'] + languagefile.languagepy['settingsMenu'+lang],value=languagefile.languagepy['settingsMenuDesc'+lang]+ "``` " + configfile.settings['prefix']+ "help settings" + "```",inline=True,)
        await ctx.send(embed = embed)
    if not arg2:
        if arg == "wikifur":
            embed = discord.Embed(color = 0x43459C, title = bot.user.name + languagefile.languagepy['commands'+lang], description = languagefile.languagepy['wikifurcommands'+lang] )
            embed.set_thumbnail(url = bot.user.avatar_url)
            embed.add_field(name=configfile.settings['prefix'] + "wikifur_display", value=languagefile.languagepy['wikifurDisplayInfo'+lang], inline=True,)
            embed.add_field(name=configfile.settings['prefix'] + "wikifur_search", value=languagefile.languagepy['wikifurSearchInfo'+lang], inline=True,)
            await ctx.send(embed = embed)
        else:
            if arg == "fun":
                embed = discord.Embed(color = 0xff9900, title = bot.user.name + languagefile.languagepy['commands'+lang], description = languagefile.languagepy['funcommands'+lang] )
                embed.set_thumbnail(url = bot.user.avatar_url)
                embed.add_field(name=configfile.settings['prefix'] + "help fun anime", value=languagefile.languagepy['helpfunanime'+lang], inline=True,)
                embed.add_field(name=configfile.settings['prefix'] + "help fun others", value=languagefile.languagepy['helpfunothers'+lang], inline=True,)
                await ctx.send(embed = embed)
            else:
                if arg == "utilities":
                    embed = discord.Embed(color = 0xff9900, title = bot.user.name + languagefile.languagepy['commands'+lang], description = languagefile.languagepy['settingscommands'+lang] )
                    embed.set_thumbnail(url = bot.user.avatar_url)
                    embed.add_field(name=configfile.settings['prefix'] + "setlang <ru/en>", value=languagefile.languagepy['setlang'+lang], inline=False,)
                    embed.add_field(name=configfile.settings['prefix'] + "about", value=languagefile.languagepy['aboutcommand'+lang], inline=False,)
                    embed.add_field(name=configfile.settings['prefix'] + "userinfo", value=languagefile.languagepy['userinfohelp'+lang], inline=False,)
                    embed.add_field(name=configfile.settings['prefix'] + "avatar", value=languagefile.languagepy['avatarhelp'+lang], inline=False,)
                    embed.add_field(name=configfile.settings['prefix'] + "guildinfo", value=languagefile.languagepy['guildinfohelp'+lang], inline=False,)
                    await ctx.send(embed = embed)
    else:
        if arg == "fun" and arg2 == "others":
            embed = discord.Embed(color = 0xff9900, title = bot.user.name + languagefile.languagepy['commands'+lang], description = languagefile.languagepy['funcommands'+lang] )
            embed.set_thumbnail(url = bot.user.avatar_url)
            embed.add_field(name=configfile.settings['prefix'] + "meme", value=languagefile.languagepy['othersMeme'+lang], inline=False,)
            embed.add_field(name=configfile.settings['prefix'] + "lyrics", value=languagefile.languagepy['othersLyrics'+lang], inline=False,)
            embed.add_field(name=configfile.settings['prefix'] + "boop", value="```OWO```", inline=False,)
            embed.add_field(name=configfile.settings['prefix'] + "minecraft_user <username>", value=languagefile.languagepy['othersMinecraft'+lang], inline=False,)
            await ctx.send(embed = embed)
        else:
            if arg == "fun" and arg2 == "anime":
                embed = discord.Embed(color = 0xff9900, title = bot.user.name + languagefile.languagepy['commands'+lang], description = languagefile.languagepy['funcommands'+lang] )
                embed.add_field(name=configfile.settings['prefix'] + "wink", value=languagefile.languagepy['animewink'+lang], inline=True,)
                embed.set_thumbnail(url = bot.user.avatar_url)
                embed.add_field(name=configfile.settings['prefix'] + "pat", value=languagefile.languagepy['animepet'+lang], inline=True,)
                embed.add_field(name=configfile.settings['prefix'] + "hug", value=languagefile.languagepy['animehug'+lang], inline=True,)
                embed.add_field(name=configfile.settings['prefix'] + "face-palm", value=languagefile.languagepy['animefacepalm'+lang], inline=True,) 
                embed.add_field(name=configfile.settings['prefix'] + "sad", value=languagefile.languagepy['animesad'+lang], inline=True,) 
                embed.add_field(name=configfile.settings['prefix'] + "quote", value=languagefile.languagepy['animequote'+lang], inline=True,) 
                await ctx.send(embed = embed)
@bot.command(pass_context=False)
async def wikifur_display(ctx):
    lang = openjson(guildID = str(ctx.message.guild.id))
    logInfo(commandname= 'wikifur_display', user = str(ctx.message.author.name), userid = str(ctx.author.id), guildID = str(ctx.message.guild.id))
    msg = ctx.message.content.split(" ")
    request = msg[2:]
    request = " ".join(request)
    try:
        pagecontent = wikifur.page(request)
        pagetext = wikifur.summary(request, sentences=5)
        embed = discord.Embed(title=request, color=discord.Colour.from_rgb(67, 69, 156), description=pagetext + "\n\n" + languagefile.languagepy['readFurther'+lang] + "({})".format(pagecontent.url))
        try:
            thumbnail = pagecontent.images[randint(0, len(pagecontent.images))]
            embed.set_image(url=thumbnail),
        except:
            thumbnailno = configfile.wikifur_config['imageURL']
            embed.set_thumbnail(url=thumbnailno),
        await ctx.send(embed=embed)
    except wikifur.DisambiguationError:
        NotSpecificRequestErrorMessage = languagefile.languagepy['NotSpecificRequestErrorMessage'+lang]
        embed = discord.Embed(title=languagefile.languagepy['badRequest'+lang], color=0xe74c3c, description=NotSpecificRequestErrorMessage)
        embed.set_thumbnail(url=configfile.wikifur_config['imageURL'])
        logWarn(commandname= 'wikifur_display', user = str(ctx.message.author.name), userid = str(ctx.author.id), guildID = str(ctx.message.guild.id), warn='Not Specific Request Error Message')
        await ctx.send(embed=embed)
    except wikifur.PageError:
        NoResultErrorMessage = languagefile.languagepy['NoResultErrorMessage'+lang]
        embed = discord.Embed(title=languagefile.languagepy['notFound'+lang], color=0xe74c3c, description=NoResultErrorMessage)
        embed.set_thumbnail(url=configfile.wikifur_config['imageURL'])
        logWarn(commandname= 'wikifur_display', user = str(ctx.message.author.name), userid = str(ctx.author.id), guildID = str(ctx.message.guild.id), warn='NoResultErrorMessage')
        await ctx.send(embed=embed)
    except:
        RandomErrorMessage = languagefile.languagepy['randomErr'+lang]
        embed = discord.Embed(title=languagefile.languagepy['error'+lang], color=0xe74c3c, description=RandomErrorMessage)
        embed.set_thumbnail(url=configfile.wikifur_config['imageURL'])
        logWarn(commandname= 'wikifur_display', user = str(ctx.message.author.name), userid = str(ctx.author.id), guildID = str(ctx.message.guild.id))
        await ctx.send(embed=embed)
@bot.command()
async def wink(ctx):
    lang = openjson(guildID = str(ctx.message.guild.id))
    embed = discord.Embed(color = 0xff9900, title = languagefile.languagepy['wink'+lang], description = "" )
    embed.set_image(url = random.choice(images.winklist))
    await ctx.send(embed = embed)
    logInfo(commandname= 'wink', user = str(ctx.message.author.name), userid = str(ctx.author.id), guildID = str(ctx.message.guild.id))
@bot.command()
async def pat(ctx):
    lang = openjson(guildID = str(ctx.message.guild.id))
    embed = discord.Embed(color = 0xff9900, title = languagefile.languagepy['pat'+lang], description = "" )
    embed.set_image(url = random.choice(images.patlist))
    logInfo(commandname= 'pat', user = str(ctx.message.author.name), userid = str(ctx.author.id), guildID = str(ctx.message.guild.id))
    await ctx.send(embed = embed)
@bot.command()
@commands.cooldown(1, 3600, commands.BucketType.user)
async def make_cookie(ctx):
    random = randrange(10)
    lang = openjson(guildID = str(ctx.message.guild.id))
    cookiesadd = int(cookiesdatabase.get(str(ctx.message.author.id))) + random
    cookiesdatabase.set(str(ctx.message.author.id), str(cookiesadd))
    embed = discord.Embed(color = 0xff9900, title = languagefile.languagepy['cookies'+lang], description = languagefile.languagepy['cookiesPlus'+lang] + str(random) + languagefile.languagepy['cookiestwo'+lang] )
    embed.set_footer(text=str(ctx.message.author.id))
    await ctx.send(embed = embed)
@make_cookie.error
async def make_cookie_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        seconds = int(error.retry_after)
        msg = 'This command is ratelimited, please try again in ' + str(display_time(seconds=seconds))
        await ctx.send(msg)
    else:
        raise error
@bot.command()
async def my_cookies(ctx):
    lang = openjson(guildID = str(ctx.message.guild.id))
    embed = discord.Embed(color = 0xff9900, title = languagefile.languagepy['cookies'+lang], description = str(cookiesdatabase.get(str(ctx.message.author.id))) + ' :cookie:')
    embed.set_footer(text=str(ctx.message.author.id))
    await ctx.send(embed = embed)
@bot.command()
async def hug(ctx):
    lang = openjson(guildID = str(ctx.message.guild.id))
    embed = discord.Embed(color = 0xff9900, title = languagefile.languagepy['hug'+lang], description = "" )
    embed.set_image(url = random.choice(images.huglist))
    logInfo(commandname= 'hug', user = str(ctx.message.author.name), userid = str(ctx.author.id), guildID = str(ctx.message.guild.id))
    await ctx.send(embed = embed)
@bot.command()
async def sad(ctx):
    lang = openjson(guildID = str(ctx.message.guild.id))
    embed = discord.Embed(color = 0xff9900, title = languagefile.languagepy['sad'+lang], description = "" )
    embed.set_image(url = random.choice(images.sadlist))
    logInfo(commandname= 'sad', user = str(ctx.message.author.name), userid = str(ctx.author.id), guildID = str(ctx.message.guild.id))
    await ctx.send(embed = embed)
@bot.command()
async def facepalm(ctx):
    lang = openjson(guildID = str(ctx.message.guild.id))
    logInfo(commandname= 'facepalm', user = str(ctx.message.author.name), userid = str(ctx.author.id), guildID = str(ctx.message.guild.id))
    embed = discord.Embed(color = 0xff9900, title = languagefile.languagepy['facepalm'+lang], description = "" )
    embed.set_image(url = random.choice(images.facepalmlist))
    await ctx.send(embed = embed) 
@bot.command()
async def quote(ctx):
    lang = openjson(guildID = str(ctx.message.guild.id))
    response = requests.get('https://some-random-api.ml/animu/quote')
    json_data = json.loads(response.text)
    logInfo(commandname= 'quote', user = str(ctx.message.author.name), userid = str(ctx.author.id), guildID = str(ctx.message.guild.id))
    embed = discord.Embed(color = 0xff9900, title = json_data['anime'] + languagefile.languagepy['quote'+lang], description = languagefile.languagepy['characther'+lang] + json_data['characther'])
    embed.add_field(name=languagefile.languagepy['quote'+lang], value=json_data['sentence'], inline=False,)
    await ctx.send(embed = embed)    
@bot.command(pass_context=True)
async def image(ctx, arg: str = None, arg2: str = ""):
    lang = openjson(guildID = str(ctx.message.guild.id))
    logInfo(commandname= 'image', user = str(ctx.message.author.name), userid = str(ctx.author.id), guildID = str(ctx.message.guild.id))
    response = 1
    tofind = arg + arg2
    try:
        response = imagesdatabase.get(str(tofind) + str(random.randint(1, int(imagesdatabase.get(tofind + 'lenght')))))
    except:
        embed = discord.Embed(color = 0, title = languagefile.languagepy['unkarg' + lang], description = languagefile.languagepy['listofavalible' + lang] )
        embed.add_field(name="--------------------", value=configfile.settings['prefix'] + "image dog", inline=False,)
        embed.add_field(name="--------------------", value=configfile.settings['prefix'] + "image cat", inline=False,)
        embed.add_field(name="--------------------", value=configfile.settings['prefix'] + "image panda", inline=False,)
        embed.add_field(name="--------------------", value=configfile.settings['prefix'] + "image fox", inline=False,)
        embed.add_field(name="--------------------", value=configfile.settings['prefix'] + "image red panda", inline=False,)
        embed.add_field(name="--------------------", value=configfile.settings['prefix'] + "image koala", inline=False,)
        embed.add_field(name="--------------------", value=configfile.settings['prefix'] + "image bird", inline=False,)
        embed.add_field(name="--------------------", value=configfile.settings['prefix'] + "image racoon", inline=False,)
        embed.add_field(name="--------------------", value=configfile.settings['prefix'] + "image whale", inline=False,)
        embed.add_field(name="--------------------", value=configfile.settings['prefix'] + "image pikachu", inline=False,)
        embed.set_thumbnail(url=configfile.settings['errorIMG'])
        await ctx.send(embed = embed)
    if response != 1:
        if arg2 == None:
            embed = discord.Embed(color = 0xff9900, title = arg, description = "" )
        else:
            embed = discord.Embed(color = 0xff9900, title = arg + " " +  arg2, description = "" )
        embed.set_image(url = response)
        await ctx.send(embed = embed)
@bot.command()
async def lyrics(ctx, *, args):
    lang = openjson(guildID = str(ctx.message.guild.id))
    response = requests.get('https://some-random-api.ml/lyrics?title=' + args)
    json_data = json.loads(response.text)
    lyricstext = json_data['lyrics'][:256]
    embed = discord.Embed(color = 0xff9900, title = json_data['title'], description = json_data['author'] )
    embed.add_field(name=languagefile.languagepy['lyrics' + lang], value=lyricstext, inline=False,)
    await ctx.send(embed = embed)
@bot.command(pass_context=True)
async def minecraft_user(ctx, arg: str = None):
    logInfo(commandname= 'minecraft_user', user = str(ctx.message.author.name), userid = str(ctx.author.id), guildID = str(ctx.message.guild.id))
    lang = openjson(guildID = str(ctx.message.guild.id))
    if arg == None:
        embed = discord.Embed(color = 0, title = languagefile.languagepy['ErrNotArg' + lang])
        embed.set_thumbnail(url = configfile.settings['errorIMG'])
        await ctx.send(embed = embed)
    else:
        try:
            sg = skingrabber()
            skin = sg.get_skin(user=arg)
            response = requests.get('https://api.mojang.com/users/profiles/minecraft/' + arg)
            json_data = json.loads(response.text)
            embed = discord.Embed(color = 0xff9900, title = languagefile.languagepy['username'+lang] + json_data['name'], description = "UUID: " + json_data['id'] )
            embed.set_thumbnail(url = skin)
            await ctx.send(embed = embed)
        except:
            logWarn(commandname= 'minecraft_user', user = str(ctx.message.author.name), userid = str(ctx.author.id), guildID = str(ctx.message.guild.id))
            embed = discord.Embed(color = 0, title = languagefile.languagepy['unkownerror'+lang])
            embed.set_thumbnail(url = configfile.settings['errorIMG'])   
            await ctx.send(embed = embed)
@bot.command()
async def meme(ctx):
    lang = openjson(guildID = str(ctx.message.guild.id))
    logInfo(commandname= 'meme', user = str(ctx.message.author.name), userid = str(ctx.author.id), guildID = str(ctx.message.guild.id))
    response = requests.get('https://some-random-api.ml/meme')
    json_data = json.loads(response.text)
    embed = discord.Embed(color = 0xff9900, title = languagefile.languagepy['randommeme'+lang], description = json_data['caption'] )
    embed.set_image(url = json_data['image'])
    await ctx.send(embed = embed)
@bot.command()
async def ascii(ctx, *, arg):
    cropped = arg[:12]
    l = cropped.split()
    s1 = '+'.join(l)  
    response = requests.get('https://artii.herokuapp.com/make?text=' + s1)
    embed = discord.Embed(color = 0xff9900, title = 'ASCII', description = "```" + response.text + "```")
    await ctx.send(embed = embed)
@bot.command()
async def sendemote(ctx, name, id):
    emote = "<:" + name + ":" + id + ">"
    await ctx.send(emote)
@bot.command()
async def about(ctx):
    lang = openjson(guildID = str(ctx.message.guild.id))
    servers = list(bot.guilds)
    logInfo(commandname= 'about', user = str(ctx.message.author.name), userid = str(ctx.author.id), guildID = str(ctx.message.guild.id))
    embed = discord.Embed(color = 0xff9900, title = bot.user.name + languagefile.languagepy['bot'+lang], description = languagefile.languagepy['aboutdesc'+lang] + '\r\n\r\n' + configfile.emojis['?'] + languagefile.languagepy['helplistend'+lang]+ '\r\n')
    embed.add_field(name=languagefile.languagepy['owner'+lang], value= configfile.emojis['botowner'] + configfile.settings['owner'], inline=True,)
    embed.add_field(name=languagefile.languagepy['library'+lang], value= configfile.emojis['libraryicon'] + "discord.py " + str(discord.__version__) , inline=True,)
    embed.add_field(name=languagefile.languagepy['prefix'+lang], value= configfile.settings['prefix'], inline=True,)
    embed.add_field(name=languagefile.languagepy['host'+lang], value= configfile.emojis['hosticon'] + "Heroku", inline=True,)
    embed.add_field(name=languagefile.languagepy['totalguilds'+lang], value= str(len(servers)), inline=True,)
    embed.add_field(name=languagefile.languagepy['botversion'+lang], value= configfile.settings['version'], inline=True,)
    embed.add_field(name=languagefile.languagepy['supportserver'+lang], value= languagefile.languagepy['clickhere'+lang] + "(https://discord.gg/tRQbVUgKqw)", inline=True,)
    embed.add_field(name=languagefile.languagepy['botname'+lang], value= bot.user.name, inline=True,)
    embed.add_field(name=languagefile.languagepy['botinvite'+lang], value= languagefile.languagepy['clickhere'+lang] + "(http://bit.ly/furprotobot)", inline=True,)
    embed.add_field(name=languagefile.languagepy['used'+lang], value='[[Discord.py]](https://pypi.org/project/discord.py/)    [[Skingrabber]](https://pypi.org/project/skingrabber/)\r\n[[Wikipedia]](https://pypi.org/project/wikipedia/)     [[Python 3.9.1]](https://www.python.org/downloads/release/python-391/)', inline=True,)
    embed.add_field(name=languagefile.languagepy['ping'+lang], value= str(round(bot.latency, 2)) + languagefile.languagepy['ms'+lang], inline=True,)
    embed.set_footer(text = 'PythonGen © 2021 All rights reserved', icon_url=configfile.settings['owneravatar'])
    embed.set_thumbnail(url = bot.user.avatar_url)
    await ctx.send(embed = embed)
@bot.command() 
async def boop(ctx): 
    logInfo(commandname= 'boop', user = str(ctx.message.author.name), userid = str(ctx.author.id), guildID = str(ctx.message.guild.id))
    author = ctx.message.author
    await ctx.send(f'OWO, {author.mention}!')
@bot.command() 
async def stop(ctx): 
    messageauthor = str(ctx.message.author.id)
    botowner = str(configfile.settings['ownerID'])
    if messageauthor == botowner:
        embed = discord.Embed(color = 0xff9900, title = 'Okay', description = "Shutting down")
        await ctx.send(embed = embed)
        await bot.close()
    else:
        embed = discord.Embed(color = 0xff9900, title = 'NO U', description = "Access denied")
        await ctx.send(embed = embed)
@bot.command() 
async def guildinfo(ctx):
    lang = openjson(guildID = str(ctx.message.guild.id))
    text_channel_list = []
    voice_channel_list = []
    for channel in ctx.message.guild.text_channels:
        text_channel_list.append(channel)
    for channel in ctx.message.guild.voice_channels:
        voice_channel_list.append(channel)
    voice_channel_count = len(voice_channel_list)
    text_channel_count = len(text_channel_list)
    all_channel_count = text_channel_count + voice_channel_count
    membersInServer = ctx.message.guild.members
    botsInServer = list(filter(filterOnlyBots, membersInServer))
    botsInServerCount = len(botsInServer)
    embed = discord.Embed(color = 0xff9900, title = ctx.message.guild.name + languagefile.languagepy['serverWord'+lang])
    embed.add_field(value=configfile.emojis['allusers'] +" "+ languagefile.languagepy['allUsers'+lang]+ str(ctx.message.guild.member_count) + '\r' + '\n' + configfile.emojis['bot'] +" "+  languagefile.languagepy['botUsers'+lang] + str(botsInServerCount) + '\r' + '\n' +configfile.emojis['human'] +" "+  languagefile.languagepy['realUsers'+lang] + str(ctx.message.guild.member_count - botsInServerCount),name= languagefile.languagepy['usersNametag'+lang], inline=True,)
    embed.add_field(name=languagefile.languagepy['Channels'+lang], value=configfile.emojis['AllChannels'] +languagefile.languagepy['allUsers'+lang] + str(all_channel_count) + '\r\n' + configfile.emojis['VoiceChannels'] + languagefile.languagepy['VoiceChannels'+lang] + str(voice_channel_count) + '\r\n' + configfile.emojis['TextChannels'] + languagefile.languagepy['TextChannels'+lang] + str(text_channel_count) , inline=True,)
    embed.add_field(name='⠀', value= '⠀', inline=True,)
    voiceregion = str(ctx.message.guild.region)
    verificationlvl = str(ctx.message.guild.verification_level)
    servowner = await bot.fetch_user(ctx.message.guild.owner_id)
    embed.add_field(name=languagefile.languagepy['serverInfoRegion'+lang], value= configfile.regions[voiceregion] + languagefile.languagepy[voiceregion+lang], inline=True,)
    embed.add_field(name=languagefile.languagepy['serverInfoOwner'+lang], value=configfile.emojis['owner'] + str(servowner), inline=True,)
    embed.add_field(name=languagefile.languagepy['VerificationLevel'+lang], value= configfile.emojis[verificationlvl] +languagefile.languagepy[verificationlvl+lang], inline=True,)
    creationmonth = str(ctx.message.guild.created_at.strftime("%m"))
    creationdate = str(ctx.message.guild.created_at.strftime("%d "+languagefile.languagepy[creationmonth+'month'+lang] +" %Y" + languagefile.languagepy['year'+lang] +", %H:%M:%S"))
    embed.add_field(name=languagefile.languagepy['guildCreationDate'+lang], value= str(creationdate), inline=True,)
    embed.set_thumbnail(url=ctx.message.guild.icon_url)
    embed.set_footer(text= 'ID: ' + str(ctx.message.guild.id))
    await ctx.send(embed = embed)
def filterOnlyBots(member):
    return member.bot
@bot.command() 
async def userinfo(ctx, userctx: discord.Member = None):
    lang = openjson(guildID = str(ctx.message.guild.id))
    spotify = '0'
    member = ctx.author if not userctx else userctx
    if member.bot == False:
        userid = member.id
        userinf = await bot.fetch_user(userid)
        embed = discord.Embed(color = 0xff9900, title = languagefile.languagepy['infoAbout'+lang] + str(userinf))
        if str(member.activity)[:15] == '<Activity type=':
            customactivitystr = languagefile.languagepy['userActivityNone'+lang]
        else:
            if str(member.activity) == 'Spotify':
                customactivitystr = languagefile.languagepy['userActivityNone'+lang]
                spotify = '1'
            else:
                customactivitystr = str(member.activity)
        if spotify == '1':
            status = configfile.emojis['spotify'] + languagefile.languagepy['userStatusSpotify'+lang] + 'Spotify'
        else:
            status = configfile.emojis[str(member.status)] + languagefile.languagepy[str(member.status)+lang]
        usercreationmonth = str(member.created_at.strftime("%m"))
        usercreationdate = str(member.created_at.strftime("%d "+languagefile.languagepy[usercreationmonth+'month'+lang] +" %Y" + languagefile.languagepy['year'+lang] +", %H:%M:%S"))
        userjoinedmonth = str(member.joined_at.strftime("%m"))
        userjoineddate = str(member.joined_at.strftime("%d "+languagefile.languagepy[userjoinedmonth+'month'+lang] +" %Y" + languagefile.languagepy['year'+lang] +", %H:%M:%S"))
        embed.add_field(name=languagefile.languagepy['basicInfo'+lang], value= languagefile.languagepy['userInfoUsername'+lang] +str(userinf)+'\r' + '\n'+languagefile.languagepy['userinfoJoined'+lang] + userjoineddate+'\r' + '\n'+languagefile.languagepy['userinfoAccCreated'+lang] + usercreationdate+'\r' + '\n'+languagefile.languagepy['userinfoStatus'+lang] + status +'\r' + '\n'+languagefile.languagepy['customactivity'+lang] + customactivitystr , inline=False)
        embed.set_footer(text='ID: ' +str(userid))
        embed.set_thumbnail(url = member.avatar_url)
        await ctx.send(embed = embed)
    else:
        embed = discord.Embed(color = 0xff9900, title = languagefile.languagepy['infoAboutBotErr'+lang])
        embed.set_thumbnail(url = configfile.settings['errorIMG'])
        await ctx.send(embed = embed)
@bot.command() 
async def avatar(ctx, userctx: discord.Member = None): 
    lang = openjson(guildID = str(ctx.message.guild.id))
    member = ctx.author if not userctx else userctx
    userinf = await bot.fetch_user(member.id)
    embed = discord.Embed(color = 0xff9900, title = languagefile.languagepy['userAvatar'+lang] + str(userinf))
    embed.set_image(url = member.avatar_url)
    await ctx.send(embed = embed)
@bot.command() 
@has_permissions(administrator=True)
async def setlang(ctx, arg): 
    language = None
    logInfo(commandname= 'setlang', user = str(ctx.message.author.name), userid = str(ctx.author.id), guildID = str(ctx.message.guild.id))
    try:
        if arg == "en":
            language = "EN"
        else:
            if arg == "ru":
                language = "RU"
    except:
        embed = discord.Embed(color = 0, title = "Error: Wrong argument")
        embed.set_thumbnail(url = configfile.settings['errorIMG'])
        await ctx.send(embed = embed)
        print (configfile.logging['atCenter'] + str(datetime.now()) + configfile.logging['warn'] + 'Error: Wrong argument')
    if language is not None:
        languagesdatabase.set(str(ctx.message.guild.id) , language)        
def logInfo(commandname = 'not defined', user = 'no user', userid = 'no id', guildID = 'no guild id'):
    if configfile.logging['logInfo'] == 'true':
        print (configfile.logging['start'])
        print (configfile.logging['atCenter'] + str(datetime.now()) + configfile.logging['info'] +'"'+ commandname +'" '+'command')
        print (configfile.logging['atCenter'] + str(datetime.now()) + configfile.logging['info'] + 'the command was called by: "' + user + '" (user ID: ' + str(userid) + ')' + ' guild id: ' + guildID)
        print (configfile.logging['end'])
def logError(commandname = 'not defined', user = 'no user', userid = 'no id', guildID = 'no guild id', error = 'unkown error'):
    if configfile.logging['logError'] == 'true':
        print (configfile.logging['start'])
        print (configfile.logging['atCenter'] + str(datetime.now()) + configfile.logging['error'] +'"'+ commandname +'" '+'command')
        print (configfile.logging['atCenter'] + str(datetime.now()) + configfile.logging['error'] + 'the command was called by: "' + user + '" (user ID: ' + str(userid) + ')' + ' guild id: ' + guildID)
        print (configfile.logging['atCenter'] + str(datetime.now()) + configfile.logging['error'] + 'Error: ' + error) 
        print (configfile.logging['end'])
def logWarn(commandname = 'not defined', user = 'no user', userid = 'no id', guildID = 'no guild id', warn = 'unkown warning'):
    if configfile.logging['logWarn'] == 'true':
        print (configfile.logging['start'])
        print (configfile.logging['atCenter'] + str(datetime.now()) + configfile.logging['warn'] +'"'+ commandname +'" '+'command')
        print (configfile.logging['atCenter'] + str(datetime.now()) + configfile.logging['warn'] + 'the command was called by: "' + user + '" (user ID: ' + str(userid) + ')' + ' guild id: ' + guildID)
        print (configfile.logging['atCenter'] + str(datetime.now()) + configfile.logging['warn'] + 'Warning: ' + warn)
        print (configfile.logging['end'])
try:
    bot.run(configfile.settings['token'])
except discord.errors.LoginFailure:
    print (configfile.logging['fatal'] + 'Incorrect token')
