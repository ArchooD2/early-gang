# imports
import time
from libraries import chatPlays
from libraries.autoStream import *
import random
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
                dice = random.randint(1, 6)
                match dice:
                    case 1:
                        await a(pressTime)
                    case 2:
                        await b(pressTime)
                    case 3:
                        await x(pressTime)
                    case 4:
                        await y(pressTime)
                    case 5:
                        await select(pressTime)
                    case 6:
                        await start(pressTime)

            # 75% chance of directionals
            else:
                dice = random.randint(1, 5)
                match dice:
                    case 1:
                        await up(pressTime)
                    case 2:
                        await down(pressTime)
                    case 3:
                        await left(pressTime)
                    case 4:
                        await right(pressTime)
                    case 5:
                        await wander(4, holdTime)

        # tell obs idle bot is inactive
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
                time.sleep(random.randint(30, 360))

                # 5% chance of no action
                dice = random.randint(1, 100)
                if dice < 96:
                    dice = random.randint(1, 17)
                    match dice:
                        case 1:
                            await up(pressTime)
                        case 2:
                            await down(pressTime)
                        case 3:
                            await left(pressTime)
                        case 4:
                            await right(pressTime)
                        case 5:
                            await holdUp(holdTime)
                        case 6:
                            await holdDown(holdTime)
                        case 7:
                            await holdLeft(holdTime)
                        case 8:
                            await holdDown(holdTime)
                        case 9:
                            await a(pressTime)
                        case 10:
                            await holdA(holdTime)
                        case 11:
                            await b(pressTime)
                        case 12:
                            await holdB()
                        case 13:
                            await x(pressTime)
                        case 14:
                            await y(pressTime)
                        case 15:
                            await select(pressTime)
                        case 16:
                            await start(pressTime)
                        case 17:
                            await wander(2, holdTime)

            # chris snack controls
            elif chatPlays.currentSnack == "chris":

                # time between inputs
                time.sleep(random.randint(5, 60))

                # 33% chance of no action
                dice = random.randint(1, 3)
                if dice != 1:
                    match dice:
                        case 1:
                            await up(pressTime)
                        case 2:
                            await down(pressTime)
                        case 3:
                            await left(pressTime)
                        case 4:
                            await right(pressTime)
                        case 5:
                            await holdUp(holdTime)
                        case 6:
                            await holdDown(holdTime)
                        case 7:
                            await holdLeft(holdTime)
                        case 8:
                            await holdDown(holdTime)
                        case 9:
                            await a(pressTime)
                        case 10:
                            await holdA(holdTime)
                        case 11:
                            await b(pressTime)
                        case 12:
                            await holdB()
                        case 13:
                            await x(pressTime)
                        case 14:
                            await y(pressTime)
                        case 15:
                            await select(pressTime)
                        case 16:
                            await start(pressTime)
                        case 17:
                            await wander(2, holdTime)

            # burst snack controls
            elif chatPlays.currentSnack == "burst":

                # time between inputs
                time.sleep(random.randint(150, 450))

                # 10% chance of no action
                dice = random.randint(1, 10)
                if dice != 1:
                    for i in range(5):
                        dice = random.randint(1, 17)
                        match dice:
                            case 1:
                                await up(pressTime)
                            case 2:
                                await down(pressTime)
                            case 3:
                                await left(pressTime)
                            case 4:
                                await right(pressTime)
                            case 5:
                                await holdUp(holdTime)
                            case 6:
                                await holdDown(holdTime)
                            case 7:
                                await holdLeft(holdTime)
                            case 8:
                                await holdDown(holdTime)
                            case 9:
                                await a(pressTime)
                            case 10:
                                await holdA(holdTime)
                            case 11:
                                await b(pressTime)
                            case 12:
                                await holdB()
                            case 13:
                                await x(pressTime)
                            case 14:
                                await y(pressTime)
                            case 15:
                                await select(pressTime)
                            case 16:
                                await start(pressTime)
                            case 17:
                                await wander(2, holdTime)

            # silly snack controls
            elif chatPlays.currentSnack == "silly":

                # time between inputs
                time.sleep(random.randint(5, 40))

                # 33% chance of no action
                dice = random.randint(1, 3)
                if dice != 1:
                    dice = random.randint(1, 9)
                    match dice:
                        case 1:
                            await up(pressTime)
                        case 2:
                            await down(pressTime)
                        case 3:
                            await left(pressTime)
                        case 4:
                            await right(pressTime)
                        case 5:
                            await holdUp(holdTime)
                        case 6:
                            await holdDown(holdTime)
                        case 7:
                            await holdLeft(holdTime)
                        case 8:
                            await holdDown(holdTime)
                        case 9:
                            await wander(2, holdTime)

            # cautious snack controls
            elif chatPlays.currentSnack == "cautious":

                # time between inputs
                time.sleep(random.randint(5, 60))

                # 20% chance of no action
                dice = random.randint(1, 5)
                if dice != 1:
                    dice = random.randint(1, 6)
                    match dice:
                        case 1:
                            await north(lightPressTime)
                        case 2:
                            await south(lightPressTime)
                        case 3:
                            await east(lightPressTime)
                        case 4:
                            await west(lightPressTime)
                        case 5:
                            await b(pressTime)
                        case 6:
                            await mashB(pressTime)

            # sonic snack controls
            elif chatPlays.currentSnack == "sonic":

                # time between inputs
                time.sleep(random.randint(10, 30))

                # 10% chance of no action
                dice = random.randint(1, 10)
                if dice != 1:
                    dice = random.randint(1, 6)
                    match dice:
                        case 1:
                            await north(lightPressTime)
                        case 2:
                            await south(lightPressTime)
                        case 3:
                            await east(lightPressTime)
                        case 4:
                            await west(lightPressTime)
                        case 5:
                            await mashA(pressTime)
                        case 6:
                            await mashB(pressTime)
                        case 7:
                            await wander(4, holdTime)
                        case 8:
                            await upWander(holdTime)
                        case 9:
                            await downWander(holdTime)
                        case 10:
                            await leftWander(holdTime)
                        case 11:
                            await rightWander(holdTime)
        else:
            await asyncio.sleep(5)

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
            if dice == 1 and (message == "a" or "hold a" in message or "mash a" in message or message == "b" or "hold b" in message or "mash b" in message or message == "x" or message == "y" or "select" in message or "start" in message or "up wander" in message or "down wander" in message or "left wander" in message or "right wander" in message or "wander" in message or "hold up" in message or "hold down" in message or "hold left" in message or "hold right" in message or "north" in message or "south" in message or "west" in message or "east" in message or "up" in message or "down" in message or "left" in message or "right" in message or "stop" in message or landmines[0] in message or landmines[1] in message or landmines[2] in message or landmines[3] in message or landmines[4] in message):
                dice = random.randint(1, 28)
                match dice:
                    case 1:
                        await up(pressTime)
                    case 2:
                        await down(pressTime)
                    case 3:
                        await left(pressTime)
                    case 4:
                        await right(pressTime)
                    case 5:
                        await holdUp(holdTime)
                    case 6:
                        await holdDown(holdTime)
                    case 7:
                        await holdLeft(holdTime)
                    case 8:
                        await holdRight(holdTime)
                    case 9:
                        await a(pressTime)
                    case 10:
                        await holdA(holdTime)
                    case 11:
                        await mashA(pressTime)
                    case 12:
                        await b(pressTime)
                    case 13:
                        await holdB()
                    case 14:
                        await mashB(pressTime)
                    case 15:
                        await x(pressTime)
                    case 16:
                        await y(pressTime)
                    case 17:
                        await select(pressTime)
                    case 18:
                        await start(pressTime)
                    case 19:
                        await stop()
                    case 20:
                        await wander(4, holdTime)
                    case 21:
                        await north(lightPressTime)
                    case 22:
                        await south(lightPressTime)
                    case 23:
                        await west(lightPressTime)
                    case 24:
                        await east(lightPressTime)
                    case 25:
                        await upWander(holdTime)
                    case 26:
                        await downWander(holdTime)
                    case 27:
                        await leftWander(holdTime)
                    case 28:
                        await rightWander(holdTime)

            # 2.5% chance of opposite input
            elif dice == 2:
                if message == "a":
                    await b(pressTime)
                elif "hold a" in message:
                    await holdB()
                elif "mash a" in message:
                    await mashB(pressTime)
                elif message == "b":
                    await a(pressTime)
                elif "hold b" in message:
                    await holdA(holdTime)
                elif "mash b" in message:
                    await mashA(pressTime)
                elif message == "x":
                    await y(pressTime)
                elif message == "y":
                    await x(pressTime)
                elif "select" in message:
                    await start(pressTime)
                elif "start" in message:
                    await select(pressTime)
                elif "up wander" in message:
                    await downWander(holdTime)
                elif "down wander" in message:
                    await upWander(holdTime)
                elif "left wander" in message:
                    await rightWander(holdTime)
                elif "right wander" in message:
                    await leftWander(holdTime)
                elif "wander" in message:
                    await stop()
                elif "hold up" in message:
                    await holdDown(holdTime)
                elif "hold down" in message:
                    await holdUp(holdTime)
                elif "hold left" in message:
                    await holdRight(holdTime)
                elif "hold right" in message:
                    await holdLeft(holdTime)
                elif "north" in message:
                    await south(lightPressTime)
                elif "south" in message:
                    await north(lightPressTime)
                elif "west" in message:
                    await east(lightPressTime)
                elif "east" in message:
                    await west(lightPressTime)
                elif "up" in message:
                    await down(pressTime)
                elif "down" in message:
                    await up(pressTime)
                elif "left" in message:
                    await right(pressTime)
                elif "right" in message:
                    await left(pressTime)
                elif "stop" in message:
                    await upWander(holdTime)
                    await downWander(holdTime)
                    await leftWander(holdTime)
                    await rightWander(holdTime)
                elif landmines[0] in message or landmines[1] in message or landmines[2] in message or landmines[3] in message or landmines[4] in message:
                    if chatPlays.landminesActive:
                        await stop()

            # 95% chance of correct inputs
            else:
                if message == "a":
                    await a(pressTime)
                elif "hold a" in message:
                    await holdA(holdTime)
                elif "mash a" in message:
                    await mashA(pressTime)
                elif message == "b":
                    await b(pressTime)
                elif "hold b" in message:
                    await holdB()
                elif "mash b" in message:
                    await mashB(pressTime)
                elif message == "x":
                    await x(pressTime)
                elif message == "y":
                    await y(pressTime)
                elif "select" in message:
                    await select(pressTime)
                elif "start" in message:
                    await start(pressTime)
                elif "up wander" in message:
                    await upWander(holdTime)
                elif "down wander" in message:
                    await downWander(holdTime)
                elif "left wander" in message:
                    await leftWander(holdTime)
                elif "right wander" in message:
                    await rightWander(holdTime)
                elif "wander" in message:
                    await wander(4, holdTime)
                elif "hold up" in message:
                    await holdUp(holdTime)
                elif "hold down" in message:
                    await holdDown(holdTime)
                elif "hold left" in message:
                    await holdLeft(holdTime)
                elif "hold right" in message:
                    await holdRight(holdTime)
                elif "north" in message:
                    await north(lightPressTime)
                elif "south" in message:
                    await south(lightPressTime)
                elif "west" in message:
                    await west(lightPressTime)
                elif "east" in message:
                    await east(lightPressTime)
                elif "up" in message:
                    await up(pressTime)
                elif "down" in message:
                    await down(pressTime)
                elif "left" in message:
                    await left(pressTime)
                elif "right" in message:
                    await right(pressTime)
                elif "stop" in message:
                    await stop()
                elif landmines[0] in message or landmines[1] in message or landmines[2] in message or landmines[3] in message or landmines[4] in message:
                    if chatPlays.landminesActive:
                        await wander(2, holdTime)

