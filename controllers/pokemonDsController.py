# imports
import random
import time

from controllers import pokemonGbaController
from libraries import chatPlays
from libraries.autoStream import *
import aiohttp

# setting up variables
pressTime = (random.randint(1, 3) / 10)
lightPressTime = (random.randint(1, 3) / 100)
holdTime = random.randint(5, 10)

# reading config
config = configparser.ConfigParser()
config.read(os.path.abspath((os.path.join(directory, "config.ini"))))
landmines = config.get("twitch", "landmines", fallback = "").strip("[]").split(", ")

# makes inputs when no one has typed in chat for a while
async def idleBot():
    
    # checks if idle bot is supposed to be on and if no one has chatted
    while chatPlays.idleBotPlaying:
        if chatPlays.timeSinceLastMessage <= (time.time() - 5 * 60):

            # tell obs to show idle bot is active
            if not chatPlays.idleBotStatus:
                chatPlays.idleBotStatus = True
                await chatPlays.updateSnatus()

            # time between inputs
            await asyncio.sleep(random.randint(1, 10) / 10)

            # 25% chance of non directionals
            dice = random.randint(1, 4)
            if dice == 1:
                input = random.choice([await r(pressTime), await l(pressTime), await pokemonGbaController.a(pressTime), await pokemonGbaController.b(pressTime), await x(pressTime), await y(pressTime), await pokemonGbaController.select(pressTime), await pokemonGbaController.start(pressTime)])
                input()
            # 75% chance of directionals
            else:
                input = random.choice([await pokemonGbaController.up(pressTime), await pokemonGbaController.down(pressTime), await pokemonGbaController.left(pressTime), await pokemonGbaController.right(pressTime), await pokemonGbaController.wander(4, holdTime)])
                input()
        else:
            if chatPlays.idleBotStatus:
                chatPlays.idleBotStatus = False
                await chatPlays.updateSnatus()
            await asyncio.sleep(5)

