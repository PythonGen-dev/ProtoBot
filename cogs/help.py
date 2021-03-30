import json

import discord
from discord.ext import commands

from modules import storage, getlang, getcustomemote

prefix = json.load(open("config.json", "r"))["prefix"]
translates = storage("./locals/langs.lang")
emotes = storage("./locals/emotes.lang")


class HelpCog(commands.Cog, name="help command"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def helpnew(self, ctx):
        commands = list()
        for command in self.bot.commands:
            if str(command) not in ["devsetlang", "eval", "helpnew", "help", "addbadge", "jishaku"]: commands.append(command.name) # remove dev commands
        embed = discord.Embed(title='Help',description='**{}** '.format(translates.get('prefix' + getlang(ctx))) + '`' + str(prefix) + '`')
        anime = str(); utilities = str(); furry = str(); nsfw = str(); others = str(); fun = str(); bots = str(); games = str()
        for command in commands:
            command = str(command)
            # anime
            if command in ["quote", "hug", "wink", "pat", "sad", "facepalm"]: anime += "> {0}{1} - {2}\r\n".format(prefix, command, translates.get(command + "_help_desc_" + getlang(ctx)))
            # utilities
            elif command in ["avatar", "aboutme", "about", "getemoji", "guildinfo", "userinfo", "boop", "setlang", "PyPI"]: utilities += "> {0}{1} - {2}\r\n".format(prefix, command, translates.get(command + "_help_desc_" + getlang(ctx)))
            # furry
            elif command in ["wikifur_search", "wikifur_display"]: furry += "> {0}{1} - {2}\r\n".format(prefix, command, translates.get(command + "_help_desc_" + getlang(ctx)))
            # nsfw
            elif command in ["rule34"]: nsfw += "> {0}{1} - {2}\r\n".format(prefix, command, translates.get(command + "_help_desc_" + getlang(ctx)))
            # fun
            elif command in ["minecraft", "ascii", "meme", "glitch", "lyrics", "image"]: fun += "> {0}{1} - {2}\r\n".format(prefix, command, translates.get(command + "_help_desc_" + getlang(ctx)))
            # bots
            elif command in ["topcord", "discordbots"]: bots += "> {0}{1} - {2}\r\n".format(prefix, command,translates.get(command + "_help_desc_" + getlang(ctx)))
            # others
            else: others += "> {0}{1}\r\n".format(prefix, command)

        embed = embed.add_field(name=getcustomemote(self=self, emote='senko', ctx=ctx) + ' {}:'.format(translates.get('animeMenu' + getlang(ctx))), value=anime, inline=False)
        embed = embed.add_field(name=getcustomemote(self=self, emote='mod', ctx=ctx) + ' {}:'.format(translates.get('utilitiesMenu' + getlang(ctx))), value=utilities, inline=False)
        embed = embed.add_field(name=getcustomemote(self=self, emote='paw', ctx=ctx) + ' {}:'.format(translates.get('furryMenu' + getlang(ctx))), value=furry, inline=False)
        embed = embed.add_field(name=getcustomemote(self=self, emote='fun', ctx=ctx) + ' {}:'.format(translates.get('funMenu' + getlang(ctx))), value=fun, inline=False)
        embed = embed.add_field(name=getcustomemote(self=self, emote='bot', ctx=ctx) + ' {}:'.format(translates.get('botsMenu' + getlang(ctx))), value=bots, inline=False)
        embed = embed.add_field(name=getcustomemote(self=self, emote='nsfw', ctx=ctx) + ' {}:'.format(translates.get('nsfwMenu' + getlang(ctx))), value=nsfw, inline=False)
        if others != "": embed = embed.add_field(name=":test_tube: " + ' {}:'.format(translates.get('othersMenu' + getlang(ctx))), value=others, inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.remove_command("help")
    bot.add_cog(HelpCog(bot))
