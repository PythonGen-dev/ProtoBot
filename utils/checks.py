import utils.aiopg as aiopg
from utils.exceptions import *


async def checkpremium(ctx):
    try:
        return (await aiopg.aiogetrow("premium", [["guildid", ctx.guild.id]]))[-1]
    except: raise NoPremiumException('no_premium')