# makes inputs every so often
async def inputBot():

    # checks if conditions are right
    while chatPlays.inputBotPlaying:
        if not chatPlays.snackShot or chatPlays.snackHealed:

            # sleepy snack controls
            if chatPlays.currentSnack == "sleepy":
                
                # time between inputs
                await asyncio.sleep(random.randint(30, 360))

                # 5% chance of no action
                dice = random.randint(1, 100)
                if dice < 96:
                    input = random.choice([await pokemonGbaController.up(pressTime), await pokemonGbaController.down(pressTime), await pokemonGbaController.left(pressTime), await pokemonGbaController.right(pressTime), await pokemonGbaController.holdUp(holdTime), await pokemonGbaController.holdDown(holdTime), await pokemonGbaController.holdLeft(holdTime), await pokemonGbaController.holdDown(holdTime), await pokemonGbaController.a(pressTime), await pokemonGbaController.holdA(holdTime), await pokemonGbaController.b(pressTime), await pokemonGbaController.holdB(), await x(pressTime), await y(pressTime), await l(pressTime), await r(pressTime), await pokemonGbaController.select(pressTime), await pokemonGbaController.start(pressTime), await pokemonGbaController.wander(2, holdTime)])
                    input()

            # chris snack controls
            elif chatPlays.currentSnack == "chris":
                
                # time between inputs
                await asyncio.sleep(random.randint(5, 60))

                # 33% chance of no action
                dice = random.randint(1, 3)
                if dice != 1:
                    input = random.choice([await pokemonGbaController.up(pressTime), await pokemonGbaController.down(pressTime), await pokemonGbaController.left(pressTime), await pokemonGbaController.right(pressTime), await pokemonGbaController.holdUp(holdTime), await pokemonGbaController.holdDown(holdTime), await pokemonGbaController.holdLeft(holdTime), await pokemonGbaController.holdDown(holdTime), await pokemonGbaController.a(pressTime), await pokemonGbaController.holdA(holdTime), await pokemonGbaController.b(pressTime), await pokemonGbaController.holdB(), await x(pressTime), await y(pressTime), await l(pressTime), await r(pressTime), await pokemonGbaController.select(pressTime), await pokemonGbaController.start(pressTime), await pokemonGbaController.wander(2, holdTime)])
                    input()
                        
            # burst snack controls
            elif chatPlays.currentSnack == "burst":
                
                # time between inputs
                await asyncio.sleep(random.randint(150, 450))

                # 10% chance of no action
                dice = random.randint(1, 10)
                if dice != 1:
                    for i in range(5):
                        input = random.choice([await pokemonGbaController.up(pressTime), await pokemonGbaController.down(pressTime), await pokemonGbaController.left(pressTime), await pokemonGbaController.right(pressTime), await pokemonGbaController.holdUp(holdTime), await pokemonGbaController.holdDown(holdTime), await pokemonGbaController.holdLeft(holdTime), await pokemonGbaController.holdDown(holdTime), await pokemonGbaController.a(pressTime), await pokemonGbaController.holdA(holdTime), await pokemonGbaController.b(pressTime), await pokemonGbaController.holdB(), await x(pressTime), await y(pressTime), await l(pressTime), await r(pressTime), await pokemonGbaController.select(pressTime), await pokemonGbaController.start(pressTime), await pokemonGbaController.wander(2, holdTime)])
                        input()

            # silly snack controls
            elif chatPlays.currentSnack == "silly":
                
                # time between inputs
                await asyncio.sleep(random.randint(5, 40))

                # 33% chance of no action
                dice = random.randint(1, 3)
                if dice != 1:
                    input = random.choice([await pokemonGbaController.up(pressTime), await pokemonGbaController.down(pressTime), await pokemonGbaController.left(pressTime), await pokemonGbaController.right(pressTime), await pokemonGbaController.holdUp(holdTime), await pokemonGbaController.holdDown(holdTime), await pokemonGbaController.holdLeft(holdTime), await pokemonGbaController.holdDown(holdTime), await pokemonGbaController.wander(2, holdTime)])
                    input()
            
            # cautious snack controls
            elif chatPlays.currentSnack == "cautious":
                
                # time between inputs
                await asyncio.sleep(random.randint(5, 60))

                # 20% chance of no action
                dice = random.randint(1, 5)
                if dice != 1:
                    input = random.choice([await pokemonGbaController.north(lightPressTime), await pokemonGbaController.south(lightPressTime), await pokemonGbaController.east(lightPressTime), await pokemonGbaController.west(lightPressTime), await pokemonGbaController.b(pressTime), await pokemonGbaController.mashB(pressTime)])
                    input()

            # sonic snack controls
            elif chatPlays.currentSnack == "sonic":

                # time between inputs
                await asyncio.sleep(random.randint(10, 30))

                # 10% chance of no action
                dice = random.randint(1, 10)
                if dice != 1:
                    input = random.choice([await pokemonGbaController.north(lightPressTime), await pokemonGbaController.south(lightPressTime), await pokemonGbaController.east(lightPressTime), await pokemonGbaController.west(lightPressTime), await pokemonGbaController.mashA(pressTime), await pokemonGbaController.mashB(pressTime), await pokemonGbaController.wander(4, holdTime), await pokemonGbaController.upWander(holdTime), await pokemonGbaController.downWander(holdTime), await pokemonGbaController.leftWander(holdTime), await pokemonGbaController.rightWander(holdTime)])
                    input()

