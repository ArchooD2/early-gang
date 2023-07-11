from obswebsocket import obsws
from obswebsocket import requests as obwsrequests
from autoStream import *
import os
import time
import threading
import pyttsx3
import pyautogui
import configparser
import requests
from datetime import datetime


ws = None
ttsOn = False
lastDonation = []
screenWidth, screenHeight = pyautogui.size()

# reading config
config = configparser.ConfigParser()
config.read(os.path.abspath((os.path.join(directory, "config.ini"))))
websocketPassword = config.get("obs", "websocket server password")
clientID = config.get("tiltify", "client id")
clientSecret = config.get("tiltify", "client secret")
code = config.get("tiltify", "code")

# checking for refresh token
refreshToken = config.get("tiltify", "refresh token")
if refreshToken == "":
    response = requests.post("https://v5api.tiltify.com/oauth/token", data = {"grant_type": "authorization_code", "client_id": clientID, "client_secret": clientSecret, "redirect_uri": 'https://localhost/', "code": code})
    # writing response to file
    with open(os.path.abspath((os.path.join(directory, "config.ini"))), 'r') as file:
        lines = file.readlines()
    for i, line in enumerate(lines):
        if line.startswith("refresh token ="):
            lines[i] = "refresh token = " + response.json().get("refresh_token") + "\n"
            break
    with open(os.path.abspath((os.path.join(directory, "config.ini"))), 'w') as file:
        file.writelines(lines)

# connecting to obs
def connectToObs():
    global ws
    ws = obsws("localhost", 4444, websocketPassword)
    ws.connect()

#finds the scene where the tts is located
def getScene():
    global ws
    headerFound = False
    bodyFound = False

    # get scene names
    sceneData = ws.call(obwsrequests.GetSceneList())
    for scene in sceneData.getScenes():
        name = scene.get("name")
        # loop through each scene to find which scene has the tts sources
        itemData = ws.call(obwsrequests.GetSceneItemList(sceneName = name))
        for item in itemData.getSceneItems():
            if item.get("sourceName") == "tts header":
                headerFound = True
                break
        for item in itemData.getSceneItems():
            if item.get("sourceName") == "tts body":
                bodyFound = True
                break

        # when both are found return current scene
        if headerFound and bodyFound:
            return name

# takes donation info and tells obs to display it
def donationAlert(name, amount, charity, message):
    # format message into lines
    lineLength = len(f"{name} donated ${amount} to {charity}")
    words = message.split()
    text = []

    currentLine = ""
    for word in words:
        if len(currentLine) + len(word) < lineLength:
            if currentLine == "":
                currentLine += word
            else:
                currentLine += " " + word
        else:
            text += [currentLine + "\n"]
            currentLine = ""
    text += currentLine
    formatted_text = ''.join(text)

    # change donation text
    with open(os.path.abspath((os.path.join(directory, "ttsBody.txt"))), "w") as file:
        file.write(formatted_text)
    with open(os.path.abspath((os.path.join(directory, "ttsHeader.txt"))), "w") as file:
        file.write(f"{name} donated ${amount} to {charity}")

    # give obs time to update text
    time.sleep(2)

    # change source positions based on text size
    response = ws.call(obwsrequests.GetSceneItemProperties(sceneName = getScene(), item = "tts header"))
    headerWidth = response.getWidth()
    headerHeight = response.getHeight()
    response = ws.call(obwsrequests.GetSceneItemProperties(sceneName = getScene(), item = "tts body"))
    bodyWidth = response.getWidth()
    ws.call(obwsrequests.SetSceneItemProperties(sceneName= getScene(), item = "tts header", position = {"x": screenWidth - headerWidth - 50, "y": 50}))
    ws.call(obwsrequests.SetSceneItemProperties(sceneName=getScene(), item="tts body", position = {"x": (screenWidth - headerWidth) + (headerWidth - bodyWidth)/2 - 50, "y": 50 + headerHeight}))


    # tell obs to show sources
    ws.call(obwsrequests.SetSceneItemProperties(sceneName=getScene(), item="tts body", visible=True))
    ws.call(obwsrequests.SetSceneItemProperties(sceneName=getScene(), item="tts header", visible=True))

    # speak message
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 80)
    engine.say(message)
    engine.runAndWait()

    # tell obs to hide sources
    ws.call(obwsrequests.SetSceneItemProperties(sceneName=getScene(), item="tts body", visible=False))
    ws.call(obwsrequests.SetSceneItemProperties(sceneName=getScene(), item="tts header", visible=False))

# starts taking and displaying tts messages
def startTTS():
    global ttsOn
    ttsOn = True
    ttsThread = threading.Thread(target=tts)
    ttsThread.start()

# stops taking and displaying tts messages
def stopTTS():
    global ttsOn
    ttsOn = False

# infinite loop that looks for new donations if tts is on
def tts():
    global ttsOn
    global ws
    global lastDonation

    while ttsOn:
        campaignData = requests.get("https://v5api.tiltify.com/api/public/users/" + (requests.get("https://v5api.tiltify.com/api/public/current-user", headers = {"Authorization": "Bearer " + (requests.post("https://v5api.tiltify.com/oauth/token",data={"client_id": clientID, "client_secret": clientSecret, "grant_type": "refresh_token", "refresh_token": refreshToken}).json().get("access_token"))}).json().get("data").get("id")) + "/campaigns", headers = {"Authorization": "Bearer " + requests.post("https://v5api.tiltify.com/oauth/token",data={"client_id": clientID, "client_secret": clientSecret, "grant_type": "refresh_token", "refresh_token": refreshToken}).json().get("access_token")})
        ids = []
        for x in campaignData.json().get("data"):
            ids += [[x.get("id"), x.get("name")]]
        for id in ids:
            donationData = requests.get("https://v5api.tiltify.com/api/public/campaigns/" + str(id[0]) + "/donations", headers = {"Authorization": "Bearer " + requests.post("https://v5api.tiltify.com/oauth/token",data={"client_id": clientID, "client_secret": clientSecret, "grant_type": "refresh_token", "refresh_token": refreshToken}).json().get("access_token")}).json().get("data")
            if donationData != [] and donationData not in lastDonation:
                lastDonation += [donationData]
                donationAlert(donationData[0].get("donor_name"), donationData[0].get("amount").get("value"), id[1], donationData[0].get("donor_comment"))