# define controls down here
async def a(pressTime):
    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("L"), pressTime)

async def holdA(holdTime):
    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("L"), holdTime)

async def mashA(pressTime):
    mashTime = 0
    while mashTime <= 2:
        await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("L"), pressTime)
        mashTime += pressTime + .3
        await asyncio.sleep(.3)

async def b(pressTime):
    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("K"), pressTime)

async def holdB():
    await chatPlays.holdKey(chatPlays.keyCodes.get("K"))

async def mashB(pressTime):
    mashTime = 0
    while mashTime <= 2:
        await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("K"), pressTime)
        mashTime += pressTime + .3
        await asyncio.sleep(.3)

async def x(pressTime):
    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("I"), pressTime)

async def y(pressTime):
    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("O"), pressTime)

async def select(pressTime):
    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("T"), pressTime)

async def start(pressTime):
    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("G"), pressTime)

async def wander(times, holdTime):
    for i in range(times):
        dice = random.randint(1, 4)
        match dice:
            case 1:
                await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("W"), holdTime)
            case 2:
                await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("A"), holdTime)
            case 3:
                await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("S"), holdTime)
            case 4:
                await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("D"), holdTime)

async def upWander(holdTime):
    for i in range(4):
        dice = random.randint(1, 10)
        if dice == 1 or dice == 2 or dice == 3 or dice == 4:
            await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("W"), holdTime)
        else:
            dice = random.randint(1, 2)
            if dice == 1:
                await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("D"), holdTime)
            else:
                await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("A"), holdTime)

