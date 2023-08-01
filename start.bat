@echo off

start /B py main.py
start /B py bots/twitch/commandBot.py
start /B py bots/twitch/econBot.py
start /B py bots/twitch/pollBot.py
start /B py bots/discord/sna1lBot.py
start /B py bots/discord/ramcicleBot.py
start /B py bots/discord/gwrbullBot.py
start /B py bots/discord/fizzyghostBot.py
start /B py bots/discord/actualbirdmanBot.py

pause
