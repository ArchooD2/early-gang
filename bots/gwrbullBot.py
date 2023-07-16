# doesnt let gwrbull delete/edit their messages

# imports
import discord
from discord.ext import commands
from libraries.autoStream import *
import threading

# getting the bot token
config = configparser.ConfigParser()
config.read(os.path.abspath((os.path.join(directory, "config.ini"))))
token = config.get("discord", "gwrbull bot token")

# setting the bot up
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix = "!", intents = intents)

# starts new gwrbull bot thread
def startGwrbullBot():
    def runBot():
        bot.run(token)

    gwrbullBotThread = threading.Thread(target = runBot)
    gwrbullBotThread.start()
    return gwrbullBotThread

# sends deleted message content
@bot.event
async def on_message_delete(message):
    if str(message.author) == "gwrbull":

        # send message content if any
        if len(message.content) > 0:
            await message.channel.send("deleted \"" + message.content + "\"")

        # save and send attachments if any
        if len(message.attachments) > 0:
            for attachment in message.attachments:
                os.makedirs(os.path.abspath(os.path.join(directory, "attachments")), exist_ok = True)
                await attachment.save(os.path.abspath(os.path.join(directory, "attachments", attachment.filename)))
                with open(os.path.join(os.path.abspath(os.path.join(directory, "attachments", attachment.filename))), "rb") as file:
                    await message.channel.send(file = discord.File(file))
                    file.close()
                    os.remove(os.path.abspath(os.path.join(directory, "attachments", attachment.filename)))

# sends message edit content
@bot.event
async def on_message_edit(before, after):
    if str(before.author) == "gwrbull" and before.content != after.content:
        await before.channel.send("edited \"" + before.content + "\" to \"" + after.content + "\"")