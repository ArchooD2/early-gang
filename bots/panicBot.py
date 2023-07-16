# pings users on discord when command bot's !panicCode or !panicStream is called
# panic bot CAN NOT know of command bot's existence hence why it writes to config instead of importing and changing a variable from command bot

# imports
import discord
import random
from discord.ext import commands
import threading
from libraries.autoStream import *
import time

# getting the bot token
config = configparser.ConfigParser()
config.read(os.path.abspath((os.path.join(directory, "config.ini"))))
token = config.get("discord", "panic bot token")

# setting the bot up
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents = intents)

# starts new panic bot thread
def startPanicBot():
    def runBot():
        bot.run(token)

    panicBotThread = threading.Thread(target = runBot)
    panicBotThread.start()
    return panicBotThread


@bot.event
async def on_ready():
    while True:

        # checks for changes to config
        config = configparser.ConfigParser()
        config.read(os.path.abspath((os.path.join(directory, "config.ini"))))

        # if !panicCode has been called
        if config.get("discord", "ping kai") == "True":

            # send the message
            for x in range(random.randint(5, 10)):
                await bot.get_channel(1129275757630332941).send(bot.get_user(1065034277756080158).mention + " AAAAHH CODE BROKE AAAAAAAAHHHHH HELP US PLEASE")
            time.sleep(4)
            await bot.get_channel(1129275757630332941).send("oops")

            # resetting the file
            with open(os.path.abspath((os.path.join(directory, "config.ini"))), "r") as file:
                lines = file.readlines()
            for i, line in enumerate(lines):
                if line.startswith("ping kai ="):
                    lines[i] = "ping kai = False\n"
                    break
            with open(os.path.abspath((os.path.join(directory, "config.ini"))), "w") as file:
                file.writelines(lines)

        # if !panicStream has been called
        if config.get("discord", "ping fizz") == "True":

            # send the message
            for x in range(random.randint(5, 10)):
                await bot.get_channel(1129275757630332941).send(bot.get_user(232746777114050561).mention + " WEEE WOOO HELP US STREAM NO WORK AAAAAAAAAAAAAAAAAHHHHHH")
            time.sleep(4)
            await bot.get_channel(1129275757630332941).send("oops")

            # resetting the file
            with open(os.path.abspath((os.path.join(directory, "config.ini"))), "r") as file:
                lines = file.readlines()
            for i, line in enumerate(lines):
                if line.startswith("ping fizz ="):
                    lines[i] = "ping fizz = False\n"
                    break
            with open(os.path.abspath((os.path.join(directory, "config.ini"))), "w") as file:
                file.writelines(lines)

