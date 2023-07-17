# imports
import time

from libraries import chatPlays
from libraries.autoStream import *
import random

# setting up variables
pressTime = (random.randint(1, 3) / 10)
lightPressTime = (random.randint(1, 3) / 100)
holdTime = random.randint(5, 10)

# reading config
config = configparser.ConfigParser()
config.read(os.path.abspath((os.path.join(directory, "config.ini"))))
landmines = config.get("twitch", "landmines", fallback = "").strip("[]").split(", ")

# makes inputs when no one has typed in chat for a while
def idleBot():

    # checks if idle bot is supposed to be on and if no one has chatted
    while chatPlays.idleBotPlaying:
        if chatPlays.noRecentMessages:

            # time between inputs
            time.sleep(random.randint(1, 10) / 10)
            dice = random.randint(1, 4)

            # 25% chance of non directionals
            if dice == 1:
                dice = random.randint(1, 6)
                match dice:
                    case 1:
                        a(pressTime)
                    case 2:
                        b(pressTime)
                    case 3:
                        x(pressTime)
                    case 4:
                        y(pressTime)
                    case 5:
                        select(pressTime)
                    case 6:
                        start(pressTime)

            # 75% chance of directionals
            else:
                dice = random.randint(1, 5)
                match dice:
                    case 1:
                        up(pressTime)
                    case 2:
                        down(pressTime)
                    case 3:
                        left(pressTime)
                    case 4:
                        right(pressTime)
                    case 5:
                        wander(4, holdTime)

# makes inputs every so often
def inputBot():

    # checks if conditions are right
    while chatPlays.inputBotPlaying:
        if not chatPlays.snackShot:

            # sleepy snack controls
            if chatPlays.currentSnack == "sleepy":

                # time between inputs
                time.sleep(random.randint(30, 720))
                dice = random.randint(1, 100)

                # 5% chance of no action
                if dice < 96:
                    dice = random.randint(1, 17)
                    match dice:
                        case 1:
                            up(pressTime)
                        case 2:
                            down(pressTime)
                        case 3:
                            left(pressTime)
                        case 4:
                            right(pressTime)
                        case 5:
                            holdUp(holdTime)
                        case 6:
                            holdDown(holdTime)
                        case 7:
                            holdLeft(holdTime)
                        case 8:
                            holdDown(holdTime)
                        case 9:
                            a(pressTime)
                        case 10:
                            holdA(holdTime)
                        case 11:
                            b(pressTime)
                        case 12:
                            holdB()
                        case 13:
                            x(pressTime)
                        case 14:
                            y(pressTime)
                        case 15:
                            select(pressTime)
                        case 16:
                            start(pressTime)
                        case 17:
                            wander(2, holdTime)

            # chris snack controls
            elif chatPlays.currentSnack == "chris":

                # time between inputs
                time.sleep(random.randint(5, 120))
                dice = random.randint(1, 3)

                # 33% chance of no action
                if dice == 1 or dice == 2:
                    dice = random.randint(1, 17)
                    match dice:
                        case 1:
                            up(pressTime)
                        case 2:
                            down(pressTime)
                        case 3:
                            left(pressTime)
                        case 4:
                            right(pressTime)
                        case 5:
                            holdUp(holdTime)
                        case 6:
                            holdDown(holdTime)
                        case 7:
                            holdLeft(holdTime)
                        case 8:
                            holdDown(holdTime)
                        case 9:
                            a(pressTime)
                        case 10:
                            holdA(holdTime)
                        case 11:
                            b(pressTime)
                        case 12:
                            holdB()
                        case 13:
                            x(pressTime)
                        case 14:
                            y(pressTime)
                        case 15:
                            select(pressTime)
                        case 16:
                            start(pressTime)
                        case 17:
                            wander(2, holdTime)

            # burst snack controls
            elif chatPlays.currentSnack == "burst":

                # time between inputs
                time.sleep(random.randint(150, 450))
                dice = random.randint(1, 10)

                # 10% chance of no action
                if dice != 1:
                    for i in range(5):
                        dice = random.randint(1, 17)
                        match dice:
                            case 1:
                                up(pressTime)
                            case 2:
                                down(pressTime)
                            case 3:
                                left(pressTime)
                            case 4:
                                right(pressTime)
                            case 5:
                                holdUp(holdTime)
                            case 6:
                                holdDown(holdTime)
                            case 7:
                                holdLeft(holdTime)
                            case 8:
                                holdDown(holdTime)
                            case 9:
                                a(pressTime)
                            case 10:
                                holdA(holdTime)
                            case 11:
                                b(pressTime)
                            case 12:
                                holdB()
                            case 13:
                                x(pressTime)
                            case 14:
                                y(pressTime)
                            case 15:
                                select(pressTime)
                            case 16:
                                start(pressTime)
                            case 17:
                                wander(2, holdTime)

            # silly snack controls
            elif chatPlays.currentSnack == "silly":

                # time between inputs
                time.sleep(random.randint(5, 80))
                dice = random.randint(1, 3)

                # 33% chance of no action
                if dice != 1:
                    dice = random.randint(1, 9)
                    match dice:
                        case 1:
                            up(pressTime)
                        case 2:
                            down(pressTime)
                        case 3:
                            left(pressTime)
                        case 4:
                            right(pressTime)
                        case 5:
                            holdUp(holdTime)
                        case 6:
                            holdDown(holdTime)
                        case 7:
                            holdLeft(holdTime)
                        case 8:
                            holdDown(holdTime)
                        case 9:
                            wander(2, holdTime)

            # cautious snack controls
            elif chatPlays.currentSnack == "cautious":

                # time between inputs
                time.sleep(random.randint(5, 120))
                dice = random.randint(1, 5)

                # 20% chance of no action
                if dice != 1:
                    dice = random.randint(1, 6)
                    match dice:
                        case 1:
                            north(lightPressTime)
                        case 2:
                            south(lightPressTime)
                        case 3:
                            east(lightPressTime)
                        case 4:
                            west(lightPressTime)
                        case 5:
                            b(pressTime)
                        case 6:
                            mashB(pressTime)

            # sonic snack controls
            elif chatPlays.currentSnack == "sonic":

                # time between inputs
                time.sleep(random.randint(10, 30))
                dice = random.randint(1, 10)

                # 10% chance of no action
                if dice != 1:
                    dice = random.randint(1, 6)
                    match dice:
                        case 1:
                            north(lightPressTime)
                        case 2:
                            south(lightPressTime)
                        case 3:
                            east(lightPressTime)
                        case 4:
                            west(lightPressTime)
                        case 5:
                            mashA(pressTime)
                        case 6:
                            mashB(pressTime)
                        case 7:
                            wander(4, holdTime)
                        case 8:
                            upWander(holdTime)
                        case 9:
                            downWander(holdTime)
                        case 10:
                            leftWander(holdTime)
                        case 11:
                            rightWander(holdTime)

