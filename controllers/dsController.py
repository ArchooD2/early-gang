# imports
import random
import time
from controllers import pokemonGbaController
from libraries import chatPlays
from libraries.autoStream import *
import aiohttp

# setting up variables
pressTime = (random.randint(5, 12) / 10)
lightPressTime = (random.randint(1, 3) / 100)
holdTime = random.randint(5, 10)
slightlyDifferentHoldTimeForWhateverFuckingReason = (random.randint(9, 15)/ 10)

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
                if dice == 1:
                    dice = random.randint(1, 8)
                    match dice:
                        case 1:
                            await pokemonGbaController.a(pressTime)
                        case 2:
                            await pokemonGbaController.b(pressTime)
                        case 3:
                            await x(pressTime)
                        case 4:
                            await y(pressTime)
                        case 5:
                            await pokemonGbaController.select(pressTime)
                        case 6:
                            await pokemonGbaController.start(pressTime)
                        case 7:
                            await l(pressTime)
                        case 8:
                            await r(pressTime)

            # 75% chance of directionals
            else:
                dice = random.randint(1, 5)
                match dice:
                    case 1:
                        await pokemonGbaController.up(pressTime)
                    case 2:
                        await pokemonGbaController.down(pressTime)
                    case 3:
                        await pokemonGbaController.left(pressTime)
                    case 4:
                        await pokemonGbaController.right(pressTime)
                    case 5:
                        await pokemonGbaController.wander(4, holdTime)
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
                    dice = random.randint(1, 19)
                    match dice:
                        case 1:
                            await pokemonGbaController.up(pressTime)
                        case 2:
                            await pokemonGbaController.down(pressTime)
                        case 3:
                            await pokemonGbaController.left(pressTime)
                        case 4:
                            await pokemonGbaController.right(pressTime)
                        case 5:
                            await pokemonGbaController.holdUp(holdTime)
                        case 6:
                            await pokemonGbaController.holdDown(holdTime)
                        case 7:
                            await pokemonGbaController.holdLeft(holdTime)
                        case 8:
                            await pokemonGbaController.holdDown(holdTime)
                        case 9:
                            await pokemonGbaController.a(pressTime)
                        case 10:
                            await pokemonGbaController.holdA(holdTime)
                        case 11:
                            await pokemonGbaController.b(pressTime)
                        case 12:
                            await pokemonGbaController.holdB()
                        case 13:
                            await x(pressTime)
                        case 14:
                            await y(pressTime)
                        case 15:
                            await l(pressTime)
                        case 16:
                            await r(pressTime)
                        case 17:
                            await pokemonGbaController.select(pressTime)
                        case 18:
                            await pokemonGbaController.start(pressTime)
                        case 19:
                            await pokemonGbaController.wander(2, holdTime)

            # chris snack controls
            elif chatPlays.currentSnack == "chris":
                
                # time between inputs
                await asyncio.sleep(random.randint(5, 60))

                # 33% chance of no action
                dice = random.randint(1, 3)
                if dice != 1:
                    dice = random.randint(1, 19)
                    match dice:
                        case 1:
                            await pokemonGbaController.up(pressTime)
                        case 2:
                            await pokemonGbaController.down(pressTime)
                        case 3:
                            await pokemonGbaController.left(pressTime)
                        case 4:
                            await pokemonGbaController.right(pressTime)
                        case 5:
                            await pokemonGbaController.holdUp(holdTime)
                        case 6:
                            await pokemonGbaController.holdDown(holdTime)
                        case 7:
                            await pokemonGbaController.holdLeft(holdTime)
                        case 8:
                            await pokemonGbaController.holdDown(holdTime)
                        case 9:
                            await pokemonGbaController.a(pressTime)
                        case 10:
                            await pokemonGbaController.holdA(holdTime)
                        case 11:
                            await pokemonGbaController.b(pressTime)
                        case 12:
                            await pokemonGbaController.holdB()
                        case 13:
                            await x(pressTime)
                        case 14:
                            await y(pressTime)
                        case 15:
                            await l(pressTime)
                        case 16:
                            await r(pressTime)
                        case 17:
                            await pokemonGbaController.select(pressTime)
                        case 18:
                            await pokemonGbaController.start(pressTime)
                        case 19:
                            await pokemonGbaController.wander(2, holdTime)
                        
            # burst snack controls
            elif chatPlays.currentSnack == "burst":
                
                # time between inputs
                await asyncio.sleep(random.randint(150, 450))

                # 10% chance of no action
                dice = random.randint(1, 10)
                if dice != 1:
                    for i in range(5):
                        dice = random.randint(1, 19)
                        match dice:
                            case 1:
                                await pokemonGbaController.up(pressTime)
                            case 2:
                                await pokemonGbaController.down(pressTime)
                            case 3:
                                await pokemonGbaController.left(pressTime)
                            case 4:
                                await pokemonGbaController.right(pressTime)
                            case 5:
                                await pokemonGbaController.holdUp(holdTime)
                            case 6:
                                await pokemonGbaController.holdDown(holdTime)
                            case 7:
                                await pokemonGbaController.holdLeft(holdTime)
                            case 8:
                                await pokemonGbaController.holdDown(holdTime)
                            case 9:
                                await pokemonGbaController.a(pressTime)
                            case 10:
                                await pokemonGbaController.holdA(holdTime)
                            case 11:
                                await pokemonGbaController.b(pressTime)
                            case 12:
                                await pokemonGbaController.holdB()
                            case 13:
                                await x(pressTime)
                            case 14:
                                await y(pressTime)
                            case 15:
                                await l(pressTime)
                            case 16:
                                await r(pressTime)
                            case 17:
                                await pokemonGbaController.select(pressTime)
                            case 18:
                                await pokemonGbaController.start(pressTime)
                            case 19:
                                await pokemonGbaController.wander(2, holdTime)

            # silly snack controls
            elif chatPlays.currentSnack == "silly":
                
                # time between inputs
                await asyncio.sleep(random.randint(5, 40))

                # 33% chance of no action
                dice = random.randint(1, 3)
                if dice != 1:
                    dice = random.randint(1, 9)
                    match dice:
                        case 1:
                            await pokemonGbaController.up(pressTime)
                        case 2:
                            await pokemonGbaController.down(pressTime)
                        case 3:
                            await pokemonGbaController.left(pressTime)
                        case 4:
                            await pokemonGbaController.right(pressTime)
                        case 5:
                            await pokemonGbaController.holdUp(holdTime)
                        case 6:
                            await pokemonGbaController.holdDown(holdTime)
                        case 7:
                            await pokemonGbaController.holdLeft(holdTime)
                        case 8:
                            await pokemonGbaController.holdDown(holdTime)
                        case 9:
                            await pokemonGbaController.wander(2, holdTime)
            
            # cautious snack controls
            elif chatPlays.currentSnack == "cautious":
                
                # time between inputs
                await asyncio.sleep(random.randint(5, 60))

                # 20% chance of no action
                dice = random.randint(1, 5)
                if dice != 1:
                    dice = random.randint(1, 6)
                    match dice:
                        case 1:
                            await pokemonGbaController.north(lightPressTime)
                        case 2:
                            await pokemonGbaController.south(lightPressTime)
                        case 3:
                            await pokemonGbaController.east(lightPressTime)
                        case 4:
                            await pokemonGbaController.west(lightPressTime)
                        case 5:
                            await pokemonGbaController.b(pressTime)
                        case 6:
                            await pokemonGbaController.mashB(pressTime)

            # sonic snack controls
            elif chatPlays.currentSnack == "sonic":

                # time between inputs
                await asyncio.sleep(random.randint(10, 30))

                # 10% chance of no action
                dice = random.randint(1, 10)
                if dice != 1:
                    dice = random.randint(1, 6)
                    match dice:
                        case 1:
                            await pokemonGbaController.north(lightPressTime)
                        case 2:
                            await pokemonGbaController.south(lightPressTime)
                        case 3:
                            await pokemonGbaController.east(lightPressTime)
                        case 4:
                            await pokemonGbaController.west(lightPressTime)
                        case 5:
                            await pokemonGbaController.mashA(pressTime)
                        case 6:
                            await pokemonGbaController.mashB(pressTime)
                        case 7:
                            await pokemonGbaController.wander(4, holdTime)
                        case 8:
                            await pokemonGbaController.upWander(holdTime)
                        case 9:
                            await pokemonGbaController.downWander(holdTime)
                        case 10:
                            await pokemonGbaController.leftWander(holdTime)
                        case 11:
                            await pokemonGbaController.rightWander(holdTime)
        else:
            await asyncio.sleep(5)

