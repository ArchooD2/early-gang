# manages channel point economy and responds to commands relating to it
# don't fuck with this too much unless you're familiar with twitchio and how it works
# not much documentation here because even i don't know what the fuck this object oriented programming is doing in python


import threading
import csv
from twitchio.ext import commands
from libraries.autoStream import *
from libraries.chatPlays import *
import requests
import os
from datetime import datetime, timezone
import sys
from random import *

# setting up variables
chatters = []
live = False
writingFile = False
readingFile = False
appendingFile = False
firstRedeemed = True

# reading random actions and items
with open(os.path.abspath((os.path.join(directory, "randomItems.txt"))), "r") as file:
    items = file.read()
    items = items.split("\n")
with open(os.path.abspath((os.path.join(directory, "randomPastTenseActions.txt"))), "r") as file:
    pastTenseActions = file.read()
    pastTenseActions = pastTenseActions.split("\n")
with open(os.path.abspath((os.path.join(directory, "randomPresentTenseActions.txt"))), "r") as file:
    presentTenseActions = file.read()
    presentTenseActions = presentTenseActions.split("\n")

def startEconBot():
    global live
    live = isLive(yourChannelName)

    bot = Bot()
    bot_thread = threading.Thread(target=bot.run)
    bot_thread.start()
    return bot_thread

# reads economy.csv and returns the contents
def readFile():
    global readingFile
    global writingFile
    global appendingFile

    readingFile = True
    while readingFile:
        if not writingFile and not appendingFile:
            with open(os.path.abspath((os.path.join(directory, "economy.csv"))), "r") as file:
                reader = csv.reader(file)
                rows = list(reader)
            readingFile = False
    rows = [row for row in rows if any(field.strip() for field in row)]
    return rows

# writes a list of rows to economy.csv
def writeFile(rows):
    global readingFile
    global writingFile
    global appendingFile

    writingFile = True
    while writingFile:
        if not appendingFile and not readingFile:
            print("writing to file please dont stop instance")
            with open(os.path.abspath((os.path.join(directory, "economy.csv"))), "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            writingFile = False
            print("done writing")
            sleep(3)

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=accessToken, prefix="!", initial_channels=[yourChannelName])

        # starts file update thread for econ bot
        csvThread = threading.Thread(target = updateWatchTime)
        csvThread.start()