# chat controls
def controller(data):

    # makes sure chat is playing
    chatPlays.noRecentMessages = False
    if chatPlays.chatPlaying is True:

        # getting current viewer count
        connected = False
        while not connected:
            try:
                response = requests.get("https://api.twitch.tv/helix/users", headers={"Client-ID": clientID, "Authorization": f"Bearer {accessToken}"})
                rateLimit = response.headers.get("Ratelimit-Remaining")
                if rateLimit != "0":
                    userResponse = requests.get(f"https://api.twitch.tv/helix/users?login={chatPlays.yourChannelName}", headers={"Client-ID": chatPlays.clientID, "Authorization": "Bearer " + chatPlays.accessToken}).json()
                    streamResponse = requests.get(f'https://api.twitch.tv/helix/streams?user_id={userResponse.get("data")[0].get("id")}', headers={"Client-ID": chatPlays.clientID, "Authorization": "Bearer " + chatPlays.accessToken}).json()
                    connected = True
                else:
                    time.sleep(5)
            except:
                time.sleep(5)

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
            message = data["message"].lower()
            dice = random.randint(1, 40)

            # 2.5% chance of random input
            if dice == 1:
                dice = random.randint(1, 28)
                match dice:
                    case 1:
                        up(pressTime)
                    case 2:
                        down(pressTime)
                    case 3:
                        left(pressTime)
                    case 4:
                        right(pressTime)
                    case 5:
                        holdUp(holdTime)
                    case 6:
                        holdDown(holdTime)
                    case 7:
                        holdLeft(holdTime)
                    case 8:
                        holdRight(holdTime)
                    case 9:
                        a(pressTime)
                    case 10:
                        holdA(holdTime)
                    case 11:
                        mashA(pressTime)
                    case 12:
                        b(pressTime)
                    case 13:
                        holdB()
                    case 14:
                        mashB(pressTime)
                    case 15:
                        x(pressTime)
                    case 16:
                        y(pressTime)
                    case 17:
                        select(pressTime)
                    case 18:
                        start(pressTime)
                    case 19:
                        stop()
                    case 20:
                        wander(4, holdTime)
                    case 21:
                        north(lightPressTime)
                    case 22:
                        south(lightPressTime)
                    case 23:
                        west(lightPressTime)
                    case 24:
                        east(lightPressTime)
                    case 25:
                        upWander(holdTime)
                    case 26:
                        downWander(holdTime)
                    case 27:
                        leftWander(holdTime)
                    case 28:
                        rightWander(holdTime)

            # 2.5% chance of opposite input
            elif dice == 2:
                if message == "a":
                    b(pressTime)
                elif "hold a" in message:
                    holdB()
                elif "mash a" in message:
                    mashB(pressTime)
                elif message == "b":
                    a(pressTime)
                elif "hold b" in message:
                    holdA(holdTime)
                elif "mash b" in message:
                    mashA(pressTime)
                elif message == "x":
                    y(pressTime)
                elif message == "y":
                    x(pressTime)
                elif "select" in message:
                    start(pressTime)
                elif "start" in message:
                    select(pressTime)
                elif "up wander" in message:
                    downWander(holdTime)
                elif "down wander" in message:
                    upWander(holdTime)
                elif "left wander" in message:
                    rightWander(holdTime)
                elif "right wander" in message:
                    leftWander(holdTime)
                elif "wander" in message:
                    stop()
                elif "hold up" in message:
                    holdDown(holdTime)
                elif "hold down" in message:
                    holdUp(holdTime)
                elif "hold left" in message:
                    holdRight(holdTime)
                elif "hold right" in message:
                    holdLeft(holdTime)
                elif "north" in message:
                    south(lightPressTime)
                elif "south" in message:
                    north(lightPressTime)
                elif "west" in message:
                    east(lightPressTime)
                elif "east" in message:
                    west(lightPressTime)
                elif "up" in message:
                    down(pressTime)
                elif "down" in message:
                    up(pressTime)
                elif "left" in message:
                    right(pressTime)
                elif "right" in message:
                    left(pressTime)
                elif "stop" in message:
                    upWander(holdTime)
                    downWander(holdTime)
                    leftWander(holdTime)
                    rightWander(holdTime)
                elif landmines[0] in message or landmines[1] in message or landmines[2] in message or landmines[3] in message or landmines[4] in message:
                    if chatPlays.landminesActive:
                        stop()

            # 95% chance of correct inputs
            else:
                if message == "a":
                    a(pressTime)
                elif "hold a" in message:
                    holdA(holdTime)
                elif "mash a" in message:
                    mashA(pressTime)
                elif message == "b":
                    b(pressTime)
                elif "hold b" in message:
                    holdB()
                elif "mash b" in message:
                    mashB(pressTime)
                elif message == "x":
                    x(pressTime)
                elif message == "y":
                    y(pressTime)
                elif "select" in message:
                    select(pressTime)
                elif "start" in message:
                    start(pressTime)
                elif "up wander" in message:
                    upWander(holdTime)
                elif "down wander" in message:
                    downWander(holdTime)
                elif "left wander" in message:
                    leftWander(holdTime)
                elif "right wander" in message:
                    rightWander(holdTime)
                elif "wander" in message:
                    wander(4, holdTime)
                elif "hold up" in message:
                    holdUp(holdTime)
                elif "hold down" in message:
                    holdDown(holdTime)
                elif "hold left" in message:
                    holdLeft(holdTime)
                elif "hold right" in message:
                    holdRight(holdTime)
                elif "north" in message:
                    north(lightPressTime)
                elif "south" in message:
                    south(lightPressTime)
                elif "west" in message:
                    west(lightPressTime)
                elif "east" in message:
                    east(lightPressTime)
                elif "up" in message:
                    up(pressTime)
                elif "down" in message:
                    down(pressTime)
                elif "left" in message:
                    left(pressTime)
                elif "right" in message:
                    right(pressTime)
                elif "stop" in message:
                    stop()
                elif landmines[0] in message or landmines[1] in message or landmines[2] in message or landmines[3] in message or landmines[4] in message:
                    if chatPlays.landminesActive:
                        wander(2, holdTime)

