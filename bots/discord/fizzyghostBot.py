# ghost pings (pun not intended) fizzyghost in a random channel every 2-10 hours

# changing system path
import sys
sys.path.insert(0, sys.path[0].replace("bots\\discord", ""))

# imports
import random
import discord
from libraries.autoStream import *

# setting the bot up
config = configparser.ConfigParser()
config.read(os.path.abspath((os.path.join(directory, "config.ini"))))
token = config.get("discord", "fizzyghost bot token")
bot = discord.Client(intents = discord.Intents.all())

# pinging every two to ten hours
@bot.event
async def on_ready():
    while True:
        await asyncio.sleep(random.randint(7200, 36000))
        message = await random.choice(list(bot.get_all_channels())).send(bot.get_user(232746777114050561).mention)
        await message.delete()