async def downWander(holdTime):
    for i in range(4):
        dice = random.randint(1, 10)
        if dice == 1 or dice == 2 or dice == 3 or dice == 4:
            await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("S"), holdTime)
        else:
            dice = random.randint(1, 2)
            if dice == 1:
                await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("D"), holdTime)
            else:
                await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("A"), holdTime)

async def leftWander(holdTime):
    for i in range(4):
        dice = random.randint(1, 10)
        if dice == 1 or dice == 2 or dice == 3 or dice == 4:
            await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("A"), holdTime)
        else:
            dice = random.randint(1, 2)
            if dice == 1:
                await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("W"), holdTime)
            else:
                await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("S"), holdTime)

async def rightWander(holdTime):
    for i in range(4):
        dice = random.randint(1, 10)
        if dice == 1 or dice == 2 or dice == 3 or dice == 4:
            await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("D"), holdTime)
        else:
            dice = random.randint(1, 2)
            if dice == 1:
                await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("W"), holdTime)
            else:
                await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("S"), holdTime)

async def holdUp(holdTime):
    dice = random.randint(1, 100)
    if dice == 1:
        for i in range(8):
            dice = random.randint(1, 4)
            match dice:
                case 1:
                    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("W"), holdTime)
                case 2:
                    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("A"), holdTime)
                case 3:
                    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("S"), holdTime)
                case 4:
                    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("D"), holdTime)
    else:
        await chatPlays.releaseKey(chatPlays.keyCodes.get("S"))
        await chatPlays.releaseKey(chatPlays.keyCodes.get("A"))
        await chatPlays.releaseKey(chatPlays.keyCodes.get("D"))
        await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("W"), holdTime)

