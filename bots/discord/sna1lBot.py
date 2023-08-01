# sends sna1l_boy new code every day and times him out until he solves it

# changing system path
import sys
sys.path.insert(0, sys.path[0].replace("bots\\discord", ""))

# imports
import discord
from libraries.autoStream import *
import asyncio
import random
import aiofile

# getting the bot token
config = configparser.ConfigParser()
config.read(os.path.abspath((os.path.join(directory, "config.ini"))))
token = config.get("discord", "sna1l bot token")
bot = discord.Client(intents = discord.Intents.all())

# setting up variables
waitingForAnswer = False
codeFile = None
strikes = None

@bot.event
async def on_ready():
    global waitingForAnswer
    global codeFile
    global strikes

    while True:

        # waiting two to five days
        await asyncio.sleep(random.randint(14400, 432000))

        strikes = 1
        waitingForAnswer = True
        codeFile = random.choice([file for file in os.listdir(os.path.join(directory, "sna1lCodeSamples", "incorrect")) if os.path.isfile(os.path.join(directory, "sna1lCodeSamples", "incorrect", file))])

        # timing out
        try:
            tasks = []
            for channel in bot.guilds[0].channels:
                task = channel.set_permissions(bot.guilds[0].get_member(1065034277756080158), send_messages = False, send_messages_in_threads = False)
                tasks.append(task)
            await asyncio.gather(*tasks)
        except:
            await asyncio.sleep(0)

        # sends python file
        if bot.get_user(1065034277756080158) and codeFile:
            async with aiofile.async_open(os.path.abspath(os.path.join(directory, "sna1lCodeSamples", "incorrect", codeFile)), "rb") as file:
                await bot.get_user(1065034277756080158).send(file = discord.File(os.path.abspath(os.path.join(directory, "sna1lCodeSamples", "incorrect", codeFile))))
                await file.close()

# receives messages from dms
@bot.event
async def on_message(message):
    global waitingForAnswer
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
                try:
                    tasks = []
                    for channel in bot.guilds[0].channels:
                        task = channel.set_permissions(bot.guilds[0].get_member(1065034277756080158), send_messages = True, send_messages_in_threads = True)
                        tasks.append(task)
                    await asyncio.gather(*tasks)
                except:
                    await asyncio.sleep(0)

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

# starting bot
bot.run(token)