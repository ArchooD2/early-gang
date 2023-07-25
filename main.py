
# imports
from bots.twitch import pollBot, commandBot, econBot
from bots.discord import gwrbullBot, ramcicleBot, sna1lBot, fizzyghostBot, birdmanBot, discordCommandBot
from libraries.charityDonoTTS import *
from libraries.chatPlays import *
from libraries.autoStream import *

# main code loop
async def main():

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

# run main and all your other background tasks here
async def setup():
    await asyncio.gather(connectToObs(), chatPlays.updateSnatus(), pollBot.Bot().start(), commandBot.Bot().start(), econBot.Bot().start(), discordCommandBot.bot.start(discordCommandBot.commandBotToken), gwrbullBot.bot.start(gwrbullBot.gwrbullBotToken), ramcicleBot.bot.start(ramcicleBot.ramcicleBotToken), sna1lBot.bot.start(sna1lBot.sna1lBotToken), birdmanBot.bot.start(birdmanBot.birdmanBotToken), fizzyghostBot.bot.start(fizzyghostBot.fizzyghostBotToken), asyncio.create_task(main()))

# don't touch this
try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup())
    loop.run_forever()
except Exception as e:
    print(e)