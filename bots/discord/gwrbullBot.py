# doesnt let gwrbull delete/edit their messages

# imports
import discord
from libraries.autoStream import *
import aiofile

# getting the bot token
config = configparser.ConfigParser()
config.read(os.path.abspath((os.path.join(directory, "config.ini"))))
gwrbullBotToken = config.get("discord", "gwrbull bot token")

# setting the bot up
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = discord.Client(intents = intents)

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