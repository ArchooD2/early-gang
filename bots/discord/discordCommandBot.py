# basic bot to host all the commands needed for the discord server
# TODO cah
# TODO role menus
import datetime

# imports
import discord
from discord.ext import commands
import random
from libraries.autoStream import *


# setting the bot up
config = configparser.ConfigParser()
config.read(os.path.abspath((os.path.join(directory, "config.ini"))))
commandBotToken = config.get("discord", "command bot token")
bot = commands.Bot(command_prefix = "!", intents = discord.Intents.all())

# it's yagging time
@bot.event
async def on_ready():
    await bot.tree.sync()
    while True:
        await asyncio.sleep(random.randint(43200, 86400))
        await bot.get_channel(1125230641563312238).send("it's yagging time")

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

# mentions a user with a message after a certain amount of time
@bot.tree.command(name="remindme")
async def remindme(interaction: discord.Interaction, days: int = None, hours: int = None, minutes: int = None, seconds: int = None, message:str = None):
    if not days:
        days = 0
    if not hours:
        hours = 0
    if not minutes:
        minutes = 0
    if not seconds:
        seconds = 0
    try:
        await interaction.response.send_message("<t:" + str(int((datetime.datetime.now() + datetime.timedelta(seconds=(seconds + minutes * 60 + hours * 3600 + days * 86400))).timestamp())) + ":R>")
        asyncio.create_task(reminderWait(interaction.user, interaction.channel, (seconds + minutes * 60 + hours * 3600 + days * 86400), message))
    except Exception as e:
        print(e)

# waiting send reminder
async def reminderWait(user, channel, seconds, message):
    await asyncio.sleep(seconds)
    if message:
        await channel.send("**reminder for **" + user.mention)
        await channel.send(embed = discord.Embed(color = 1, description = message, title = ("reminder for " + user.name)))
    else:
        await channel.send("**reminder for **" + user.mention)