# chat controls
async def controller(message):
    # makes sure chat is playing
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
            message = message.lower()
            dice = random.randint(1, 40)

            # 2.5% chance of random input
            if dice == 1 and (message == "a" or "shoot" in message or "left+" in message or "right+" in message or "down+" in message or "up+" in message or "hold a" in message or "mash a" in message or message == "b" or "hold b" in message or "mash b" in message or message == "x" or message == "y" or "select" in message or "start" in message or message == "l" or message == "r" or "up wander" in message or "down wander" in message or "left wander" in message or "right wander" in message or "wander" in message or "hold up" in message or "hold down" in message or "hold left" in message or "hold right" in message or "north" in message or "south" in message or "west" in message or "east" in message or "up" in message or "down" in message or "left" in message or "right" in message or "stop" in message or landmines[0] in message or landmines[1] in message or landmines[2] in message or landmines[3] in message or landmines[4] in message):
                dice = random.randint(1, 34)
                match dice:
                    case 1:
                        await pokemonGbaController.up(pressTime)
                    case 2:
                        await pokemonGbaController.down(pressTime)
                    case 3:
                        await pokemonGbaController.left(pressTime)
                    case 4:
                        await pokemonGbaController.right(pressTime)
                    case 5:
                        await pokemonGbaController.holdUp(holdTime)
                    case 6:
                        await pokemonGbaController.holdDown(holdTime)
                    case 7:
                        await pokemonGbaController.holdLeft(holdTime)
                    case 8:
                        await pokemonGbaController.holdRight(holdTime)
                    case 9:
                        await pokemonGbaController.a(pressTime)
                    case 10:
                        await pokemonGbaController.holdA(holdTime)
                    case 11:
                        await pokemonGbaController.mashA(pressTime)
                    case 12:
                        await pokemonGbaController.b(pressTime)
                    case 13:
                        await pokemonGbaController.holdB()
                    case 14:
                        await pokemonGbaController.mashB(pressTime)
                    case 15:
                        await x(pressTime)
                    case 16:
                        await y(pressTime)
                    case 17:
                        await pokemonGbaController.select(pressTime)
                    case 18:
                        await pokemonGbaController.start(pressTime)
                    case 19:
                        await l(pressTime)
                    case 20:
                        await r(pressTime)
                    case 21:
                        await pokemonGbaController.stop()
                    case 22:
                        await pokemonGbaController.wander(4, holdTime)
                    case 23:
                        await pokemonGbaController.north(lightPressTime)
                    case 24:
                        await pokemonGbaController.south(lightPressTime)
                    case 25:
                        await pokemonGbaController.west(lightPressTime)
                    case 26:
                        await pokemonGbaController.east(lightPressTime)
                    case 27:
                        await pokemonGbaController.upWander(holdTime)
                    case 28:
                        await pokemonGbaController.downWander(holdTime)
                    case 29:
                        await pokemonGbaController.leftWander(holdTime)
                    case 30:
                        await pokemonGbaController.rightWander(holdTime)
                    case 31:
                        await leftPlus(slightlyDifferentHoldTimeForWhateverFuckingReason)
                    case 32:
                        await rightPlus(slightlyDifferentHoldTimeForWhateverFuckingReason)
                    case 33:
                        await upPlus(slightlyDifferentHoldTimeForWhateverFuckingReason)
                    case 34:
                        await downPlus(slightlyDifferentHoldTimeForWhateverFuckingReason)
            # 2.5% chance of opposite input
            elif dice == 2:
                if message == "a" or "shoot" in message:
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
                elif "up+" in message:
                    await downPlus(slightlyDifferentHoldTimeForWhateverFuckingReason)
                elif "down+" in message:
                    await upPlus(slightlyDifferentHoldTimeForWhateverFuckingReason)
                elif "left+" in message:
                    await rightPlus(slightlyDifferentHoldTimeForWhateverFuckingReason)
                elif "right+" in message:
                    await leftPlus(slightlyDifferentHoldTimeForWhateverFuckingReason)
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
                if message == "a" or "shoot" in message:
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
                elif "up+" in message:
                    await upPlus(slightlyDifferentHoldTimeForWhateverFuckingReason)
                elif "down+" in message:
                    await downPlus(slightlyDifferentHoldTimeForWhateverFuckingReason)
                elif "left+" in message:
                    await leftPlus(slightlyDifferentHoldTimeForWhateverFuckingReason)
                elif "right+" in message:
                    await rightPlus(slightlyDifferentHoldTimeForWhateverFuckingReason)
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

async def leftPlus(holdTime):
    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("A"), holdTime)

async def rightPlus(holdTime):
    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("D"), holdTime)

async def upPlus(holdTime):
    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("W"), holdTime)

async def downPlus(holdTime):
    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("S"), holdTime)