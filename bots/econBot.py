# manages channel point economy and responds to commands relating to it
# don't fuck with this too much unless you're familiar with twitchio and how it works
# also you gotta know how to use sqlite3 so good luck ;)
# not much documentation here because even i don't know what the fuck this object oriented programming shit is doing in python

# imports
import asyncio
import time
from datetime import datetime, timezone
import random
from twitchio.ext import commands
from libraries.chatPlays import *
import sqlite3

# setting up variables
databaseLock = asyncio.Lock()
chatters = []
live = False
firstRedeemed = True

# starts econ bot in a new thread
def startEconBot():
    global live
    live = isLive(yourChannelName)

    bot = Bot()
    econBotThread = threading.Thread(target = bot.run)
    econBotThread.start()
    return econBotThread

class Bot(commands.Bot):

    # sets up bot and connects to twitch
    def __init__(self):
        super().__init__(token = accessToken, prefix = "!", initial_channels = [yourChannelName])

    # starts updating database
    async def event_ready(self):
        await self.updateWatchTime()

    # whenever a user joins write their id and entry time into an array and add their id to the database if not there
    async def event_join(self, channel, user):
        global chatters

        # adds chatter id, watch time start, and uptime start
        if getBroadcasterId(user.name) not in chatters and getBroadcasterId(user.name) is not None:
            chatters += [[getBroadcasterId(user.name), time.time(), time.time()]]

        # reading database
        async with databaseLock:
            db = sqlite3.connect(os.path.abspath((os.path.join(directory, "chatData.db"))))
            cursor = db.cursor()
            cursor.execute("SELECT id FROM economy WHERE id=?", (getBroadcasterId(user.name),))
            result = cursor.fetchone()

            # adding id if not in database
            if result is None:
                cursor.execute("INSERT INTO economy (id, watchtime, points) VALUES (?,?,?)", (getBroadcasterId(user.name), 0, 0, ))
                db.commit()
            db.close()

    # whenever a user leaves add their remaining time to the csv and remove them from the array
    async def event_part(self, user):
        global chatters

        # finding chatter's time
        for element in chatters:
            if element[0] == getBroadcasterId(user.name):
                chatter = element
                break

        # writing chatter time to file
        if chatter and isLive(yourChannelName):
            async with databaseLock:
                db = sqlite3.connect(os.path.abspath((os.path.join(directory, "chatData.db"))))
                cursor = db.cursor()
                cursor.execute("SELECT * FROM economy WHERE id=?", (getBroadcasterId(user.name),))
                result = cursor.fetchone()
                cursor.execute("UPDATE economy SET watchtime=? WHERE id=?", ((float(result[1]) + (time.time() - chatter[1])), getBroadcasterId(user.name)))
                db.commit()
                db.close()

            # removing chatter from active chatter list
            chatters.remove(chatter)

    # sends a message with the user's watch time formatted as days, hours, minutes, seconds
    @commands.command()
    async def watchtime(self, ctx: commands.Context):

        # finding user id in database
        async with databaseLock:
            db = sqlite3.connect(os.path.abspath((os.path.join(directory, "chatData.db"))))
            cursor = db.cursor()
            cursor.execute("SELECT * FROM economy WHERE id=?", (getBroadcasterId(ctx.author.name),))
            result = cursor.fetchone()
            db.close()

        # calculating output
        if result:
            seconds = round(float(result[1]))
            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)
            days, hours = divmod(hours, 24)
            weeks, days = divmod(days, 7)
            months, weeks = divmod(weeks, 4)
            years, months = divmod(months, 12)
            centuries, years = divmod(years, 100)

            duration = ""
            if centuries > 0:
                duration += str(centuries) + " centuries "
            if years > 0:
                duration += str(years) + " years "
            if months > 0:
                duration += str(months) + " months "
            if weeks > 0:
                duration += str(weeks) + " weeks "
            if days > 0:
                duration += str(days) + " days "
            if hours > 0:
                duration += str(hours) + " hours "
            if minutes > 0:
                duration += str(minutes) + " minutes "
            if seconds > 0:
                duration += str(seconds) + " seconds"
            if duration == "":
                duration += str(seconds) + " seconds"

            await ctx.send("[bot] " + ctx.author.name + " has watched " + yourChannelName + " for " + duration)

    # tells the user how many points they have
    @commands.command()
    async def bp(self, ctx: commands.Context):

        # finding user id in database
        async with databaseLock:
            db = sqlite3.connect(os.path.abspath((os.path.join(directory, "chatData.db"))))
            cursor = db.cursor()
            cursor.execute("SELECT * FROM economy WHERE id=?", (getBroadcasterId(ctx.author.name),))
            result = cursor.fetchone()
            db.close()

        # sending result if id exists
        if result:
            await ctx.send("[bot] " + ctx.author.name + " has " + str(result[2]) + " basement pesos")

    # first user to redeem this gets points but those afterward lose points
    @commands.command()
    async def first(self, ctx: commands.Context):
        global firstRedeemed

        if isLive(yourChannelName):

            # calculate points gained/loss
            connected = False
            while not connected:
                try:
                    response = requests.get("https://api.twitch.tv/helix/users", headers = {"Client-ID": clientID, "Authorization": f"Bearer {accessToken}"})
                    rateLimit = response.headers.get("Ratelimit-Remaining")
                    if rateLimit != "0":
                        userResponse = requests.get(f"https://api.twitch.tv/helix/users?login={yourChannelName}", headers = {"Client-ID": clientID, "Authorization": "Bearer " + accessToken}).json()
                        streamResponse = requests.get(f'https://api.twitch.tv/helix/streams?user_id={userResponse.get("data")[0].get("id")}', headers = {"Client-ID": clientID, "Authorization": "Bearer " + accessToken}).json()
                        connected = True
                    else:
                        await asyncio.sleep(5)
                except:
                    await asyncio.sleep(5)

            # in case uptime is 0
            try:
                points = round(1000/((datetime.now(timezone.utc) - datetime.fromisoformat(streamResponse.get("data")[0].get("started_at")[:-1]).replace(tzinfo=timezone.utc)).total_seconds())) if round(1000/((datetime.now(timezone.utc) - datetime.fromisoformat(streamResponse.get("data")[0].get("started_at")[:-1]).replace(tzinfo=timezone.utc)).total_seconds())) > 100 else 100
            except:
                points = 1000

            # searching database for id
            async with databaseLock:
                db = sqlite3.connect(os.path.abspath((os.path.join(directory, "chatData.db"))))
                cursor = db.cursor()
                cursor.execute("SELECT * FROM economy WHERE id=?", (getBroadcasterId(ctx.author.name),))
                result = cursor.fetchone()

                # updating points
                if result:

                    # if first !first, give points
                    if not firstRedeemed:
                        cursor.execute("UPDATE economy SET points=? WHERE id=?", ((result[2] + points), getBroadcasterId(ctx.author.name)))

                        await ctx.send("[bot] " + ctx.author.name + " is first " + ctx.author.name + " gained " + str(points) + " basement pesos")

                    # if not first !first, take points
                    else:
                        if result[2] > 100:
                            cursor.execute("UPDATE economy SET points=? WHERE id=?", ((result[2] - points), getBroadcasterId(ctx.author.name)))
                        else:
                            cursor.execute("UPDATE economy SET points=? WHERE id=?", (0, getBroadcasterId(ctx.author.name)))
                        await ctx.send("[bot] " + ctx.author.name + " is not first " + ctx.author.name + " lost " + str(points) + " basement pesos")
                    db.commit()
                    db.close()

    # lets users give their points to each other
    @commands.command()
    async def giveBp(self, ctx: commands.Context):

        # checks if it's a whitelister so that they can print money
        if ctx.author.name in whiteListers:

            # error handling
            if ctx.message.content == "!giveBp" or ctx.message.content == "!giveBp ":
                await ctx.send("please include the user and amount your command messages formatted like !giveBP user, 100")

            # finding and updating the appropriate points
            else:
                ctx.message.content = ctx.message.content.replace("!giveBp ", "")
                ctx.message.content = ctx.message.content.split(", ")

                if getBroadcasterId(ctx.message.content[0]):
                    async with databaseLock:
                        db = sqlite3.connect(os.path.abspath((os.path.join(directory, "chatData.db"))))
                        cursor = db.cursor()
                        cursor.execute("SELECT * FROM economy WHERE id=?", (getBroadcasterId(ctx.author.name),))
                        result = cursor.fetchone()
                        cursor.execute("UPDATE economy SET points=? WHERE id=?", ((result[2] + int(ctx.message.content[1])), getBroadcasterId(ctx.message.content[0])))
                        db.commit()
                        db.close()

                    await ctx.send("[bot] gave " + ctx.message.content[0] + " " + ctx.message.content[1] + " basement pesos")

        # actually transfer money if it's not a whitelister
        else:

            # error handling
            if ctx.message.content == "!giveBp" or ctx.message.content == "!giveBp ":
                await ctx.send("please include the user and amount your command messages formatted like !giveBP user, 100")

            # finding and updating the appropriate points
            else:
                ctx.message.content = ctx.message.content.replace("!giveBp ", "")
                ctx.message.content = ctx.message.content.split(", ")

                # no stealing >:)
                if int(ctx.message.content[1]) < 0:
                    await ctx.send("[bot] nice try")

                # if both users exist
                elif getBroadcasterId(ctx.author.name) and getBroadcasterId(ctx.message.content[0]):

                    # finding giver and taker
                    async with databaseLock:
                        db = sqlite3.connect(os.path.abspath((os.path.join(directory, "chatData.db"))))
                        cursor = db.cursor()

                        cursor.execute("SELECT * FROM economy WHERE id=?", (getBroadcasterId(ctx.author.name),))
                        giver = cursor.fetchone()

                        cursor.execute("SELECT * FROM economy WHERE id=?", (getBroadcasterId(ctx.author.name),))
                        taker = cursor.fetchone()

                        # check if giver has enough points
                        if giver[2] < int(ctx.message.content[1]):
                            await ctx.send("[bot] not enough basement pesos")

                        # transfer money
                        elif giver and taker:
                            cursor.execute("UPDATE economy SET points=? WHERE id=?", ((giver[2] - int(ctx.message.content[1])), getBroadcasterId(ctx.author.name)))
                            cursor.execute("UPDATE economy SET points=? WHERE id=?", ((taker[2] + int(ctx.message.content[1])), getBroadcasterId(ctx.message.content[0])))
                            db.commit()
                            db.close()

                            await ctx.send("[bot] " + ctx.author.name + " gave " + ctx.message.content[0] + " " + ctx.message.content[1] + " basement pesos")

                        # error handling
                        else:
                            await ctx.send("[bot] couldn't find at least one user")
                else:
                    await ctx.send("[bot] couldn't find at least one user")

    # lets whitelisters take points
    @commands.command()
    async def bpTax(self, ctx: commands.Context):

        # checks if the chatter can do this
        if ctx.author.name in whiteListers:

            # error handling
            if ctx.message.content == "!bpTax" or ctx.message.content == "!bpTax ":
                await ctx.send("please include the user and amount your command messages formatted like !bpTax user, 100")

            # finding and updating the appropriate points
            else:
                ctx.message.content = ctx.message.content.replace("!bpTax ", "")
                ctx.message.content = ctx.message.content.split(", ")

                # seeing if user exists
                if getBroadcasterId(ctx.message.content[0]):
                    async with databaseLock:
                        db = sqlite3.connect(os.path.abspath((os.path.join(directory, "chatData.db"))))
                        cursor = db.cursor()
                        cursor.execute("SELECT * FROM economy WHERE id=?", (getBroadcasterId(ctx.message.content[0]),))
                        result = cursor.fetchone()

                        # if user in database
                        if result:
                            cursor.execute("UPDATE economy SET points=? WHERE id=?", ((result[2] - int(ctx.message.content[1])), getBroadcasterId(ctx.message.content[0])))
                            db.commit()
                            db.close()
                            await ctx.send("[bot] took from " + ctx.message.content[0] + " " + ctx.message.content[1] + " basement pesos")

    # lists commands available for purchase
    @commands.command()
    async def bpShop(self, ctx: commands.Context):
        await ctx.send("[bot] !shoot (1000), !shootSnack (1000), !swapSnack (500), !emp (300)")

    # times out user
    @commands.command()
    async def shoot(self, ctx: commands.Context):
        duration = random.randint(10, 60)
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
                    await asyncio.sleep(5)
            except:
                await asyncio.sleep(5)
        modIds = []
        for mod in response.json().get("data"):
            modIds += [mod.get("user_id")]

        # if no person named shoot random
        if ctx.message.content == "!shoot":

            async with databaseLock:

                # finding user id in database
                db = sqlite3.connect(os.path.abspath((os.path.join(directory, "chatData.db"))))
                cursor = db.cursor()
                cursor.execute("SELECT * FROM economy WHERE id=?", (getBroadcasterId(ctx.author.name),))
                result = cursor.fetchone()

                # check if user has the money
                if result[2] < 1000 and ctx.author.name not in whiteListers:
                    await ctx.send("[bot] not enough basement pesos")
                else:
                    if ctx.author.name not in whiteListers:
                        cursor.execute("UPDATE economy SET points=? WHERE id=?", ((result[2] - 1000), getBroadcasterId(ctx.author.name)))
                        db.commit()

                    # getting all current chatters
                    connected = False
                    while not connected:
                        try:
                            response = requests.get("https://api.twitch.tv/helix/users", headers={"Client-ID": clientID, "Authorization": f"Bearer {accessToken}"})
                            rateLimit = response.headers.get("Ratelimit-Remaining")
                            if rateLimit != "0":
                                response = requests.get("https://api.twitch.tv/helix/chat/chatters?broadcaster_id=" + getBroadcasterId(yourChannelName) + "&moderator_id=" + getBroadcasterId(yourChannelName), headers={"Authorization": f"Bearer {accessToken}", "Client-Id": clientID})
                                connected = True
                            else:
                                await asyncio.sleep(5)
                        except:
                            await asyncio.sleep(5)

                    names = []
                    for element in response.json().get("data"):
                        names += [[element.get("user_id"), element.get("user_name")]]
                    user = names[random.randint(0, len(names) - 1)]

                    # getting item and action
                    cursor.execute("SELECT item FROM items ORDER BY RANDOM() LIMIT 1")
                    item = cursor.fetchone()
                    cursor.execute("SELECT action FROM pastTenseActions ORDER BY RANDOM() LIMIT 1")
                    pastTenseAction = cursor.fetchone()

                    # shooting the random chatter
                    connected = False
                    while not connected:
                        try:
                            response = requests.get("https://api.twitch.tv/helix/users", headers={"Client-ID": clientID, "Authorization": f"Bearer {accessToken}"})
                            rateLimit = response.headers.get("Ratelimit-Remaining")
                            if rateLimit != "0":
                                response = requests.post("https://api.twitch.tv/helix/moderation/bans?broadcaster_id=" + getBroadcasterId(yourChannelName) + "&moderator_id=" + getBroadcasterId(yourChannelName), headers = {"Authorization": "Bearer " + accessToken, "Client-Id": clientID, "Content-Type": "application/json"}, json = {"data": {"user_id": user[0], "reason": "you got shot", "duration": duration}})
                                await ctx.send("[bot] " + ctx.author.name + " " + ''.join(filter(lambda x: x.isalpha() or x.isspace(), str(pastTenseAction))) + " " + user[1] + " with " + ''.join(filter(lambda x: x.isalpha() or x.isspace(), str(item))))
                                connected = True
                            else:
                                await asyncio.sleep(5)
                        except:
                            await asyncio.sleep(5)

                    # setting up remod thread if needed
                    if user[0] in modIds:
                        print("started remod thread")
                        asyncio.create_task(self.remod(user[0], duration))
                db.close()

        # try to shoot listed person
        else:
            async with databaseLock:

                # finding user id in database
                db = sqlite3.connect(os.path.abspath((os.path.join(directory, "chatData.db"))))
                cursor = db.cursor()
                cursor.execute("SELECT * FROM economy WHERE id=?", (getBroadcasterId(ctx.author.name),))
                result = cursor.fetchone()

                # check if user has the money
                if result[2] < 1000 and ctx.author.name not in whiteListers:
                    await ctx.send("[bot] not enough basement pesos")
                else:
                    if ctx.author.name not in whiteListers:
                        cursor.execute("UPDATE economy SET points=? WHERE id=?", ((result[2] - 1000), getBroadcasterId(ctx.author.name)))
                        db.commit()

                    dice = random.randint(1, 100)
                    ctx.message.content = (ctx.message.content).replace("!shoot ", "")
                    id = getBroadcasterId(ctx.message.content)

                    # error handling
                    if id == None:
                        await ctx.send("[bot] couldn't find user")

                    # shooting based off dice
                    else:

                        # getting item and action
                        cursor.execute("SELECT item FROM items ORDER BY RANDOM() LIMIT 1")
                        item = cursor.fetchone()
                        cursor.execute("SELECT action FROM pastTenseActions ORDER BY RANDOM() LIMIT 1")
                        pastTenseAction = cursor.fetchone()
                        cursor.execute("SELECT action FROM presentTenseActions ORDER BY RANDOM() LIMIT 1")
                        presentTenseAction = cursor.fetchone()

                        # 10% chance to shoot yourself
                        if dice > 90:
                            connected = False
                            while not connected:
                                try:
                                    response = requests.get("https://api.twitch.tv/helix/users", headers={"Client-ID": clientID, "Authorization": f"Bearer {accessToken}"})
                                    rateLimit = response.headers.get("Ratelimit-Remaining")
                                    if rateLimit != "0":
                                        response = requests.post("https://api.twitch.tv/helix/moderation/bans?broadcaster_id=" + getBroadcasterId(yourChannelName) + "&moderator_id=" + getBroadcasterId(yourChannelName), headers = {"Authorization": "Bearer " + accessToken, "Client-Id": clientID, "Content-Type": "application/json"}, json = {"data": {"user_id": getBroadcasterId(ctx.author.name), "reason": "you got shot", "duration": duration}})
                                        finalId = getBroadcasterId(ctx.author.name)
                                        await ctx.send("[bot] " + ctx.author.name + " missed and " + ''.join(filter(lambda x: x.isalpha() or x.isspace(), str(item))) + " bounced into their head")
                                        connected = True
                                    else:
                                        await asyncio.sleep(5)
                                except:
                                    await asyncio.sleep(5)

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
                                        await asyncio.sleep(5)
                                except:
                                    await asyncio.sleep(5)

                            names = []
                            for element in response.json().get("data"):
                                names += [[element.get("user_id"), element.get("user_name")]]
                            user = names[random.randint(0, len(names)-1)]

                            connected = False
                            while not connected:
                                try:
                                    response = requests.get("https://api.twitch.tv/helix/users", headers={"Client-ID": clientID, "Authorization": f"Bearer {accessToken}"})
                                    rateLimit = response.headers.get("Ratelimit-Remaining")
                                    if rateLimit != "0":
                                        response = requests.post("https://api.twitch.tv/helix/moderation/bans?broadcaster_id=" + getBroadcasterId(yourChannelName) + "&moderator_id=" + getBroadcasterId(yourChannelName), headers = {"Authorization": "Bearer " + accessToken, "Client-Id": clientID, "Content-Type": "application/json"}, json = {"data": {"user_id": user[0], "reason": "you got shot", "duration": duration}})
                                        finalId = user[0]
                                        await ctx.send("[bot] " + ctx.author.name + " tried to " + ''.join(filter(lambda x: x.isalpha() or x.isspace(), str(presentTenseAction))) + " " + ctx.message.content + " with "  + ''.join(filter(lambda x: x.isalpha() or x.isspace(), str(item))) + " but they used " + user[1] + " as a shield")
                                        connected = True
                                    else:
                                        await asyncio.sleep(5)
                                except:
                                    await asyncio.sleep(5)


                        # 25% chance to shoot target
                        else:
                            connected = False
                            while not connected:
                                try:
                                    response = requests.get("https://api.twitch.tv/helix/users", headers={"Client-ID": clientID, "Authorization": f"Bearer {accessToken}"})
                                    rateLimit = response.headers.get("Ratelimit-Remaining")
                                    if rateLimit != "0":
                                        response = requests.post("https://api.twitch.tv/helix/moderation/bans?broadcaster_id=" + getBroadcasterId(yourChannelName) + "&moderator_id=" + getBroadcasterId(yourChannelName), headers = {"Authorization": "Bearer " + accessToken, "Client-Id": clientID, "Content-Type": "application/json"}, json = {"data": {"user_id": id, "reason": "you got shot", "duration": duration}})
                                        finalId = id
                                        await ctx.send("[bot] " + ctx.author.name + " " + ''.join(filter(lambda x: x.isalpha() or x.isspace(), str(pastTenseAction))) + " " + ctx.message.content + " with " + ''.join(filter(lambda x: x.isalpha() or x.isspace(), str(item))))
                                        connected = True
                                    else:
                                        await asyncio.sleep(5)
                                except:
                                    await asyncio.sleep(5)

                        if finalId in modIds:
                              asyncio.create_task(self.remod(finalId, duration))
                    db.close()

    # disables input bot for 10 to 30 minutes
    @commands.command()
    async def shootSnack(self, ctx: commands.Context):

        async with databaseLock:

            # finding user id in database
            db = sqlite3.connect(os.path.abspath((os.path.join(directory, "chatData.db"))))
            cursor = db.cursor()
            cursor.execute("SELECT * FROM economy WHERE id=?", (getBroadcasterId(ctx.author.name),))
            result = cursor.fetchone()

            # check if user has the money
            if result[2] < 1000 and ctx.author.name not in whiteListers:
                await ctx.send("[bot] not enough basement pesos")
            else:
                if ctx.author.name not in whiteListers:
                    cursor.execute("UPDATE economy SET points=? WHERE id=?", ((result[2] - 1000), getBroadcasterId(ctx.author.name)))
                    db.commit()

                # getting random action and item
                cursor.execute("SELECT item FROM items ORDER BY RANDOM() LIMIT 1")
                item = cursor.fetchone()
                cursor.execute("SELECT action FROM pastTenseActions ORDER BY RANDOM() LIMIT 1")
                action = cursor.fetchone()

                # disabling input bot
                chatPlays.snackShot = True
                await ctx.send("[bot] " + ctx.author.name + " " + ''.join(filter(lambda x: x.isalpha() or x.isspace(), str(action))) + " " + chatPlays.currentSnack + " snack with " + ''.join(filter(lambda x: x.isalpha() or x.isspace(), str(item))))
                updateSnatus()
                asyncio.create_task(self.snackWait())
            db.close()

    # changes input bot type
    @commands.command()
    async def swapSnack(self, ctx: commands.Context):

        async with databaseLock:

            # finding user id in database
            db = sqlite3.connect(os.path.abspath((os.path.join(directory, "chatData.db"))))
            cursor = db.cursor()
            cursor.execute("SELECT * FROM economy WHERE id=?", (getBroadcasterId(ctx.author.name),))
            result = cursor.fetchone()

            # check if user has the money
            if result[2] < 500 and ctx.author.name not in whiteListers:
                await ctx.send("[bot] not enough basement pesos")
            else:
                if ctx.author.name not in whiteListers:
                    cursor.execute("UPDATE economy SET points=? WHERE id=?", ((result[2] - 500), getBroadcasterId(ctx.author.name)))
                    db.commit()
                chatPlays.currentSnack = snacks[random.randint(0, len(snacks) - 1)]
                await ctx.send("[bot] " + chatPlays.currentSnack + " snack was swapped in")
                updateSnatus()
            db.close()

    # disables landmines for ten to fifteen minutes
    @commands.command()
    async def emp(self, ctx: commands.Context):

        async with databaseLock:

            # finding user id in database
            db = sqlite3.connect(os.path.abspath((os.path.join(directory, "chatData.db"))))
            cursor = db.cursor()
            cursor.execute("SELECT * FROM economy WHERE id=?", (getBroadcasterId(ctx.author.name),))
            result = cursor.fetchone()

            # check if user has the money
            if result[2] < 300 and ctx.author.name not in whiteListers:
                await ctx.send("[bot] not enough basement pesos")
            else:
                if ctx.author.name not in whiteListers:
                    cursor.execute("UPDATE economy SET points=? WHERE id=?",
                                   ((result[2] - 300), getBroadcasterId(ctx.author.name)))
                    db.commit()
                chatPlays.landminesActive = False
                await ctx.send("[bot] " + ctx.author.name + " deactivated landmines")
                asyncio.create_task(self.empWait())
            db.close()

    # as soon as bot is logged in constantly check the array and update watch time and points
    async def updateWatchTime(self):
        global chatters
        global live
        global firstRedeemed

        while True:
            await asyncio.sleep(5)

            # when channel goes live reset uptime and !first
            if isLive(yourChannelName):
                if not live:
                    for element in chatters:
                        element[1] = time.time()
                        element[2] = time.time()
                    live = True
                    firstRedeemed = False

                # update database for all users in chat
                async with databaseLock:
                    for chatter in chatters:

                        # trying to find id
                        db = sqlite3.connect(os.path.abspath((os.path.join(directory, "chatData.db"))))
                        cursor = db.cursor()
                        cursor.execute("SELECT * FROM economy WHERE id=?", (chatter[0],))
                        result = cursor.fetchone()

                        # setting points and watchtime
                        if result:
                            if (time.time() - chatter[2]) >= 300:
                                cursor.execute("UPDATE economy SET points=? WHERE id=?", ((result[2] + 10), chatter[0]))
                                chatter[2] = time.time()
                            cursor.execute("UPDATE economy SET watchtime=? WHERE id=?", ((float(result[1]) + (time.time() - chatter[1])), chatter[0]))
                            chatter[1] = time.time()

                            db.commit()
                    db.close()

            else:
                live = False

    # thread to wait to restart input bot
    async def snackWait(self):
        await asyncio.sleep(random.randint(600, 900))
        chatPlays.snackShot = False
        updateSnatus()


    # thread to wait to restart input bot
    async def empWait(self):
        await asyncio.sleep(random.randint(600, 1800))
        chatPlays.landminesActive = False

    # thread to wait to remod a mod after timing them out
    async def remod(self, id, duration):
        print("waitng for timeout to end")
        await asyncio.sleep(duration)
        print("timeout ended, trying to remod")

        modIds = []
        while str(id) not in modIds:
            connected = False
            while not connected:
                try:
                    response = requests.get("https://api.twitch.tv/helix/users", headers={"Client-ID": clientID, "Authorization": f"Bearer {accessToken}"})
                    rateLimit = response.headers.get("Ratelimit-Remaining")
                    if rateLimit != "0":
                        response = requests.post("https://api.twitch.tv/helix/moderation/moderators?broadcaster_id=" + getBroadcasterId(yourChannelName) + "&user_id=" + id ,headers={"Authorization": f"Bearer {accessToken}", "Client-Id": clientID})
                        response = requests.get("https://api.twitch.tv/helix/moderation/moderators?broadcaster_id=" + getBroadcasterId(yourChannelName),headers={"Authorization": f"Bearer {accessToken}", "Client-Id": clientID})
                        modIds = []
                        for mod in response.json().get("data"):
                            modIds += [str(mod.get("user_id"))]
                        connected = True
                        print("remodded")
                    else:
                        await asyncio.sleep(5)
                except:
                    await asyncio.sleep(5)
