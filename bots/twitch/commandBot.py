# responds to basic commands in chat
# don't fuck with this too much unless you're familiar with twitchio and how it works
# not much documentation here because even i don't know what the fuck this object oriented programming is doing in python
import base64
# imports
from urllib.parse import urlencode
from bots.twitch.econBot import *
import aiosqlite
from libraries.chatPlays import *

# reading config
config = configparser.ConfigParser()
config.read(os.path.abspath((os.path.join(directory, "config.ini"))))
spotifyClientID = config.get("spotify", "client id")
spotifyClientSecret = config.get("spotify", "client secret")
spotifyRefreshToken = config.get("spotify", "spotify refresh token")

# if you don't have a refresh token
if spotifyRefreshToken == "":

    # getting code from user
    print(f'authorize this script by going to:\n{"https://accounts.spotify.com/authorize" + "?" + urlencode({"client_id": spotifyClientID, "response_type": "code", "redirect_uri": "http://localhost:8888/callback", "scope": "user-read-currently-playing user-modify-playback-state"})}')
    authorizationCode = input("enter the authorization code found in the redirected url after \"code=\": ")

    # gets access token and refresh token using the code
    response = requests.post("https://accounts.spotify.com/api/token", auth = (spotifyClientID, spotifyClientSecret), data = {"grant_type": "authorization_code", "code": authorizationCode, "redirect_uri": "http://localhost:8888/callback"})

    # writes refresh token to info file for future use
    if 'refresh_token' in response.json():
        with open(os.path.abspath((os.path.join(directory, "config.ini"))), 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if line.startswith("spotify refresh token ="):
                    lines[i] = "spotify refresh token = " + response.json()["refresh_token"] + "\n"
                    break
            with open(os.path.abspath((os.path.join(directory, "config.ini"))), "w") as file:
                file.writelines(lines)
    else:
        print("problem getting tokens " + response.json())

class Bot(commands.Bot):

    # sets up bot and connects to twitch
    def __init__(self):
        super().__init__(token = accessToken, prefix="!", initial_channels = [yourChannelName])

    # when someone sends a message in chat
    async def event_message(self, message):

        # don't take bot messages as real messages
        if message.echo:
            return

        # checking for inputs
        if chatPlays.chatPlaying and message.content[0] != "!":
            await asyncio.create_task(controller(message.content))
            chatPlays.timeSinceLastMessage = time.time()

        # reading database
        async with databaseLock:
            async with aiosqlite.connect(os.path.abspath(os.path.join(directory, "chatData.db"))) as db:
                cursor = await db.cursor()
                await cursor.execute("SELECT * FROM chatters WHERE id = ?", (await getBroadcasterId(message.author.name),))
                result = await cursor.fetchone()

                # sending welcome message if id isn't in database
                if not result:
                    await cursor.execute("INSERT INTO chatters (id) VALUES (?)", (await getBroadcasterId(message.author.name),))
                    await db.commit()
                    await self.connected_channels[0].send("[bot] welcome " + message.author.name + " to early_gang, where we play games and vibe while we wait for dougdoug to stream again. right now we are trying to beat a randomized pokemon white before dougdoug streams again. the controls are up, down, right, start, a, b, x, and y (more at !controls) and additionally the snack family may try to \"help\" you out. enjoy!")

        await self.handle_commands(message)

    # sends list of chat plays controls
    @commands.command()
    async def controls(self, ctx: commands.Context):
        await ctx.send("[bot] (capitalization doesnt matter) up, down, left, right, hold up, hold down, hold left, hold right, a, hold a, mash a, b, hold b, mash b, x, y, l, r, start, select, stop, wander, up wander, down wander, left wander, right wander, north, south, east, west")

    # sends what's going on
    @commands.command()
    async def what(self, ctx: commands.Context):
        await ctx.send("[bot] chat tries to beat randomised pokemon white before dougdoug streams again")

    # sends dougdoug channel link
    @commands.command()
    async def dougdoug(self, ctx: commands.Context):
        await ctx.send("[bot] https://www.twitch.tv/dougdoug")

    # ROGGED BUT FERN
    @commands.command()
    async def RIGGED(self, ctx: commands.Context):
        await ctx.send("[bot] BUT FAIR")

    # sus
    @commands.command()
    async def areYouAnImposter(self, ctx: commands.Context):
        await ctx.send("no, no I am not. I am the original early gang, beep bop boop.")

    # sends a list of all the bots
    @commands.command()
    async def bots(self, ctx: commands.Context):
        await ctx.send("[bot] input bot, aka chris snack, presses a random button every minute or so, idle bot steals your controller if you leave it alone for five minutes, and theres a 5% chance of your own input being completely random or the opposite")

    # sends a list of commands
    @commands.command()
    async def menu(self, ctx: commands.Context):
        await ctx.send("[bot] !what, !bots, !song, !controls, !vote, !poll, !discord, !watchtime, !bp, !donate, !playlist, !bpShop")

    # sends link to discord
    @commands.command()
    async def discord(self, ctx: commands.Context):
        await ctx.send("[bot] https://discord.gg/eYSUuqNUvb")

    # sends link to tiltify page
    @commands.command()
    async def donate(self, ctx: commands.Context):
        await ctx.send("[bot] https://tiltify.com/@early-gang/profile")

    # sends link to stream music playlist
    @commands.command()
    async def playlist(self, ctx: commands.Context):
        await ctx.send("[bot] https://open.spotify.com/playlist/0GhV1AmrhugyYsCb8gEHsS?si=02930e0a7cd54a03")

    # lets sna1l raid
    @commands.command()
    async def raid(self, ctx: commands.Context):
        if ctx.author.name == "sna1l_boy":
            ctx.message.content = ctx.message.content.replace("!raid ", "")
            await raid(yourChannelName, ctx.message.content)
            await openGame()

    # lets sna1l mod people
    @commands.command()
    async def mod(self, ctx: commands.Context):
        if ctx.author.name == "sna1l_boy":
            ctx.message.content = ctx.message.content.replace("!mod ", "")
            requests.post("https://api.twitch.tv/helix/moderation/moderators?broadcaster_id=" + await getBroadcasterId(yourChannelName) + "&user_id=" + await getBroadcasterId(ctx.message.content), headers={"Authorization": f"Bearer {accessToken}", "Client-Id": clientID})

    # sends a message with the currently playing song
    @commands.command()
    async def song(self, ctx: commands.Context):
        async with aiohttp.ClientSession() as session:

            # create access token
            async with session.post("https://accounts.spotify.com/api/token", headers={"Authorization": "Basic " + base64.b64encode(f"{spotifyClientID}:{spotifyClientSecret}".encode()).decode()}, data={"grant_type": "refresh_token", "refresh_token": spotifyRefreshToken}) as response:
                data = await response.json()
                if "access_token" in data:
                    accessToken = data["access_token"]
                else:
                    print("error refreshing token: " + data)
                    accessToken = None

            # get song
            if accessToken:
                async with session.get("https://api.spotify.com/v1/me/player/currently-playing", headers = {"Authorization": "Bearer " + accessToken}) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data['is_playing']:
                            await ctx.send(f"[bot] {data['item']['name']} by {data['item']['artists'][0]['name']}")
                        else:
                            await ctx.send("[bot] no song playing")
                    else:
                        await ctx.send("[bot] can't get song")