# chat controls
async def controller(data):
    
    # makes sure chat is playing
    chatPlays.noRecentMessages = False
    await chatPlays.updateSnatus()
    if chatPlays.chatPlaying is True:

        # getting current viewer count
        connected = False
        while not connected:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://api.twitch.tv/helix/users", headers={"Client-ID": clientID, "Authorization": "Bearer " + accessToken}) as response:
                        rateLimit = response.headers.get("Ratelimit-Remaining")
                        if rateLimit != "0":
                            userResponse = await response.json()

                            async with session.get("https://api.twitch.tv/helix/streams?user_id=" + userResponse.get("data")[0].get("id"), headers={"Client-ID": chatPlays.clientID, "Authorization": "Bearer " + chatPlays.accessToken}) as streamResponse:
                                streamResponse = await streamResponse.json()
                                connected = True
                        else:
                            await asyncio.sleep(5)
            except:
                await asyncio.sleep(5)

        # setting up odds based on view count
        try:
            if int(streamResponse.get("data")[0].get("viewer_count")) > 100:
                dice = (random.randint(1, 10))
            elif int(streamResponse.get("data")[0].get("viewer_count")) > 50:
                dice = random.randint(1, 5)
            elif int(streamResponse.get("data")[0].get("viewer_count")) > 35:
                dice = random.randint(1, 5)
                if dice == 1 or dice == 2:
                    dice = 1
            elif int(streamResponse.get("data")[0].get("viewer_count")) > 20:
                dice = (random.randint(1, 4))
                if dice != 1:
                    dice = 1
            else:
                dice = 1
        except:
            dice = 1

        # making input
        if dice == 1:
            message = data.lower()
            dice = random.randint(1, 40)

            # 2.5% chance of random input
            if dice == 1:
                input = random.choice([await pokemonGbaController.up(pressTime), await pokemonGbaController.down(pressTime), await pokemonGbaController.left(pressTime), await pokemonGbaController.right(pressTime), await pokemonGbaController.holdUp(holdTime), await pokemonGbaController.holdDown(holdTime), await pokemonGbaController.holdLeft(holdTime), await pokemonGbaController.holdRight(holdTime), await pokemonGbaController.a(pressTime), await pokemonGbaController.holdA(holdTime), await pokemonGbaController.mashA(pressTime), await pokemonGbaController.b(pressTime), await pokemonGbaController.holdB(), await pokemonGbaController.mashB(pressTime), await x(pressTime), await y(pressTime), await pokemonGbaController.select(pressTime), await pokemonGbaController.start(pressTime), await l(pressTime), await r(pressTime), await pokemonGbaController.stop(), await pokemonGbaController.wander(4, holdTime), await pokemonGbaController.north(lightPressTime), await pokemonGbaController.south(lightPressTime), await pokemonGbaController.west(lightPressTime), await pokemonGbaController.east(lightPressTime), await pokemonGbaController.upWander(holdTime), await pokemonGbaController.downWander(holdTime), await pokemonGbaController.leftWander(holdTime), await pokemonGbaController.rightWander(holdTime)])
                input()

            # 2.5% chance of opposite input
            elif dice == 2:
                if message == "a":
                    await pokemonGbaController.b(pressTime)
                elif "hold a" in message:
                    await pokemonGbaController.holdB()
                elif "mash a" in message:
                    await pokemonGbaController.mashB(pressTime)
                elif message == "b":
                    await pokemonGbaController.a(pressTime)
                elif "hold b" in message:
                    await pokemonGbaController.holdA(holdTime)
                elif "mash b" in message:
                    await pokemonGbaController.mashA(pressTime)
                elif message == "x":
                    await y(pressTime)
                elif message == "y":
                    await x(pressTime)
                elif "select" in message:
                    await pokemonGbaController.start(pressTime)
                elif "start" in message:
                    await pokemonGbaController.select(pressTime)
                elif message == "l":
                    await r(pressTime)
                elif message == "r":
                    await l(pressTime)
                elif "up wander" in message:
                    await pokemonGbaController.downWander(holdTime)
                elif "down wander" in message:
                    await pokemonGbaController.upWander(holdTime)
                elif "left wander" in message:
                    await pokemonGbaController.rightWander(holdTime)
                elif "right wander" in message:
                    await pokemonGbaController.leftWander(holdTime)
                elif "wander" in message:
                    await pokemonGbaController.stop()
                elif "hold up" in message:
                    await pokemonGbaController.holdDown(holdTime)
                elif "hold down" in message:
                    await pokemonGbaController.holdUp(holdTime)
                elif "hold left" in message:
                    await pokemonGbaController.holdRight(holdTime)
                elif "hold right" in message:
                    await pokemonGbaController.holdLeft(holdTime)
                elif "north" in message:
                    await pokemonGbaController.south(lightPressTime)
                elif "south" in message:
                    await pokemonGbaController.north(lightPressTime)
                elif "west" in message:
                    await pokemonGbaController.east(lightPressTime)
                elif "east" in message:
                    await pokemonGbaController.west(lightPressTime)
                elif "up" in message:
                    await pokemonGbaController.down(pressTime)
                elif "down" in message:
                    await pokemonGbaController.up(pressTime)
                elif "left" in message:
                    await pokemonGbaController.right(pressTime)
                elif "right" in message:
                    await pokemonGbaController.left(pressTime)
                elif "stop" in message:
                    await pokemonGbaController.upWander(holdTime)
                    await pokemonGbaController.downWander(holdTime)
                    await pokemonGbaController.leftWander(holdTime)
                    await pokemonGbaController.rightWander(holdTime)
                elif landmines[0] in message or landmines[1] in message or landmines[2] in message or landmines[3] in message or landmines[4] in message:
                    if chatPlays.landminesActive:
                        await pokemonGbaController.stop()

            # 95% chance of correct inputs
            else:
                if message == "a":
                    await pokemonGbaController. a(pressTime)
                elif "hold a" in message:
                    await pokemonGbaController.holdA(holdTime)
                elif "mash a" in message:
                    await pokemonGbaController.mashA(pressTime)
                elif message == "b":
                    await pokemonGbaController.b(pressTime)
                elif "hold b" in message:
                    await pokemonGbaController.holdB()
                elif "mash b" in message:
                    await pokemonGbaController.mashB(pressTime)
                elif message == "x":
                    await x(pressTime)
                elif message == "y":
                    await y(pressTime)
                elif "select" in message:
                    await pokemonGbaController.select(pressTime)
                elif "start" in message:
                    await pokemonGbaController.start(pressTime)
                elif message == "l":
                    await l(pressTime)
                elif message == "r":
                    await r(pressTime)
                elif "up wander" in message:
                    await pokemonGbaController.upWander(holdTime)
                elif "down wander" in message:
                    await pokemonGbaController.downWander(holdTime)
                elif "left wander" in message:
                    await pokemonGbaController.leftWander(holdTime)
                elif "right wander" in message:
                    await pokemonGbaController.rightWander(holdTime)
                elif "wander" in message:
                    await pokemonGbaController.wander(4, holdTime)
                elif "hold up" in message:
                    await pokemonGbaController.holdUp(holdTime)
                elif "hold down" in message:
                    await pokemonGbaController.holdDown(holdTime)
                elif "hold left" in message:
                    await pokemonGbaController.holdLeft(holdTime)
                elif "hold right" in message:
                    await pokemonGbaController.holdRight(holdTime)
                elif "north" in message:
                    await pokemonGbaController.north(lightPressTime)
                elif "south" in message:
                    await pokemonGbaController.south(lightPressTime)
                elif "west" in message:
                    await pokemonGbaController.west(lightPressTime)
                elif "east" in message:
                    await pokemonGbaController.east(lightPressTime)
                elif "up" in message:
                    await pokemonGbaController.up(pressTime)
                elif "down" in message:
                    await pokemonGbaController.down(pressTime)
                elif "left" in message:
                    await pokemonGbaController.left(pressTime)
                elif "right" in message:
                    await pokemonGbaController.right(pressTime)
                elif "stop" in message:
                    await pokemonGbaController.stop()
                elif landmines[0] in message or landmines[1] in message or landmines[2] in message or landmines[3] in message or landmines[4] in message:
                    if chatPlays.landminesActive:
                        await pokemonGbaController.wander(2, holdTime)

# define controls down here
async def x(pressTime):
    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("O"), pressTime)

async def y(pressTime):
    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("V"), pressTime)

async def l(pressTime):
    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("Q"), pressTime)

async def r(pressTime):
    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("E"), pressTime)