# define controls down here
def a(pressTime):
    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("L"), pressTime)

def holdA(holdTime):
    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("L"), holdTime)

def mashA(pressTime):
    mashTime = 0
    while mashTime <= 2:
        chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("L"), pressTime)
        mashTime += pressTime + .3
        time.sleep(.3)

def b(pressTime):
    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("K"), pressTime)

def holdB():
    chatPlays.holdKey(chatPlays.keyCodes.get("K"))

def mashB(pressTime):
    mashTime = 0
    while mashTime <= 2:
        chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("K"), pressTime)
        mashTime += pressTime + .3
        time.sleep(.3)

def x(pressTime):
    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("I"), pressTime)

def y(pressTime):
    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("O"), pressTime)

def select(pressTime):
    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("T"), pressTime)

def start(pressTime):
    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("G"), pressTime)

def wander(times, holdTime):
    for i in range(times):
        dice = random.randint(1, 4)
        match dice:
            case 1:
                chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("W"), holdTime)
            case 2:
                chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("A"), holdTime)
            case 3:
                chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("S"), holdTime)
            case 4:
                chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("D"), holdTime)

def upWander(holdTime):
    for i in range(4):
        dice = random.randint(1, 10)
        if dice == 1 or dice == 2 or dice == 3 or dice == 4:
            chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("W"), holdTime)
        else:
            dice = random.randint(1, 2)
            if dice == 1:
                chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("D"), holdTime)
            else:
                chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("A"), holdTime)

