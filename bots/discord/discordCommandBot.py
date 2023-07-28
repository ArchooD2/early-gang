# basic bot to host all the commands needed for the discord server
# TODO reminders
# TODO cah
# TODO role menus

# imports
import asyncio
import random

import discord
from libraries.autoStream import *

# setting the bot up
config = configparser.ConfigParser()
config.read(os.path.abspath((os.path.join(directory, "config.ini"))))
commandBotToken = config.get("discord", "command bot token")
bot = discord.Client(command_prefix = "!", intents = discord.Intents.all())

# void counter
@bot.event
async def on_member_update(before, after):

    # when someone leaves
    if discord.utils.get(before.roles, id=1132732881140203571) or discord.utils.get(before.roles, id=1125863416708472832):
        await bot.get_channel(1132769096900034700).send("Void Visitor has departed: " + before.mention + ". Void Count: " + str(len(discord.utils.get(bot.get_guild(1122315794538303528).roles, id = 1132732881140203571).members) + len(discord.utils.get(bot.get_guild(1122315794538303528).roles, id = 1125863416708472832).members)))

    # when someone joins
    if discord.utils.get(after.roles, id=1132732881140203571) or discord.utils.get(after.roles, id=1125863416708472832):
        await bot.get_channel(1132769096900034700).send("Void Visitor has arrived: " + before.mention + ". Void Count: " + str(len(discord.utils.get(bot.get_guild(1122315794538303528).roles, id = 1132732881140203571).members) + len(discord.utils.get(bot.get_guild(1122315794538303528).roles, id = 1125863416708472832).members)))

# voids user for a random amount of time on reaction to the role menu
@bot.event
async def on_raw_reaction_add(payload):
    message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    if payload.message_id == 1132625274077454416 and discord.utils.get(message.reactions, emoji="🍿"):
        await payload.member.add_roles(bot.guilds[0].get_role(1125863416708472832))
        asyncio.create_task(voidWait(payload.member, discord.utils.get(message.reactions, emoji="🍿")))

# waiting to unvoid
async def voidWait(user, reaction):
    await asyncio.sleep(random.randint(120, 10800))
    await user.remove_roles(bot.guilds[0].get_role(1125863416708472832))
    await reaction.remove(user)