# sends sna1l_boy new code every day and times him out until he solves it

# imports
import discord
from libraries.autoStream import *
import asyncio
import random
import aiofile

# getting the bot token
config = configparser.ConfigParser()
config.read(os.path.abspath((os.path.join(directory, "config.ini"))))
sna1lBotToken = config.get("discord", "sna1l bot token")

# setting the bot up
intents = discord.Intents.default()
intents.dm_messages = True
intents.members = True
intents.message_content = True
intents.guilds = True
bot = discord.Client(intents = intents)

# setting up variables
waitingForAnswer = False
guild = None
channels = None
codeFile = None
strikes = None
permissions = discord.PermissionOverwrite()

@bot.event
async def on_ready():
    global waitingForAnswer
    global permissions
    global channels
    global guild
    global codeFile
    global strikes

    while True:

        # waiting two to five days
        await asyncio.sleep(random.randint(14400, 432000))

        strikes = 1
        waitingForAnswer = True
        guild = bot.guilds[0]
        channels = guild.channels
        codeFile = random.choice([file for file in os.listdir(os.path.join(directory, "sna1lCodeSamples", "incorrect")) if os.path.isfile(os.path.join(directory, "sna1lCodeSamples", "incorrect", file))])

        # timing out user
        permissions.send_messages = False
        tasks = []
        for channel in channels:
            if isinstance(channel, discord.TextChannel):
                task = setChannelPermissions(channel, bot.get_user(1065034277756080158), permissions)
                tasks.append(task)
        await asyncio.gather(*tasks)

        # sends python file
        if bot.get_user(1065034277756080158) and codeFile:
            async with aiofile.async_open(os.path.abspath(os.path.join(directory, "sna1lCodeSamples", "incorrect", codeFile)), "rb") as file:
                await bot.get_user(1065034277756080158).send(file = discord.File(os.path.abspath(os.path.join(directory, "sna1lCodeSamples", "incorrect", codeFile))))
                await file.close()

# receives messages from dms
@bot.event
async def on_message(message):
    global waitingForAnswer
    global permissions
    global channels
    global strikes

    if message.author.id == 1065034277756080158 and isinstance(message.channel, discord.DMChannel) and waitingForAnswer:

        # check for correct answer
        if len(message.attachments) > 0:
            for attachment in message.attachments:
                await attachment.save(os.path.abspath(os.path.join(directory, "tempAttachments", attachment.filename)))
                async with aiofile.async_open(os.path.join(os.path.abspath(os.path.join(directory, "tempAttachments", attachment.filename))), "rb") as file:
                    response = await file.read()
                    await file.close()
                    os.remove(os.path.abspath(os.path.join(directory, "tempAttachments", attachment.filename)))
                async with aiofile.async_open(os.path.abspath(os.path.join(directory, "sna1lCodeSamples", "correct", codeFile)), "rb") as file:
                    answer = await file.read()
                    await file.close()

            # if files match
            if response == answer:
                waitingForAnswer = False

                # untiming out
                permissions.send_messages = True
                tasks = []
                for channel in channels:
                    if isinstance(channel, discord.TextChannel):
                        task = setChannelPermissions(channel, message.author, permissions)
                        tasks.append(task)
                await asyncio.gather(*tasks)

                await bot.get_user(1065034277756080158).send("well done")

            # if not then add to strike count
            else:
                if strikes == 3:
                    waitingForAnswer = False
                    await bot.get_user(1065034277756080158).send("strike " + str(strikes))
                    await bot.get_user(1065034277756080158).send("better luck tomorrow :)")
                else:
                    await bot.get_user(1065034277756080158).send("strike " + str(strikes))
                    strikes += 1


# for timing out in all channels at the same time
async def setChannelPermissions(channel, user, permissions):

    # """""error handling""""" in case bot can't access all channels
    try:
        await channel.set_permissions(user, overwrite=permissions)
    except:
        await asyncio.sleep(0)
