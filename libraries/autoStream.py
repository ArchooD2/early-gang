# functions for doing stream stuff remotely/semi-remotely 

# imports
import configparser
import os
import time
import pyautogui
import requests

# setting up variables
whiteListers = ["dougdoug", "parkzer", "fizzeghost", "sna1l_boy"]

# finding directory
directory = ""
if os.path.exists(os.path.abspath(os.path.join("files"))):
    directory = os.path.abspath(os.path.join("files"))
else:
    print("looking for files directory")
    for root, dirs, files in os.walk("\\"):
        if "early-gang-main\\files\\config.ini" in os.path.abspath(os.path.join(root, "config.ini")):
            directory = os.path.abspath(os.path.join(root))
if directory == "":
    print("couldn't find directory")
else:
    print(directory)

# reading config
config = configparser.ConfigParser()
config.read(os.path.abspath((os.path.join(directory, "config.ini"))))
clientID = config.get("twitch", "client id")
accessToken = config.get("twitch", "access token")
streamerChannelName = config.get("twitch", "streamer channel name")
yourChannelName = config.get("twitch", "your channel name")

# checks if a channel is live then returns true if they are, false if not, and none if an error occurs
def isLive(channelName):

    # asking twitch for the information
    try:
        response = requests.get("https://api.twitch.tv/helix/users", headers = {"Client-ID": clientID, "Authorization": f"Bearer {accessToken}"})
        rateLimit = response.headers.get("Ratelimit-Remaining")
        if rateLimit != "0":
            response = requests.get("https://api.twitch.tv/helix/streams?user_login=" + channelName, headers = {"Client-ID": clientID, "Authorization": "Bearer " + accessToken})
            if response.status_code == 200:
                data = response.json()
                if data["data"]:
                    return True
                else:
                    return False

            # error handling
            else:
                print("oops you fucked up somewhere double check your info file")
                return None

        # trying again
        else:
            time.sleep(5)
            isLive(channelName)
    except:
        time.sleep(5)
        isLive(channelName)

# looks up the id corresponding to a channel name
# needed for initiating raids
def getBroadcasterId(channelName):

    # asking twitch for the id
    try:
        response = requests.get("https://api.twitch.tv/helix/users", headers = {"Client-ID": clientID, "Authorization": f"Bearer {accessToken}"})
        rateLimit = response.headers.get("Ratelimit-Remaining")
        if rateLimit != "0":
            response = requests.get("https://api.twitch.tv/helix/users?login=" + channelName, headers = {"Client-ID": clientID, "Authorization": "Bearer " + accessToken})
            if response.status_code == 200:
                data = response.json()
                if data["data"]:
                    broadcasterId = data["data"][0]["id"]
                    return broadcasterId

                # error handling
                else:
                    print(channelName + "is misspelled or something")

            # more error handling
            else:
                print("twitch fucked up")

        # trying again
        else:
            time.sleep(5)
            getBroadcasterId(channelName)
    except:
        time.sleep(5)
        getBroadcasterId(channelName)

# starts a raid from your channel to another
def raid(raiderChannelName, raideeChannelName):

    # asking twitch to start raid
    try:
        response = requests.get("https://api.twitch.tv/helix/users", headers = {"Client-ID": clientID, "Authorization": f"Bearer {accessToken}"})
        rateLimit = response.headers.get("Ratelimit-Remaining")
        if rateLimit != "0":
            if getBroadcasterId(raiderChannelName) and getBroadcasterId(raideeChannelName):
                raid_response = requests.post("https://api.twitch.tv/helix/raids", headers = {"Authorization": "Bearer " + accessToken, "Client-Id": clientID}, params = {"from_broadcaster_id": getBroadcasterId(raiderChannelName), "to_broadcaster_id": getBroadcasterId(raideeChannelName)})
                if raid_response.status_code != 200:
                    print("twitch fucked up")
            else:
                raid(raiderChannelName, raideeChannelName)

        # trying again
        else:
            time.sleep(5)
            raid(raiderChannelName, raideeChannelName)

    # waiting and trying again if internet goes out
    except:
        time.sleep(5)
        raid(raiderChannelName, raideeChannelName)

    # waiting for raid cooldown
    time.sleep(15)

    # clicking the raid now button
    openBrowser()
    imageLocation = pyautogui.locateOnScreen(os.path.abspath((os.path.join(directory, "media", "raidNow.png"))), confidence = .9)
    if imageLocation is not None:
        pyautogui.moveTo((imageLocation.left + (imageLocation.width / 2)), (imageLocation.top + (imageLocation.height / 2)))
        pyautogui.click()
    else:
        print("script couldn't find the start raid button")

    # waiting to make sure raid went through
    time.sleep(10)

    # returning to your channel page
    pyautogui.keyDown("alt")
    pyautogui.press("left")
    pyautogui.keyUp("alt")