async def holdDown(holdTime):
    dice = random.randint(1, 100)
    if dice == 1:
        for i in range(8):
            dice = random.randint(1, 4)
            match dice:
                case 1:
                    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("W"), holdTime)
                case 2:
                    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("A"), holdTime)
                case 3:
                    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("S"), holdTime)
                case 4:
                    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("D"), holdTime)
    else:
        await chatPlays.releaseKey(chatPlays.keyCodes.get("W"))
        await chatPlays.releaseKey(chatPlays.keyCodes.get("A"))
        await chatPlays.releaseKey(chatPlays.keyCodes.get("D"))
        await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("S"), holdTime)

async def holdLeft(holdTime):
    dice = random.randint(1, 100)
    if dice == 1:
        for i in range(8):
            dice = random.randint(1, 4)
            match dice:
                case 1:
                    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("W"), holdTime)
                case 2:
                    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("A"), holdTime)
                case 3:
                    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("S"), holdTime)
                case 4:
                    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("D"), holdTime)
    else:
        await chatPlays.releaseKey(chatPlays.keyCodes.get("D"))
        await chatPlays.releaseKey(chatPlays.keyCodes.get("S"))
        await chatPlays.releaseKey(chatPlays.keyCodes.get("W"))
        await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("A"), holdTime)

async def holdRight(holdTime):
    dice = random.randint(1, 100)
    if dice == 1:
        for i in range(8):
            dice = random.randint(1, 4)
            match dice:
                case 1:
                    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("W"), holdTime)
                case 2:
                    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("A"), holdTime)
                case 3:
                    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("S"), holdTime)
                case 4:
                    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("D"), holdTime)
    else:
        await chatPlays.releaseKey(chatPlays.keyCodes.get("A"))
        await chatPlays.releaseKey(chatPlays.keyCodes.get("W"))
        await chatPlays.releaseKey(chatPlays.keyCodes.get("S"))
        await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("D"), holdTime)

async def north(lightPressTime):
    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("W"), lightPressTime)

async def south(lightPressTime):
    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("S"), lightPressTime)

async def west(lightPressTime):
    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("A"), lightPressTime)

async def east(lightPressTime):
    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("D"), lightPressTime)

async def up(pressTime):
    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("W"), pressTime)

async def down(pressTime):
    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("S"), pressTime)

async def left(pressTime):
    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("A"), pressTime)

async def right(pressTime):
    await chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("D"), pressTime)

async def stop():
    await chatPlays.releaseKey(chatPlays.keyCodes.get("K"))
    await chatPlays.releaseKey(chatPlays.keyCodes.get("V"))
    await chatPlays.releaseKey(chatPlays.keyCodes.get("Q"))
    await chatPlays.releaseKey(chatPlays.keyCodes.get("E"))
    await chatPlays.releaseKey(chatPlays.keyCodes.get("L"))
    await chatPlays.releaseKey(chatPlays.keyCodes.get("I"))
    await chatPlays.releaseKey(chatPlays.keyCodes.get("O"))
    await chatPlays.releaseKey(chatPlays.keyCodes.get("T"))
    await chatPlays.releaseKey(chatPlays.keyCodes.get("G"))
    await chatPlays.releaseKey(chatPlays.keyCodes.get("W"))
    await chatPlays.releaseKey(chatPlays.keyCodes.get("A"))
    await chatPlays.releaseKey(chatPlays.keyCodes.get("S"))
    await chatPlays.releaseKey(chatPlays.keyCodes.get("D"))