# whenever a user joins write their id and entry time into an array and add their id to the database if not there
    async def event_join(self, channel, user):
        global chatters
        global readingFile
        global appendingFile
        # adds chatter id, watch time start, and uptime start
        if getBroadcasterId(user.name) not in chatters and getBroadcasterId(user.name) is not None:
            chatters += [[getBroadcasterId(user.name), time(), time()]]

        # read the existing ids from the csv file
        csvIds = []
        readingFile = True
        while readingFile:
            if not writingFile and not appendingFile:
                with open(os.path.abspath((os.path.join(directory, "economy.csv"))), "r") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        csvIds += [row[0]]
                readingFile = False

        # add any ids not in the csv to it
        appendingFile = True
        while appendingFile:
            if not writingFile and not readingFile:
                with open(os.path.abspath((os.path.join(directory, "economy.csv"))), "a", newline = "") as file:
                    writer = csv.writer(file)
                    for name, watch, points in chatters:
                        if str(name) not in csvIds:
                            writer.writerow([name, 0, 0])
                appendingFile = False

    # whenever a user leaves add their remaining time to the csv and remove them from the array
    async def event_part(self, user):
        global chatters
        global writingFile
        global readingFile
        global appendingFile
        data = await self.fetch_users([user.name])
        chatter = []

        # finding chatter's time
        for element in chatters:
            if element[0] == data[0].id:
                chatter = element
                break

        # writing chatter time to file
        if chatter and isLive(yourChannelName):
            rows = readFile()
            for row in rows:
                if row[0] == str(data[0].id):
                    row[1] = float(row[1]) + (time() - chatter[1])
                    break
            writeFile(rows)

            # removing chatter from active chatter list
            chatters.remove(chatter)

    # sends a message with the user's watch time formatted as days, hours, minutes, seconds
    @commands.command()
    async def watchtime(self, ctx: commands.Context):
        global writingFile
        global readingFile
        global appendingFile

        # finding user id
        data = await self.fetch_users([ctx.author.name])
        data = data[0].id

        # reading csv file
        rows = readFile()

        # checks each row for id and if so retrieves the associated watchtime and sends it
        for row in rows:
            if row[0] == str(data):
                seconds = round(float(row[1]))
                minutes, seconds = divmod(seconds, 60)
                hours, minutes = divmod(minutes, 60)
                days, hours = divmod(hours, 24)

                await ctx.send("[bot] " + ctx.author.name + " has watched " + yourChannelName + " for " + str(days) + " days " + str(hours) + " hours " + str(minutes) + " minutes and " + str(seconds) + " seconds")
                break

    # tells the user how many points they have
    @commands.command()
    async def bp(self, ctx: commands.Context):
        global writingFile
        global readingFile
        global appendingFile

        # checks each row for id and if so retrieves the associated watchtime and sends it
        rows = readFile()
        for row in rows:
            if row[0] == str(getBroadcasterId(ctx.author.name)):
                await ctx.send("[bot] " + ctx.author.name + " has " + str(round(float(row[2]))) + " basement pesos")
                break


    @commands.command()
    async def first(self, ctx: commands.Context):
        global firstRedeemed
        global writingFile
        global readingFile
        global appendingFile

        if isLive(yourChannelName):
            # calculate points gained/loss
            connected = False
            while not connected:
                try:
                    response = requests.get("https://api.twitch.tv/helix/users", headers={"Client-ID": clientID, "Authorization": f"Bearer {accessToken}"})
                    rateLimit = response.headers.get("Ratelimit-Remaining")
                    if rateLimit != "0":
                        userResponse = requests.get(f"https://api.twitch.tv/helix/users?login={yourChannelName}", headers = {"Client-ID": clientID, "Authorization": "Bearer " + accessToken}).json()
                        streamResponse = requests.get(f'https://api.twitch.tv/helix/streams?user_id={userResponse.get("data")[0].get("id")}', headers = {"Client-ID": clientID, "Authorization": "Bearer " + accessToken}).json()
                        connected = True
                    else:
                        sleep(5)
                except:
                    sleep(5)

            # in case uptime is 0
            try:
                points = round(1000/((datetime.now(timezone.utc) - datetime.fromisoformat(streamResponse.get("data")[0].get("started_at")[:-1]).replace(tzinfo=timezone.utc)).total_seconds())) if round(1000/((datetime.now(timezone.utc) - datetime.fromisoformat(streamResponse.get("data")[0].get("started_at")[:-1]).replace(tzinfo=timezone.utc)).total_seconds())) > 100 else 100
            except:
                points = 1000

            # updating points
            rows = readFile()
            for row in rows:
                if row[0] == str(getBroadcasterId(ctx.author.name)):
                    # if first !first, give 100 points
                    if not firstRedeemed:
                        row[2] = int(row[2]) + int(points)
                        await ctx.send("[bot] " + ctx.author.name + " is first " + ctx.author.name + " gained " + str(points) + " basement pesos")
                    # if not first !first, take 100 points
                    else:
                        if int(row[2]) > 0:
                            row[2] = int(row[2]) - int(points)
                        else:
                            row[2] = 0
                        await ctx.send("[bot] " + ctx.author.name + " is not first " + ctx.author.name + " lost " + str(points) + " basement pesos")
                    break
            writeFile(rows)

    # lets users give their points to each other
    @commands.command()
    async def giveBp(self, ctx: commands.Context):
        global writingFile
        global readingFile
        global appendingFile

        if ctx.author.name == "fizzeghost" or ctx.author.name == "sna1l_boy" or ctx.author.name == "dougdoug" or ctx.author.name == "parkzer":
            if ctx.message.content == "!giveBp" or ctx.message.content == "!giveBp ":
                    await ctx.send("please include the user and amount your command messages formatted like !giveBP user, 100")
            else:
                ctx.message.content = (ctx.message.content).replace("!giveBp ", "")
                ctx.message.content = ctx.message.content.split(", ")

                print(getBroadcasterId(ctx.message.content[0]))
                if getBroadcasterId(ctx.message.content[0]) != None:
                    # updating points
                    rows = readFile()
                    for row in rows:
                        if row[0] == str(getBroadcasterId(ctx.message.content[0])):
                            print(row[2])
                            row[2] = int(row[2]) + int(ctx.message.content[1])
                            print(row[2])
                            await ctx.send("[bot] gave " + ctx.message.content[0] + " " + ctx.message.content[1] + " basement pesos")
                            break
                    writeFile(rows)

        else:
            if ctx.message.content == "!giveBp" or ctx.message.content == "!giveBp ":
                    await ctx.send("please include the user and amount your command messages formatted like !giveBP user, 100")
            else:
                ctx.message.content = ctx.message.content.replace("!giveBp ", "")
                ctx.message.content = ctx.message.content.split(", ")

                if getBroadcasterId(ctx.author.name) != "" and getBroadcasterId(ctx.message.content[0]) != "":
                    # updating points
                    rows = readFile()
                    foundTaker = False
                    foundGiver = False

                    for row in rows:
                        if row[0] == str(getBroadcasterId(ctx.author.name)):
                            foundGiver = True
                            if int(row[2]) < int(ctx.message.content[1]):
                                ctx.message.content[1] = int(row[2])
                            row[2] = int(row[2]) - int(ctx.message.content[1])
                            break

                    for row in rows:
                        if row[0] == str(getBroadcasterId(ctx.message.content[0])):
                            foundTaker = True
                            row[2] = int(row[2]) + int(ctx.message.content[1])
                            break

                    if foundTaker and foundGiver:
                        # writing changes to file
                        writeFile(rows)
                        await ctx.send("[bot] " + ctx.author.name + " gave " + ctx.message.content[0] + " " + ctx.message.content[1] + " basement pesos")
                    else:
                        await ctx.send("[bot] couldn't find at least one user")

    @commands.command()
    async def bpTax(self, ctx: commands.Context):
        global writingFile
        global readingFile
        global appendingFile

        if ctx.author.name == "fizzeghost" or ctx.author.name == "sna1l_boy" or ctx.author.name == "dougdoug" or ctx.author.name == "parkzer":
            if ctx.message.content == "!bpTax" or ctx.message.content == "!bpTax ":
                await ctx.send(
                    "please include the user and amount your command messages formatted like !bpTax user, 100")
            else:
                ctx.message.content = (ctx.message.content).replace("!bpTax ", "")
                ctx.message.content = ctx.message.content.split(", ")

                if getBroadcasterId(ctx.message.content[0]) != None:

                    # updating points
                    rows = readFile()
                    for row in rows:
                        if row[0] == str(getBroadcasterId([ctx.message.content[0]])):
                            row[2] = int(row[2]) - int(ctx.message.content[1])
                            await ctx.send("[bot] took from " + ctx.message.content[0] + " " + ctx.message.content[1] + " basement pesos")
                            break
                    writeFile(rows)

    @commands.command()
    async def bpShop(self, ctx: commands.Context):
        await ctx.send("[bot] !shoot (2000), !shootSnack (2000), !swapSnack (1000)")

    # times out user
    @commands.command()
    async def shoot(self, ctx: commands.Context):
        time = randint(10, 60)
        finalId = ""

        # getting mod ids
        connected = False
        while not connected:
            try:
                response = requests.get("https://api.twitch.tv/helix/users", headers={"Client-ID": clientID, "Authorization": f"Bearer {accessToken}"})
                rateLimit = response.headers.get("Ratelimit-Remaining")
                if rateLimit != "0":
                    response = requests.get("https://api.twitch.tv/helix/moderation/moderators?broadcaster_id=" + getBroadcasterId(yourChannelName),headers={"Authorization": f"Bearer {accessToken}", "Client-Id": clientID})
                    connected = True
                else:
                    sleep(5)
            except:
                sleep(5)
        modIds = []
        for mod in response.json().get("data"):
            modIds += [mod.get("user_id")]

        # if no person named shoot random
        if ctx.message.content == "!shoot":
            rows = readFile()
            for row in rows:
                if row[0] == str(getBroadcasterId(ctx.author.name)):
                    if int(row[2]) < 2000 and ctx.author.name != "dougdoug" and ctx.author.name != "parkzer" and ctx.author.name != "fizzeghost" and ctx.author.name != "sna1l_boy":
                        await ctx.send("[bot] not enough basement pesos")
                    else:
                        connected = False
                        while not connected:
                            try:
                                response = requests.get("https://api.twitch.tv/helix/users", headers={"Client-ID": clientID, "Authorization": f"Bearer {accessToken}"})
                                rateLimit = response.headers.get("Ratelimit-Remaining")
                                if rateLimit != "0":
                                    response = requests.get("https://api.twitch.tv/helix/chat/chatters?broadcaster_id=" + getBroadcasterId(yourChannelName) + "&moderator_id=" + getBroadcasterId(yourChannelName), headers = {"Authorization": f"Bearer {accessToken}", "Client-Id": clientID})
                                    connected = True
                                else:
                                    sleep(5)
                            except:
                                sleep(5)

                        names = []
                        for element in response.json().get("data"):
                            names += [[element.get("user_id"), element.get("user_name")]]
                        user = names[randint(0, len(names)-1)]

                        connected = False
                        while not connected:
                            try:
                                response = requests.get("https://api.twitch.tv/helix/users", headers={"Client-ID": clientID, "Authorization": f"Bearer {accessToken}"})
                                rateLimit = response.headers.get("Ratelimit-Remaining")
                                if rateLimit != "0":
                                    response = requests.post("https://api.twitch.tv/helix/moderation/bans?broadcaster_id=" + getBroadcasterId(yourChannelName) + "&moderator_id=" + getBroadcasterId(yourChannelName), headers = {"Authorization": "Bearer " + accessToken, "Client-Id": clientID, "Content-Type": "application/json"}, json = {"data": {"user_id": user[0], "reason": "you got shot", "duration": time}})
                                    connected = True
                                else:
                                    sleep(5)
                            except:
                                sleep(5)

                        await ctx.send("[bot] " + ctx.author.name +  " " + pastTenseActions[randint(0, len(pastTenseActions)-1)] + " " + user[1] + " with " + items[randint(0, len(items)-1)])
                        if ctx.author.name != "dougdoug" and ctx.author.name != "parkzer" and ctx.author.name != "fizzeghost" and ctx.author.name != "sna1l_boy":
                            row[2] = int(row[2]) - 2000
                            writeFile(rows)

                        if user[0] in modIds:
                            remodThread = threading.Thread(target=remod(user[0], time))
                            remodThread.start()
                    break
        # try to shoot listed person
        else:
            rows = readFile()
            for row in rows:
                if row[0] == str(getBroadcasterId(ctx.author.name)):
                    if int(row[2]) < 2000 and ctx.author.name != "dougdoug" and ctx.author.name != "parkzer" and ctx.author.name != "fizzeghost" and ctx.author.name != "sna1l_boy":
                        await ctx.send("[bot] not enough basement pesos")
                    else:
                        dice = randint(1, 100)
                        ctx.message.content = (ctx.message.content).replace("!shoot ", "")
                        id = getBroadcasterId(ctx.message.content)

                        # error handling
                        if id == None:
                             await ctx.send("[bot] couldn't find user")
                        else:
                            # 10% chance to shoot yourself
                            if dice > 90:

                                connected = False
                                while not connected:
                                    try:
                                        response = requests.get("https://api.twitch.tv/helix/users", headers={"Client-ID": clientID, "Authorization": f"Bearer {accessToken}"})
                                        rateLimit = response.headers.get("Ratelimit-Remaining")
                                        if rateLimit != "0":
                                            response = requests.post("https://api.twitch.tv/helix/moderation/bans?broadcaster_id=" + getBroadcasterId(yourChannelName) + "&moderator_id=" + getBroadcasterId(yourChannelName), headers = {"Authorization": "Bearer " + accessToken, "Client-Id": clientID, "Content-Type": "application/json"}, json = {"data": {"user_id": getBroadcasterId(ctx.author.name), "reason": "you got shot", "duration": time}})
                                            connected = True
                                        else:
                                            sleep(5)
                                    except:
                                        sleep(5)

                                finalId = getBroadcasterId(ctx.author.name)
                                await ctx.send("[bot] " + ctx.author.name + " missed and " + items[randint(0, len(items)-1)] + " bounced into their head")

                            # 65% chance to shoot random
                            elif dice > 25:
                                connected = False
                                while not connected:
                                    try:
                                        response = requests.get("https://api.twitch.tv/helix/users", headers={"Client-ID": clientID, "Authorization": f"Bearer {accessToken}"})
                                        rateLimit = response.headers.get("Ratelimit-Remaining")
                                        if rateLimit != "0":
                                            response = requests.get("https://api.twitch.tv/helix/chat/chatters?broadcaster_id=" + getBroadcasterId(yourChannelName) + "&moderator_id=" + getBroadcasterId(yourChannelName), headers = {"Authorization": f"Bearer {accessToken}", "Client-Id": clientID})
                                            connected = True
                                        else:
                                            sleep(5)
                                    except:
                                        sleep(5)

                                names = []
                                for element in response.json().get("data"):
                                    names += [[element.get("user_id"), element.get("user_name")]]
                                user = names[randint(0, len(names)-1)]

                                connected = False
                                while not connected:
                                    try:
                                        response = requests.get("https://api.twitch.tv/helix/users", headers={"Client-ID": clientID,
                                                                                                              "Authorization": f"Bearer {accessToken}"})
                                        rateLimit = response.headers.get("Ratelimit-Remaining")
                                        if rateLimit != "0":
                                            response = requests.post("https://api.twitch.tv/helix/moderation/bans?broadcaster_id=" + getBroadcasterId(yourChannelName) + "&moderator_id=" + getBroadcasterId(yourChannelName), headers = {"Authorization": "Bearer " + accessToken, "Client-Id": clientID, "Content-Type": "application/json"}, json = {"data": {"user_id": user[0], "reason": "you got shot", "duration": time}})
                                            connected = True
                                        else:
                                            sleep(5)
                                    except:
                                        sleep(5)

                                finalId = user[0]
                                await ctx.send("[bot] " + ctx.author.name + " tried to " + presentTenseActions[randint(0, len(presentTenseActions)-1)] + " " + ctx.message.content + " with "  + items[randint(0, len(items)-1)] + " but they used " + user[1] + " as a shield")

                            # 25% chance to shoot target
                            else:

                                connected = False
                                while not connected:
                                    try:
                                        response = requests.get("https://api.twitch.tv/helix/users", headers={"Client-ID": clientID, "Authorization": f"Bearer {accessToken}"})
                                        rateLimit = response.headers.get("Ratelimit-Remaining")
                                        if rateLimit != "0":
                                            response = requests.post("https://api.twitch.tv/helix/moderation/bans?broadcaster_id=" + getBroadcasterId(yourChannelName) + "&moderator_id=" + getBroadcasterId(yourChannelName), headers = {"Authorization": "Bearer " + accessToken, "Client-Id": clientID, "Content-Type": "application/json"}, json = {"data": {"user_id": id, "reason": "you got shot", "duration": time}})
                                            connected = True
                                        else:
                                            sleep(5)
                                    except:
                                        sleep(5)

                                await ctx.send("[bot] " + ctx.author.name + " " + pastTenseActions[randint(0, len(pastTenseActions)-1)] + " " + ctx.message.content + " with " + items[randint(0, len(items)-1)])

                            finalId = id
                            if ctx.author.name != "dougdoug" and ctx.author.name != "parkzer" and ctx.author.name != "fizzeghost" and ctx.author.name != "sna1l_boy":
                                row[2] = int(row[2]) - 2000
                                writeFile(rows)

                            if finalId in modIds:
                                remodThread = threading.Thread(target=remod(finalId, time))
                                remodThread.start()
                    break

    # disables input bot for 10 to 30 minutes
    @commands.command()
    async def shootSnack(self, ctx: commands.Context):
        rows = readFile()
        for row in rows:
            if row[0] == str(getBroadcasterId(ctx.author.name)):
                if int(row[2]) < 2000 and ctx.author.name != "dougdoug" and ctx.author.name != "parkzer" and ctx.author.name != "fizzeghost" and ctx.author.name != "sna1l_boy":
                    await ctx.send("[bot] not enough basement pesos")
                else:
                    chatPlays.snackShot = True
                    await ctx.send("[bot] " + ctx.author.name + " " +  pastTenseActions[randint(0, len(pastTenseActions)-1)] + " " + chatPlays.currentSnack + " snack with " + items[randint(0, len(items)-1)])

                    if ctx.author.name != "dougdoug" and ctx.author.name != "parkzer" and ctx.author.name != "fizzeghost" and ctx.author.name != "sna1l_boy":
                        row[2] = int(row[2]) - 2000
                        writeFile(rows)
                    break

                    waitThread = threading.Thread(target=snackWait)
                    waitThread.start()

