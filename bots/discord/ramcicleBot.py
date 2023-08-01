# times out ramcicle every time he speaks

# changing system path
import sys
sys.path.insert(0, sys.path[0].replace("bots\\discord", ""))

# imports
import discord
from libraries.autoStream import *

# setting the bot up
config = configparser.ConfigParser()
config.read(os.path.abspath((os.path.join(directory, "config.ini"))))
token = config.get("discord", "ramcicle bot token")
bot = discord.Client(intents = discord.Intents.all())

@bot.event
async def on_message(message):
    if message.author.id == 232162258229264384 and 1 == 2:

        # timing out
        try:
            tasks = []
            for channel in bot.guilds[0].channels:
                task = channel.set_permissions(bot.guilds[0].get_member(232162258229264384), send_messages = False, send_messages_in_threads = False)
                tasks.append(task)
            await asyncio.gather(*tasks)
        except:
            await asyncio.sleep(0)

        # waiting
        await asyncio.sleep(3)

        # untiming out
        try:
            tasks = []
            for channel in bot.guilds[0].channels:
                task = channel.set_permissions(bot.guilds[0].get_member(232162258229264384), send_messages = True, send_messages_in_threads = True)
                tasks.append(task)
            await asyncio.gather(*tasks)
        except:
            await asyncio.sleep(0)

    # telling the bot what to do
    await bot.process_commands(message)

# starting bot
bot.run(token)