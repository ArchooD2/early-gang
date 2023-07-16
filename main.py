from bots.commandBot import *
from bots.pollBot import *
from libraries.chatPlays import *
from libraries.charityDonoTTS import *
from bots.panicBot import *
from bots.gwrbullBot import *

# setting stuff up
econBotThread = startEconBot()
commandBotThread = startCommandBot()
pollBotThread = startPollBot()
panicBotThread = startPanicBot()
gwrbotThread = startGwrbullBot()
connectToObs()
connectToTwitchChat()

# so you don't have to restart stream
if isLive(yourChannelName):
    startTTS()
    startChatPlays()
    startAutoSave()
    startIdleBot()
    startInputBot()
    startInternetPing()

while True:

    # if streamer goes live
    if (isLive(yourChannelName) and isLive(streamerChannelName)):

        # shut down everything
        if ttsOn:
            stopTTS()
        if chatPlaying:
            stopChatPlays()
        if idleBotPlaying:
            stopIdleBot()
        if inputBotPlaying:
            stopInputBot()
        if autoSaving:
            stopAutoSave()
        if pinging:
            stopInternetPing()

        # end stream
        if isLive(yourChannelName):
            raid(yourChannelName, streamerChannelName)
            stopStream()

    # if streamer goes offline
    elif (not isLive(yourChannelName) and not isLive(streamerChannelName)):
        # start stream
        if not isLive(yourChannelName):
            startStream()
        if not ttsOn:
            startTTS()
        if not chatPlaying:
            startChatPlays()
        if not autoSaving:
            startAutoSave()
        if not idleBotPlaying:
            startIdleBot()
        if not inputBotPlaying:
            startInputBot()
        if not pinging:
            startInternetPing()

# so asyncio doesn't yell at me :)
econBotThread.join()
commandBotThread.join()
pollBotThread.join()
panicBotThread.join()
gwrbotThread.join()