def downWander(holdTime):
    for i in range(4):
        dice = random.randint(1, 10)
        if dice == 1 or dice == 2 or dice == 3 or dice == 4:
            chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("S"), holdTime)
        else:
            dice = random.randint(1, 2)
            if dice == 1:
                chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("D"), holdTime)
            else:
                chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("A"), holdTime)

def leftWander(holdTime):
    for i in range(4):
        dice = random.randint(1, 10)
        if dice == 1 or dice == 2 or dice == 3 or dice == 4:
            chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("A"), holdTime)
        else:
            dice = random.randint(1, 2)
            if dice == 1:
                chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("W"), holdTime)
            else:
                chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("S"), holdTime)

def rightWander(holdTime):
    for i in range(4):
        dice = random.randint(1, 10)
        if dice == 1 or dice == 2 or dice == 3 or dice == 4:
            chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("D"), holdTime)
        else:
            dice = random.randint(1, 2)
            if dice == 1:
                chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("W"), holdTime)
            else:
                chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("S"), holdTime)

def holdUp(holdTime):
    dice = random.randint(1, 100)
    if dice == 1:
        for i in range(8):
            dice = random.randint(1, 4)
            match dice:
                case 1:
                    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("W"), holdTime)
                case 2:
                    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("A"), holdTime)
                case 3:
                    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("S"), holdTime)
                case 4:
                    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("D"), holdTime)
    else:
        chatPlays.releaseKey(chatPlays.keyCodes.get("S"))
        chatPlays.releaseKey(chatPlays.keyCodes.get("A"))
        chatPlays.releaseKey(chatPlays.keyCodes.get("D"))
        chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("W"), holdTime)

def holdDown(holdTime):
    dice = random.randint(1, 100)
    if dice == 1:
        for i in range(8):
            dice = random.randint(1, 4)
            match dice:
                case 1:
                    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("W"), holdTime)
                case 2:
                    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("A"), holdTime)
                case 3:
                    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("S"), holdTime)
                case 4:
                    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("D"), holdTime)
    else:
        chatPlays.releaseKey(chatPlays.keyCodes.get("W"))
        chatPlays.releaseKey(chatPlays.keyCodes.get("A"))
        chatPlays.releaseKey(chatPlays.keyCodes.get("D"))
        chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("S"), holdTime)

def holdLeft(holdTime):
    dice = random.randint(1, 100)
    if dice == 1:
        for i in range(8):
            dice = random.randint(1, 4)
            match dice:
                case 1:
                    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("W"), holdTime)
                case 2:
                    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("A"), holdTime)
                case 3:
                    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("S"), holdTime)
                case 4:
                    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("D"), holdTime)
    else:
        chatPlays.releaseKey(chatPlays.keyCodes.get("D"))
        chatPlays.releaseKey(chatPlays.keyCodes.get("S"))
        chatPlays.releaseKey(chatPlays.keyCodes.get("W"))
        chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("A"), holdTime)

def holdRight(holdTime):
    dice = random.randint(1, 100)
    if dice == 1:
        for i in range(8):
            dice = random.randint(1, 4)
            match dice:
                case 1:
                    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("W"), holdTime)
                case 2:
                    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("A"), holdTime)
                case 3:
                    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("S"), holdTime)
                case 4:
                    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("D"), holdTime)
    else:
        chatPlays.releaseKey(chatPlays.keyCodes.get("A"))
        chatPlays.releaseKey(chatPlays.keyCodes.get("W"))
        chatPlays.releaseKey(chatPlays.keyCodes.get("S"))
        chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("D"), holdTime)

def north(lightPressTime):
    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("W"), lightPressTime)

def south(lightPressTime):
    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("S"), lightPressTime)

def west(lightPressTime):
    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("A"), lightPressTime)

def east(lightPressTime):
    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("D"), lightPressTime)

def up(pressTime):
    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("W"), pressTime)

def down(pressTime):
    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("S"), pressTime)

def left(pressTime):
    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("A"), pressTime)

def right(pressTime):
    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("D"), pressTime)

def stop():
    chatPlays.releaseKey(chatPlays.keyCodes.get("K"))
    chatPlays.releaseKey(chatPlays.keyCodes.get("L"))
    chatPlays.releaseKey(chatPlays.keyCodes.get("W"))
    chatPlays.releaseKey(chatPlays.keyCodes.get("A"))
    chatPlays.releaseKey(chatPlays.keyCodes.get("S"))
    chatPlays.releaseKey(chatPlays.keyCodes.get("D"))