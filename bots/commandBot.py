# responds to basic commands in chat
# dont fuck with this too much unless youre familiar with twitchio and how it works
# not much documentation here because even i dont know what the fuck this object oriented programming is doing in python

import threading
import csv
from twitchio.ext import commands
from libraries.autoStream import *
import requests
from urllib.parse import urlencode
import os
from datetime import datetime, timezone

# starts command bot
def startCommandBot():
    bot = Bot()
    botThread = threading.Thread(target=bot.run)
    botThread.start()
    return botThread

# bot commands class
class Bot(commands.Bot):

    # sets up bot and connects to twitch
    def __init__(self):
        super().__init__(token = accessToken, prefix="!", initial_channels = [yourChannelName])

    @commands.command()
    async def controls(self, ctx: commands.Context):
        await ctx.send("[bot] (capitilization doesnt matter) up, down, left, right, hold up, hold down, hold left, hold right, a, hold a, mash a, b, hold b, mash b, x, y, l, r, start, select, stop, wander, up wander, down wander, left wander, right wander, north, south, east, west")

    @commands.command()
    async def what(self, ctx: commands.Context):
        await ctx.send(
            "[bot] chat tries to beat randomised pokemon heart gold before dougdoug streams again")

    @commands.command()
    async def dougdoug(self, ctx: commands.Context):
        await ctx.send("[bot] https://www.twitch.tv/dougdoug")

    @commands.command()
    async def RIGGED(self, ctx: commands.Context):
        await ctx.send("[bot] BUT FAIR")

    @commands.command()
    async def areYouAnImposter(self, ctx: commands.Context):
        await ctx.send("no, no I am not. I am the original early gang, beep bop boop.")

    @commands.command()
    async def bots(self, ctx: commands.Context):
        await ctx.send("[bot] input bot, aka chris snack, presses a random button every minute or so, idle bot steals your controller if you leave it alone for five minutes, and theres a 5% chance of your own input being completely random or the opposite")

    @commands.command()
    async def menu(self, ctx: commands.Context):
        await ctx.send("[bot] !what, !bots, !song, !controls, !vote, !poll, !discord, !watchtime, !bp, !donate")

    @commands.command()
    async def discord(self, ctx: commands.Context):
        await ctx.send("[bot] https://discord.gg/eYSUuqNUvb")

    @commands.command()
    async def donate(self, ctx: commands.Context):
        await ctx.send("[bot] https://tiltify.com/@early-gang/profile")

    @commands.command()
    async def song(self, ctx: commands.Context):
        global config

        # reading config
        clientId = config.get("spotify", "client id")
        clientSecret = config.get("spotify", "client secret")
        refreshToken = config.get("spotify", "refresh token")

        # if you already made a refresh token
        if refreshToken:
            # create access token
            response = requests.post("https://accounts.spotify.com/api/token", auth = (clientId, clientSecret), data = {"grant_type": "refresh_token", "refresh_token": refreshToken})
            data = response.json()
            if "access_token" in data:
                accessToken = data["access_token"]
            else:
                print(f"error refreshing token: {data}")
                accessToken = None

                # makes another refresh token if cant create access token for whatever reason
            if accessToken == None:
                # gets authorization code from user
                print(f'authorize this script by going to:\n{"https://accounts.spotify.com/authorize" + "?" + urlencode({"client_id": clientId, "response_type": "code", "redirect_uri": "http://localhost:8888/callback", "scope": "user-read-currently-playing"})}')
                authorizationCode = input("enter the authorization code found in the redirected url after \"code=\": ")

                # gets access token and refresh token using the code
                response = requests.post("https://accounts.spotify.com/api/token", auth = (clientId, clientSecret),data = {"grant_type": "authorization_code", "code": authorizationCode, "redirect_uri": "http://localhost:8888/callback"})
                data = response.json()
                if "access_token" in data and 'refresh_token' in data:
                    accessToken = data['access_token']
                    refreshToken = data['refresh_token']
                    # writes refresh token to info file for future use
                    with open(os.path.abspath((os.path.join(directory, "config.ini"))), "a") as file:
                        file.write(refreshToken)
                else:
                    print(f"problem getting tokens: {data}")

                # writes refresh token to info file for future use
                with open(os.path.abspath((os.path.join(directory, "config.ini"))), "a") as file:
                    file.write(refreshToken)

        # if you have no refresh token
        else:
            # gets authorization code from user
            print(f'authorize this script by going to:\n{"https://accounts.spotify.com/authorize" + "?" + urlencode({"client_id": clientId, "response_type": "code", "redirect_uri": "http://localhost:8888/callback", "scope": "user-read-currently-playing"})}')
            authorizationCode = input("enter the authorization code found in the redirected url after \"code=\": ")

            # gets access token and refresh token using the code
            response = requests.post("https://accounts.spotify.com/api/token", auth = (clientId, clientSecret), data = {"grant_type": "authorization_code", "code": authorizationCode,"redirect_uri": "http://localhost:8888/callback"})
            data = response.json()
            if 'access_token' in data and 'refresh_token' in data:
                accessToken = data['access_token']
                refreshToken = data['refresh_token']
                # writes refresh token to info file for future use
                with open(os.path.abspath((os.path.join(directory, "config.ini"))), "a") as file:
                    file.write(refreshToken)
            else:
                print(f"problem getting tokens: {data}")

        # finally actually get and send playing song
        response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers = {"Authorization": f"Bearer {accessToken}"})
        if response.status_code == 200:
            data = response.json()
            if data['is_playing']:
                await ctx.send(f"[bot] {data['item']['name']} by {data['item']['artists'][0]['name']}")
            else:
                await ctx.send("[bot] no song playing")
        else:
            await ctx.send("[bot] cant get song")
