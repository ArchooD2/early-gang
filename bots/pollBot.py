# creates and manages poll in chat
# don't fuck with this too much unless you're familiar with twitchio and how it works
# not much documentation here because even i don't know what the fuck this object oriented programming is doing in python

import threading
from twitchio.ext import commands
from libraries.autoStream import *

# setting up variables
runningPoll = False
pollName = ""
pollStarter = ""
pollOptions = []
voters = []

# starts bot in new thread
def startPollBot():
    bot = Bot()
    botThread = threading.Thread(target=bot.run)
    botThread.start()
    return botThread

class Bot(commands.Bot):

    # sets up bot and connects to twitch
    def __init__(self):
        super().__init__(token=accessToken, prefix="!", initial_channels=[yourChannelName])

    # does whenever a message is sent
    async def event_message(self, message):
        global pollStarter
        global pollOptions
        global runningPoll
        global voters
        global pollName

        # don't take bot responses as real messages
        if message.echo:
            return

        # if pole is active
        elif runningPoll:
            # checks if chatter already votes
            if message.author.name not in voters:
                # checks if message is number then increases vote count for the specified option
                for x in range(len(pollOptions)):
                    if message.content == str(x + 1):
                        pollOptions[x][1] += 1
                        voters += [message.author.name]

        # telling bot to do command
        await self.handle_commands(message)

    # starts poll if it's a whitelisted user and no other polls are going on
    @commands.command()
    async def startPoll(self, ctx):
        global pollStarter
        global pollOptions
        global voters
        global pollName
        global runningPoll

        if ctx.author.name == "fizzeghost" or ctx.author.name == "sna1l_boy" or ctx.author.name == "dougdoug" or ctx.author.name == "parkzer":
            if not runningPoll:
                if ctx.message.content == "!startPoll" or ctx.message.content == "!startPoll ":
                    await ctx.send("please include your title and poll options in your command messages formatted like !startPoll title, option 1, option 2, option 3, ...")
                else:
                    ctx.message.content = (ctx.message.content).replace("!startPoll ", "")
                    ctx.message.content = ctx.message.content.split(", ")
                    pollName = ctx.message.content[0]
                    pollStarter = ctx.author.name
                    pollOptions = []
                    for element in ctx.message.content:
                        if element != ctx.message.content[0]:
                            pollOptions += [[element, 0]]
                    voters = []
                    runningPoll = True

    # tells current poll voting options and stats or results from most recent past one
    @commands.command()
    async def poll(self, ctx):
        global pollStarter
        global pollOptions
        global runningPoll
        global pollName

        if runningPoll:
            results = ""
            total = 0
            for x in range(len(pollOptions)):
                total += pollOptions[x][1]
            for x in range(len(pollOptions)):
                if total != 0:
                    results += (str(x + 1) + ", " + pollOptions[x][0] + " - " + str('%.2f' % ((pollOptions[x][1] / total) * 100)) + "%, ")
                else:
                    results += (str(x + 1) + ", " + pollOptions[x][0] + " - " + "0%, ")
            await ctx.send("[bot] " + pollName + ": " + results)

        if not runningPoll:
            if pollOptions == []:
                await ctx.send("[bot] no past or ongoing polls")
            else:
                results = ""
                total = 0
                for x in range(len(pollOptions)):
                    total += int(pollOptions[x][1])
                for x in range(len(pollOptions)):
                    if total != 0:
                        results += (pollOptions[x][0] + " - " + str('%.2f' % ((pollOptions[x][1] / total) * 100)) + "%, ")
                    else:
                        results += (pollOptions[x][0] + " - 0%, ")
                await ctx.send("[bot] " + "\"" + pollName + "\"" + " results: " + results)

    # stops poll and responds with results
    @commands.command()
    async def endPoll(self, ctx):
        global pollStarter
        global runningPoll
        global pollOptions
        global voters
        global pollName

        if ctx.author.name == pollStarter:
            if not runningPoll:
                await ctx.send("[bot] no ongoing polls")
            elif runningPoll:
                runningPoll = False
                results = ""
                total = 0
                for x in range(len(pollOptions)) :
                    total += pollOptions[x][1]
                for x in range(len(pollOptions)) :
                    if total != 0:
                        results += (pollOptions[x][0] + " - " + str('%.2f'%((pollOptions[x][1]/total) * 100)) + "%, ")
                    else:
                        results += (pollOptions[x][0] + " - 0%, ")
                await ctx.send("[bot] " + "\"" + pollName + "\"" + " results: " + results)

    # tells the user how to vote in poll
    @commands.command()
    async def vote(self, ctx):
        global pollOptions
        if runningPoll:
            results = ""
            for x in range(len(pollOptions)):
                results += ("type \"" + str(x+1) + "\" to vote \"" + pollOptions[x][0] + "\", ")
            await ctx.send("[bot] " + results)
        else:
            await ctx.send("[bot] no ongoing poll")
