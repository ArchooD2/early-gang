# functions for doing stream stuff remotely/semi-remotely 

# imports
import configparser
import os
import aiohttp
import pyautogui
import requests
import asyncio

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
async def isLive(channelName):

    # asking twitch for the information
    try:
        async with aiohttp.ClientSession(headers = {"Client-ID": clientID, "Authorization": f"Bearer {accessToken}"}) as session:
            async with session.get("https://api.twitch.tv/helix/users") as response:
                rateLimit = response.headers.get("Ratelimit-Remaining")
                if rateLimit != "0":
                    async with session.get("https://api.twitch.tv/helix/streams?user_login=" + channelName) as streamResponse:
                        if streamResponse.status == 200:
                            data = await streamResponse.json()
                            if data["data"]:
                                return True
                            else:
                                return False
                        else:
                            print("error checking if channel is live" + await streamResponse.json())
                            return None
               # trying again
                else:
                    await asyncio.sleep(5)
                    await isLive(channelName)
    except:
        await asyncio.sleep(5)
        await isLive(channelName)

# looks up the id corresponding to a channel name
# needed for initiating raids
async def getBroadcasterId(channelName):

    # asking twitch for the id
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.get("https://api.twitch.tv/helix/users", headers = {"Client-ID": clientID, "Authorization": "Bearer " + accessToken})
            rateLimit = response.headers.get("Ratelimit-Remaining")
            if rateLimit != "0":
                response = await session.get("https://api.twitch.tv/helix/users?login=" +channelName, headers = {"Client-ID": clientID, "Authorization": "Bearer " + accessToken})

                if response.status == 200:
                    data = await response.json()
                    if data["data"]:
                        broadcasterId = data["data"][0]["id"]
                        return broadcasterId

                    # error handling
                    else:
                        print("error getting id " + await response.json())

                # more error handling
                else:
                    await asyncio.sleep(5)
                    return await getBroadcasterId(channelName)
    except:
        await asyncio.sleep(5)
        return await getBroadcasterId(channelName)

# starts a raid from your channel to another
async def raid(raiderChannelName, raideeChannelName):

    # asking twitch to start raid
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.twitch.tv/helix/users", headers={"Client-ID": clientID, "Authorization": f"Bearer {accessToken}"}) as response:
                rateLimit = response.headers.get("Ratelimit-Remaining")
                if rateLimit != "0":
                    if await getBroadcasterId(raiderChannelName) and await getBroadcasterId(raideeChannelName):
                        async with session.post("https://api.twitch.tv/helix/raids", headers={"Authorization": "Bearer " + accessToken, "Client-Id": clientID}, params={"from_broadcaster_id": await getBroadcasterId(raiderChannelName), "to_broadcaster_id": await getBroadcasterId(raideeChannelName)}) as raid_response:
                            if raid_response.status != 200:
                                print("twitch fucked up")

                    # trying again
                    else:
                        await raid(raiderChannelName, raideeChannelName)
                else:
                    await asyncio.sleep(5)
                    await raid(raiderChannelName, raideeChannelName)
    except:
        await asyncio.sleep(5)
        await raid(raiderChannelName, raideeChannelName)

    # waiting for raid cooldown
    await asyncio.sleep(5)

    # clicking the raid now button
    await openBrowser()
    imageLocation = pyautogui.locateOnScreen(os.path.abspath((os.path.join(directory, "media", "raidNow.png"))), confidence = .9)
    if imageLocation is not None:
        pyautogui.moveTo((imageLocation.left + (imageLocation.width / 2)), (imageLocation.top + (imageLocation.height / 2)))
        pyautogui.click()
    else:
        print("script couldn't find the start raid button")

    # waiting to make sure raid went through
    await asyncio.sleep(5)

    # returning to your channel page
    pyautogui.keyDown("alt")
    pyautogui.press("left")
    pyautogui.keyUp("alt")

# opens obs and clicks the starts stream button
async def startStream():
    await openOBS()
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
    await openGame()

# opens obs and clicks stop stream button
async def stopStream():
    await openOBS()
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
    await openGame()

# clicks the obs icon
async def openOBS():
    imageLocation = pyautogui.locateOnScreen(os.path.abspath((os.path.join(directory, "media", "obs.png"))), confidence = .9)
    if imageLocation is not None:
        pyautogui.moveTo((imageLocation.left + (imageLocation.width / 2)), (imageLocation.top + (imageLocation.height / 2)))
        pyautogui.click()
    else:
        print("script couldn't find the obs icon")

# clicks the browser icon
async def openBrowser():
    imageLocation = pyautogui.locateOnScreen(os.path.abspath((os.path.join(directory, "media", "browser.png"))), confidence = .9)
    if imageLocation is not None:
        pyautogui.moveTo((imageLocation.left + (imageLocation.width / 2)), (imageLocation.top + (imageLocation.height / 2)))
        pyautogui.click()
    else:
        print("script couldn't find the browser icon")

# clicks the icon for the game chat is playing
async def openGame():
    imageLocation = pyautogui.locateOnScreen(os.path.abspath((os.path.join(directory, "media", "game.png"))), confidence = .9)
    if imageLocation is not None:
        pyautogui.moveTo((imageLocation.left + (imageLocation.width / 2)), (imageLocation.top + (imageLocation.height / 2)))
        pyautogui.click()
    else:
        print("script couldn't find the game icon")