# opens obs and clicks the starts stream button
def startStream():
    openOBS()
    imageLocation = pyautogui.locateOnScreen(os.path.abspath((os.path.join(directory, "media", "startStreamingPassive.png"))), confidence = .9)
    if imageLocation is not None:
        pyautogui.moveTo((imageLocation.left + (imageLocation.width / 2)), (imageLocation.top + (imageLocation.height / 2)))
        pyautogui.click()
    else:
        print("script couldn't find the start streaming passive icon")
        imageLocation = pyautogui.locateOnScreen(os.path.abspath((os.path.join(directory, "media", "startStreamingActive.png"))), confidence = .9)
        if imageLocation is not None:
            pyautogui.moveTo((imageLocation.left + (imageLocation.width / 2)), (imageLocation.top + (imageLocation.height / 2)))
            pyautogui.click()
        else:
            print("script couldn't find the start streaming active icon")
    openGame()

# opens obs and clicks stop stream button
def stopStream():
    openOBS()
    imageLocation = pyautogui.locateOnScreen(os.path.abspath((os.path.join(directory, "media", "stopStreamingPassive.png"))), confidence = .9)
    if imageLocation is not None:
        pyautogui.moveTo((imageLocation.left + (imageLocation.width / 2)), (imageLocation.top + (imageLocation.height / 2)))
        pyautogui.click()
    else:
        print("script couldn't find the stop streaming passive button")
        imageLocation = pyautogui.locateOnScreen(os.path.abspath((os.path.join(directory, "media", "stopStreamingActive.png"))), confidence = .9)
        if imageLocation is not None:
            pyautogui.moveTo((imageLocation.left + (imageLocation.width / 2)),
                             (imageLocation.top + (imageLocation.height / 2)))
            pyautogui.click()
        else:
            print("script couldn't find the stop streaming active button")
    openGame()

# clicks the obs icon
def openOBS():
    imageLocation = pyautogui.locateOnScreen(os.path.abspath((os.path.join(directory, "media", "obs.png"))), confidence = .9)
    if imageLocation is not None:
        pyautogui.moveTo((imageLocation.left + (imageLocation.width / 2)), (imageLocation.top + (imageLocation.height / 2)))
        pyautogui.click()
    else:
        print("script couldn't find the obs icon")

# clicks the browser icon
def openBrowser():
    imageLocation = pyautogui.locateOnScreen(os.path.abspath((os.path.join(directory, "media", "browser.png"))), confidence = .9)
    if imageLocation is not None:
        pyautogui.moveTo((imageLocation.left + (imageLocation.width / 2)), (imageLocation.top + (imageLocation.height / 2)))
        pyautogui.click()
    else:
        print("script couldn't find the browser icon")

# clicks the icon for the game chat is playing
def openGame():
    imageLocation = pyautogui.locateOnScreen(os.path.abspath((os.path.join(directory, "media", "game.png"))), confidence = .9)
    if imageLocation is not None:
        pyautogui.moveTo((imageLocation.left + (imageLocation.width / 2)), (imageLocation.top + (imageLocation.height / 2)))
        pyautogui.click()
    else:
        print("script couldn't find the game icon")
