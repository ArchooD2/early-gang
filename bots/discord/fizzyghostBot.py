# ghost pings (pun not intended) fizzygohst in a random channel every 2-10 hours
import random

# imports
import discord
from libraries.autoStream import *

# getting the bot token
config = configparser.ConfigParser()
config.read(os.path.abspath((os.path.join(directory, "config.ini"))))
fizzyghostBotToken = config.get("discord", "fizzyghost bot token")

# setting the bot up
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = discord.Client(intents = intents)

# pinging every two to ten hours
@bot.event
async def on_ready():
    while True:
        await asyncio.sleep(random.randint(7200, 36000))
        message = await random.choice(list(bot.get_all_channels())).send(bot.get_user(232746777114050561).mention)
        await message.delete()


