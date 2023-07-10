# functions for doing stream stuff remotely/semi-remotely 

from time import *
import requests
import pyautogui
import os
import configparser

# finding directory
directory = ""
if os.path.exists(os.path.abspath(os.path.join("files"))):
    directory = os.path.abspath(os.path.join("files"))
else:
    print("looking for files directory")
    for root, dirs, files in os.walk("\\"):
        if "early-gang-main\\files\\config.ini" in os.path.abspath(os.path.join(root, "config.ini")):
            directory = os.path.abspath(os.path.join(root))
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
    # try/except so the script doesn't throw an error if the internet briefly goes out
    try:
        # checking if you have the rate requests to do this
        response = requests.get("https://api.twitch.tv/helix/users", headers = {"Client-ID": clientID, "Authorization": f"Bearer {accessToken}"})
        rateLimit = response.headers.get("Ratelimit-Remaining")
        if rateLimit != "0":
            # asking twitch for the information
            response = requests.get("https://api.twitch.tv/helix/streams?user_login=" + channelName, headers = {"Client-ID": clientID, "Authorization": "Bearer " + accessToken})
            if response.status_code == 200:
                data = response.json()
                if data["data"]:
                    return True
                else:
                    return False
            # error handling
            else:
                print("oops you fucked up somewhere\ndouble check your info file")
                return None
        # waiting and trying again if theres no rate left
        else:
            sleep(5)
            isLive(channelName)
    # waiting and trying again if internet goes out
    except:
        sleep(5)
        isLive(channelName)

# looks up the id corresponding to a channel name
# needed for initiating raids
def getBroadcasterId(channelName):
    # try/except so the script doesnt throw an error if the internet briefly goes out
    try:
        # checking if you have the rate requests to do this
        response = requests.get("https://api.twitch.tv/helix/users", headers = {"Client-ID": clientID, "Authorization": f"Bearer {accessToken}"})
        rateLimit = response.headers.get("Ratelimit-Remaining")
        if rateLimit != "0":
            # asking twitch for the information
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
        # waiting and trying again if theres no rate left
        else:
            sleep(5)
            getBroadcasterId(channelName)
    # waiting and trying again if internet goes out
    except:
        sleep(5)
        getBroadcasterId(channelName)

# starts a raid from your channel to another
def raid(raiderChannelName, raideeChannelName):
    # try/except so the script doesnt throw an error if the internet briefly goes out
    try:
        # checking if you have the rate requests to do this
        response = requests.get("https://api.twitch.tv/helix/users", headers = {"Client-ID": clientID, "Authorization": f"Bearer {accessToken}"})
        rateLimit = response.headers.get("Ratelimit-Remaining")
        if rateLimit != "0":
            # asking twitch to start raid
            if getBroadcasterId(raiderChannelName) and getBroadcasterId(raideeChannelName):
                raid_response = requests.post("https://api.twitch.tv/helix/raids", headers = {"Authorization": "Bearer " + accessToken, "Client-Id": clientID} , params = {"from_broadcaster_id": getBroadcasterId(raiderChannelName), "to_broadcaster_id": getBroadcasterId(raideeChannelName)})
                # error handling
                if raid_response.status_code != 200:
                    print("twitch fucked up")
            # trying again if the script couldn't find the broadcaster ids
            else:
                raid(raiderChannelName, raideeChannelName)
        # waiting and trying again if there's no rate left
        else:
            sleep(5)
            raid(raiderChannelName, raideeChannelName)
    # waiting and trying again if internet goes out
    except:
        sleep(5)
        raid(raiderChannelName, raideeChannelName)

    # waiting for raid cooldown
    sleep(15)

    # clicking the raid now button
    openBrowser()
    imageLocation = pyautogui.locateOnScreen(os.path.abspath((os.path.join(directory, "media", "raidNow.png"))), confidence = .9)
    if imageLocation is not None:
        pyautogui.moveTo((imageLocation.left + (imageLocation.width / 2)), (imageLocation.top + (imageLocation.height / 2)))
        pyautogui.click()
    else:
        print("script couldn't find the start raid button")

    # waiting to make sure raid went through
    sleep(10)

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
