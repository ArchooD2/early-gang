# imports
from libraries.charityDonoTTS import *
from libraries.chatPlays import *
from libraries.autoStream import *

# main code loop
async def main():

    # setting up
    await connectToObs()
    await chatPlays.updateSnatus()

    # so you don't have to restart stream
    if await isLive(yourChannelName):
        await startTTS()
        await startChatPlays()
        await startAutoSave()
        await startIdleBot()
        await startInputBot()

    # infinite loop to check stream statuses
    while True:

        # if streamer goes live
        if await isLive(yourChannelName) and await isLive(streamerChannelName):

            # shut down everything
            if ttsOn:
                await stopTTS()
            if chatPlaying:
                await stopChatPlays()
            if idleBotPlaying:
                await stopIdleBot()
            if inputBotPlaying:
                await stopInputBot()
            if autoSaving:
                await stopAutoSave()

            # end stream
            if await isLive(yourChannelName):
                await raid(yourChannelName, streamerChannelName)
                await stopStream()

        # if streamer goes offline
        elif not await isLive(yourChannelName) and not await isLive(streamerChannelName):

            # start stream
            if not await isLive(yourChannelName):
                await startStream()
            if not ttsOn:
                await startTTS()
            if not chatPlaying:
                await startChatPlays()
            if not autoSaving:
                await startAutoSave()
            if not idleBotPlaying:
                await startIdleBot()
            if not inputBotPlaying:
                await startInputBot()

        await asyncio.sleep(3)


# don't touch this
try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()
except Exception as e:
    print(e)

