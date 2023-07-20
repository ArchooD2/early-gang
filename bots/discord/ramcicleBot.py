# times out ramcicle every time he speaks

# imports
import discord
import asyncio
from libraries.autoStream import *
import threading

# getting the bot token
config = configparser.ConfigParser()
config.read(os.path.abspath((os.path.join(directory, "config.ini"))))
ramcicleBotToken = config.get("discord", "ramcicle bot token")

# setting the bot up
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.members = True
bot = discord.Client(intents = intents)

@bot.event
async def on_message(message):
    if message.author.id == 232162258229264384:

        # getting server info
        guild = bot.guilds[0]
        channels = guild.channels
        permissions = discord.PermissionOverwrite()

        # setting permissions for all channels
        permissions.send_messages = False
        tasks = []
        for channel in channels:
            if isinstance(channel, discord.TextChannel):
                task = setChannelPermissions(channel, message.author, permissions)
                tasks.append(task)
        await asyncio.gather(*tasks)

        # waiting
        await asyncio.sleep(3)

        # resetting permissions for all channels
        permissions.send_messages = True
        tasks = []
        for channel in channels:
            if isinstance(channel, discord.TextChannel):
                task = setChannelPermissions(channel, message.author, permissions)
                tasks.append(task)
        await asyncio.gather(*tasks)

    # telling the bot what to do
    await bot.process_commands(message)

# for timing out in all channels at the same time
async def setChannelPermissions(channel, user, permissions):

    # """""error handling""""" in case bot can't access all channels
    try:
        await channel.set_permissions(user, overwrite=permissions)
    except:
        await asyncio.sleep(0)