# changes input bot type
    @commands.command()
    async def swapSnack(self, ctx: commands.Context):

        rows = readFile()
        for row in rows:
            if row[0] == str(getBroadcasterId(ctx.author.name)):
                if int(row[2]) < 1000 and ctx.author.name != "dougdoug" and ctx.author.name != "parkzer" and ctx.author.name != "fizzeghost" and ctx.author.name != "sna1l_boy":
                    await ctx.send("[bot] not enough basement pesos")
                else:
                    chatPlays.currentSnack = snacks[randint(0, len(snacks) - 1)]
                    await ctx.send("[bot] " + chatPlays.currentSnack + " snack was swapped in")

                    if ctx.author.name != "dougdoug" and ctx.author.name != "parkzer" and ctx.author.name != "fizzeghost" and ctx.author.name != "sna1l_boy":
                        row[2] = int(row[2]) - 1000
                        writeFile(rows)
                    break

# as soon as bot is logged in constantly check the array and update watch time and points
def updateWatchTime():
    global chatters
    global live
    global firstRedeemed
    global writingFile
    global readingFile
    global appendingFile

    while True:
        if isLive(yourChannelName):
            if not live:
                for element in chatters:
                    element[1] = time()
                    element[2] = time()
                live = True
                firstRedeemed = False

            for element in chatters:
                rows = readFile()
                for row in rows:
                    if row[0] == str(element[0]):
                        if (time() - element[2]) >= 300:
                            row[2] = int(row[2]) + 10
                            element[2] = time()
                        row[1] = float(row[1]) + (time() - element[1])
                        element[1] = time()
                        break
            writeFile(rows)
        else:
            live = False
        sleep(1)

# thread to wait to restart input bot
def snackWait():
    sleep(randint(600, 1800))
    chatPlays.snackShot = False

def remod(id, time):
    sleep(time)
    modIds = []
    connected = False
    while not connected and id not in modIds:
        try:
            response = requests.get("https://api.twitch.tv/helix/users", headers={"Client-ID": clientID, "Authorization": f"Bearer {accessToken}"})
            rateLimit = response.headers.get("Ratelimit-Remaining")
            if rateLimit != "0":
                response = requests.get("https://api.twitch.tv/helix/moderation/moderators?broadcaster_id=" + getBroadcasterId(yourChannelName) + "&user_id=" + id ,headers={"Authorization": f"Bearer {accessToken}", "Client-Id": clientID})
                response = requests.get("https://api.twitch.tv/helix/moderation/moderators?broadcaster_id=" + getBroadcasterId(yourChannelName),headers={"Authorization": f"Bearer {accessToken}", "Client-Id": clientID})
                modIds = []
                for mod in response.json().get("data"):
                    modIds += [mod.get("user_id")]
                connected = True
            else:
                sleep(5)
        except:
            sleep(5)
