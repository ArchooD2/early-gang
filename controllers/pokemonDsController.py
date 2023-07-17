# imports
import random
from controllers import pokemonGbaController
from libraries import chatPlays
from libraries.autoStream import *

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
                dice = random.randint(1, 8)
                match dice:
                    case 1:
                        pokemonGbaController.a(pressTime)
                    case 2:
                        pokemonGbaController.b(pressTime)
                    case 3:
                        x(pressTime)
                    case 4:
                        y(pressTime)
                    case 5:
                        pokemonGbaController.select(pressTime)
                    case 6:
                        pokemonGbaController.start(pressTime)
                    case 7:
                        l(pressTime)
                    case 8:
                        r(pressTime)
                    
            # 75% chance of directionals
            else:
                dice = random.randint(1, 5)
                match dice:
                    case 1:
                        pokemonGbaController.up(pressTime)
                    case 2:
                        pokemonGbaController.down(pressTime)
                    case 3:
                        pokemonGbaController.left(pressTime)
                    case 4:
                        pokemonGbaController.right(pressTime)
                    case 5:
                        pokemonGbaController.wander(4, holdTime)

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
                    dice = random.randint(1, 19)
                    match dice:
                        case 1:
                            pokemonGbaController.up(pressTime)
                        case 2:
                            pokemonGbaController.down(pressTime)
                        case 3:
                            pokemonGbaController.left(pressTime)
                        case 4:
                            pokemonGbaController.right(pressTime)
                        case 5:
                            pokemonGbaController.holdUp(holdTime)
                        case 6:
                            pokemonGbaController.holdDown(holdTime)
                        case 7:
                            pokemonGbaController.holdLeft(holdTime)
                        case 8:
                            pokemonGbaController.holdDown(holdTime)
                        case 9:
                            pokemonGbaController.a(pressTime)
                        case 10:
                            pokemonGbaController.holdA(holdTime)
                        case 11:
                            pokemonGbaController.b(pressTime)
                        case 12:
                            pokemonGbaController.holdB()
                        case 13:
                            x(pressTime)
                        case 14:
                            y(pressTime)
                        case 15:
                            l(pressTime)
                        case 16:
                            r(pressTime)
                        case 17:
                            pokemonGbaController.select(pressTime)
                        case 18:
                            pokemonGbaController.start(pressTime)
                        case 19:
                            pokemonGbaController.wander(2, holdTime)

            # chris snack controls
            elif chatPlays.currentSnack == "chris":
                
                # time between inputs
                time.sleep(random.randint(5, 120))
                dice = random.randint(1, 3)

                # 33% chance of no action
                if dice != 1:
                    dice = random.randint(1, 19)
                    match dice:
                        case 1:
                            pokemonGbaController.up(pressTime)
                        case 2:
                            pokemonGbaController.down(pressTime)
                        case 3:
                            pokemonGbaController.left(pressTime)
                        case 4:
                            pokemonGbaController.right(pressTime)
                        case 5:
                            pokemonGbaController.holdUp(holdTime)
                        case 6:
                            pokemonGbaController.holdDown(holdTime)
                        case 7:
                            pokemonGbaController.holdLeft(holdTime)
                        case 8:
                            pokemonGbaController.holdDown(holdTime)
                        case 9:
                            pokemonGbaController.a(pressTime)
                        case 10:
                            pokemonGbaController.holdA(holdTime)
                        case 11:
                            pokemonGbaController.b(pressTime)
                        case 12:
                            pokemonGbaController.holdB()
                        case 13:
                            x(pressTime)
                        case 14:
                            y(pressTime)
                        case 15:
                            l(pressTime)
                        case 16:
                            r(pressTime)
                        case 17:
                            pokemonGbaController.select(pressTime)
                        case 18:
                            pokemonGbaController.start(pressTime)
                        case 19:
                            pokemonGbaController.wander(2, holdTime)
                        
            # burst snack controls
            elif chatPlays.currentSnack == "burst":
                
                # time between inputs
                time.sleep(random.randint(150, 450))
                dice = random.randint(1, 10)

                # 10% chance of no action
                if dice != 1:
                    for i in range(5):
                        dice = random.randint(1, 19)
                        match dice:
                            case 1:
                                pokemonGbaController.up(pressTime)
                            case 2:
                                pokemonGbaController.down(pressTime)
                            case 3:
                                pokemonGbaController.left(pressTime)
                            case 4:
                                pokemonGbaController.right(pressTime)
                            case 5:
                                pokemonGbaController.holdUp(holdTime)
                            case 6:
                                pokemonGbaController.holdDown(holdTime)
                            case 7:
                                pokemonGbaController.holdLeft(holdTime)
                            case 8:
                                pokemonGbaController.holdDown(holdTime)
                            case 9:
                                pokemonGbaController.a(pressTime)
                            case 10:
                                pokemonGbaController.holdA(holdTime)
                            case 11:
                                pokemonGbaController.b(pressTime)
                            case 12:
                                pokemonGbaController.holdB()
                            case 13:
                                x(pressTime)
                            case 14:
                                y(pressTime)
                            case 15:
                                l(pressTime)
                            case 16:
                                r(pressTime)
                            case 17:
                                pokemonGbaController.select(pressTime)
                            case 18:
                                pokemonGbaController.start(pressTime)
                            case 19:
                                pokemonGbaController.wander(2, holdTime)

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
                            pokemonGbaController.up(pressTime)
                        case 2:
                            pokemonGbaController.down(pressTime)
                        case 3:
                            pokemonGbaController.left(pressTime)
                        case 4:
                            pokemonGbaController.right(pressTime)
                        case 5:
                            pokemonGbaController.holdUp(holdTime)
                        case 6:
                            pokemonGbaController.holdDown(holdTime)
                        case 7:
                            pokemonGbaController.holdLeft(holdTime)
                        case 8:
                            pokemonGbaController.holdDown(holdTime)
                        case 9:
                            pokemonGbaController.wander(2, holdTime)
            
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
                            pokemonGbaController.north(lightPressTime)
                        case 2:
                            pokemonGbaController.south(lightPressTime)
                        case 3:
                            pokemonGbaController.east(lightPressTime)
                        case 4:
                            pokemonGbaController.west(lightPressTime)
                        case 5:
                            pokemonGbaController.b(pressTime)
                        case 6:
                            pokemonGbaController.mashB(pressTime)

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
                dice = random.randint(1, 30)
                match dice:
                    case 1:
                        pokemonGbaController.up(pressTime)
                    case 2:
                        pokemonGbaController.down(pressTime)
                    case 3:
                        pokemonGbaController.left(pressTime)
                    case 4:
                        pokemonGbaController.right(pressTime)
                    case 5:
                        pokemonGbaController.holdUp(holdTime)
                    case 6:
                        pokemonGbaController.holdDown(holdTime)
                    case 7:
                        pokemonGbaController.holdLeft(holdTime)
                    case 8:
                        pokemonGbaController.holdRight(holdTime)
                    case 9:
                        pokemonGbaController.a(pressTime)
                    case 10:
                        pokemonGbaController.holdA(holdTime)
                    case 11:
                        pokemonGbaController.mashA(pressTime)
                    case 12:
                        pokemonGbaController.b(pressTime)
                    case 13:
                        pokemonGbaController.holdB()
                    case 14:
                        pokemonGbaController.mashB(pressTime)
                    case 15:
                        x(pressTime)
                    case 16:
                        y(pressTime)
                    case 17:
                        pokemonGbaController.select(pressTime)
                    case 18:
                        pokemonGbaController.start(pressTime)
                    case 19:
                        l(pressTime)
                    case 20:
                        r(pressTime)
                    case 21:
                        pokemonGbaController.stop()
                    case 22:
                        pokemonGbaController.wander(4, holdTime)
                    case 23:
                        pokemonGbaController.north(lightPressTime)
                    case 24:
                        pokemonGbaController.south(lightPressTime)
                    case 25:
                        pokemonGbaController.west(lightPressTime)
                    case 26:
                        pokemonGbaController.east(lightPressTime)
                    case 27:
                        pokemonGbaController.upWander(holdTime)
                    case 28:
                        pokemonGbaController.downWander(holdTime)
                    case 29:
                        pokemonGbaController.leftWander(holdTime)
                    case 30:
                        pokemonGbaController.rightWander(holdTime)
            
            # 2.5% chance of opposite input
            elif dice == 2:
                if message == "a":
                    pokemonGbaController.b(pressTime)
                elif "hold a" in message:
                    pokemonGbaController.holdB()
                elif "mash a" in message:
                    pokemonGbaController.mashB(pressTime)
                elif message == "b":
                    pokemonGbaController.a(pressTime)
                elif "hold b" in message:
                    pokemonGbaController.holdA(holdTime)
                elif "mash b" in message:
                    pokemonGbaController.mashA(pressTime)
                elif message == "x":
                    y(pressTime)
                elif message == "y":
                    x(pressTime)
                elif "select" in message:
                    pokemonGbaController.start(pressTime)
                elif "start" in message:
                    pokemonGbaController.select(pressTime)
                elif message == "l":
                    r(pressTime)
                elif message == "r":
                    l(pressTime)
                elif "up wander" in message:
                    pokemonGbaController.downWander(holdTime)
                elif "down wander" in message:
                    pokemonGbaController.upWander(holdTime)
                elif "left wander" in message:
                    pokemonGbaController.rightWander(holdTime)
                elif "right wander" in message:
                    pokemonGbaController.leftWander(holdTime)
                elif "wander" in message:
                    pokemonGbaController.stop()
                elif "hold up" in message:
                    pokemonGbaController.holdDown(holdTime)
                elif "hold down" in message:
                    pokemonGbaController.holdUp(holdTime)
                elif "hold left" in message:
                    pokemonGbaController.holdRight(holdTime)
                elif "hold right" in message:
                    pokemonGbaController.holdLeft(holdTime)
                elif "north" in message:
                    pokemonGbaController.south(lightPressTime)
                elif "south" in message:
                    pokemonGbaController.north(lightPressTime)
                elif "west" in message:
                    pokemonGbaController.east(lightPressTime)
                elif "east" in message:
                    pokemonGbaController.west(lightPressTime)
                elif "up" in message:
                    pokemonGbaController.down(pressTime)
                elif "down" in message:
                    pokemonGbaController.up(pressTime)
                elif "left" in message:
                    pokemonGbaController.right(pressTime)
                elif "right" in message:
                    pokemonGbaController.left(pressTime)
                elif "stop" in message:
                    pokemonGbaController.upWander(holdTime)
                    pokemonGbaController.downWander(holdTime)
                    pokemonGbaController.leftWander(holdTime)
                    pokemonGbaController.rightWander(holdTime)
                elif landmines[0] in message or landmines[1] in message or landmines[2] in message or landmines[3] in message or landmines[4] in message:
                    if chatPlays.landminesActive:
                        pokemonGbaController.stop()
            
            # 95% chance of correct inputs
            else:
                if message == "a":
                    pokemonGbaController. a(pressTime)
                elif "hold a" in message:
                    pokemonGbaController.holdA(holdTime)
                elif "mash a" in message:
                    pokemonGbaController.mashA(pressTime)
                elif message == "b":
                    pokemonGbaController.b(pressTime)
                elif "hold b" in message:
                    pokemonGbaController.holdB()
                elif "mash b" in message:
                    pokemonGbaController.mashB(pressTime)
                elif message == "x":
                    x(pressTime)
                elif message == "y":
                    y(pressTime)
                elif "select" in message:
                    pokemonGbaController.select(pressTime)
                elif "start" in message:
                    pokemonGbaController.start(pressTime)
                elif message == "l":
                    l(pressTime)
                elif message == "r":
                    r(pressTime)
                elif "up wander" in message:
                    pokemonGbaController.upWander(holdTime)
                elif "down wander" in message:
                    pokemonGbaController.downWander(holdTime)
                elif "left wander" in message:
                    pokemonGbaController.leftWander(holdTime)
                elif "right wander" in message:
                    pokemonGbaController.rightWander(holdTime)
                elif "wander" in message:
                    pokemonGbaController.wander(4, holdTime)
                elif "hold up" in message:
                    pokemonGbaController.holdUp(holdTime)
                elif "hold down" in message:
                    pokemonGbaController.holdDown(holdTime)
                elif "hold left" in message:
                    pokemonGbaController.holdLeft(holdTime)
                elif "hold right" in message:
                    pokemonGbaController.holdRight(holdTime)
                elif "north" in message:
                    pokemonGbaController.north(lightPressTime)
                elif "south" in message:
                    pokemonGbaController.south(lightPressTime)
                elif "west" in message:
                    pokemonGbaController.west(lightPressTime)
                elif "east" in message:
                    pokemonGbaController.east(lightPressTime)
                elif "up" in message:
                    pokemonGbaController.up(pressTime)
                elif "down" in message:
                    pokemonGbaController.down(pressTime)
                elif "left" in message:
                    pokemonGbaController.left(pressTime)
                elif "right" in message:
                    pokemonGbaController.right(pressTime)
                elif "stop" in message:
                    pokemonGbaController.stop()
                elif landmines[0] in message or landmines[1] in message or landmines[2] in message or landmines[3] in message or landmines[4] in message:
                    if chatPlays.landminesActive:
                        pokemonGbaController.wander(2, holdTime)

# define controls down here
def x(pressTime):
    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("O"), pressTime)

def y(pressTime):
    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("V"), pressTime)

def l(pressTime):
    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("Q"), pressTime)

def r(pressTime):
    chatPlays.holdAndReleaseKey(chatPlays.keyCodes.get("E"), pressTime)