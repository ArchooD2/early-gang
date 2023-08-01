# doesnt let gwrbull delete/edit their messages

# changing system path
import sys
sys.path.insert(0, sys.path[0].replace("bots\\discord", ""))

# imports
import discord
from libraries.autoStream import *
import aiofile

# setting the bot up
config = configparser.ConfigParser()
config.read(os.path.abspath((os.path.join(directory, "config.ini"))))
token = config.get("discord", "gwrbull bot token")
bot = discord.Client(intents = discord.Intents.all())

# sends deleted message content
@bot.event
async def on_message_delete(message):

    if message.author.id == 959715465914105856:

        # send message content if any
        if len(message.content) > 0:
            await message.channel.send("deleted \"" + message.content + "\"")

        # save and send attachments if any
        if len(message.attachments) > 0:
            for attachment in message.attachments:
                await attachment.save(os.path.abspath(os.path.join(directory, "tempAttachments", attachment.filename)))
                async with aiofile.async_open(os.path.join(os.path.abspath(os.path.join(directory, "tempAttachments", attachment.filename))), "rb") as file:
                    await message.channel.send(file = discord.File(os.path.join(os.path.abspath(os.path.join(directory, "tempAttachments", attachment.filename)))))
                    await file.close()
                    os.remove(os.path.abspath(os.path.join(directory, "tempAttachments", attachment.filename)))

# sends message edit content
@bot.event
async def on_message_edit(before, after):
    if before.author.id == 959715465914105856 and before.content != after.content:
        await before.channel.send("edited \"" + before.content + "\" to \"" + after.content + "\"")

# starting bot
bot.run(token)