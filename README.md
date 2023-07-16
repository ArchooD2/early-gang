## how the fuck do i use this?!??!?!

### part I - shit you need to install
- [python](https://www.python.org/downloads/)
- [requests](https://pypi.org/project/requests/)
- [PyAutoGUI](https://pypi.org/project/PyAutoGUI/)
- [pillow](https://pypi.org/project/Pillow/)
- [openCV](https://pypi.org/project/opencv-python/)
- [twitchChatIrc](https://pypi.org/project/twitch-chat-irc/)
- [pynput](https://pypi.org/project/pynput/)
- [twitchio](https://pypi.org/project/twitchio/)
- [obs](https://obsproject.com/)
- [obs-websocket](https://obsproject.com/forum/resources/obs-websocket-remote-control-obs-studio-using-websockets.466/)
- [obs-websocket-py](https://pypi.org/project/obs-websocket-py/)
- [pyttsx3](https://pypi.org/project/pyttsx3/)

### part II - setting up the script
- download the .zip
- unzip the folder and open config.ini in a text editor
- fill in each line for each section you plan on using
- if you're using chatPlays.py be sure to change the controller to fit whatever game you're using it for
- once you have the config set up can run the script

### part III - setting up twitch
- log into your [dev account](https://dev.twitch.tv/)
- go to "name's Console" then "Applications"
- click "Register Application" and fill out all the information boxes however you want but add "http://localhost/" as the redirect url
- go back to "Applications" then click "Manage" on the one you just made
- you should see "Client ID" near the bottom of the page
- paste said id into the twitch client id section in the python file
- paste "https://id.twitch.tv/oauth2/authorize?client_id=CLIENT_ID_HERE&redirect_uri=http://localhost/&response_type=token&scope=viewing_activity_read+channel:manage:raids+chat:edit+chat:read+moderator:manage:banned_users+moderator:read:chatters+channel:manage:moderators" into your browser
- replace "CLIENT_ID_HERE" with your id and go to the url
- you should be redirected to a new url that contains "access_token="
- copy and paste that long ass string into the twitch access token section

### part IV - setting up spotify
  - login to [spotify developers](https://developer.spotify.com/) and go to your dashboard
  - click "Create App" and set http://localhost:8888/callback as the redirect url
  - go to the app then click "Settings" and you should see "Client ID" and "Client secret" near the top
  - paste these into your config file at their respective locations
  - refresh token will be generated by the script so leave it blank for now

### part V - setting up obs
  - open obs and click on "Tools" at the top
  - if you installed obs-websockets correctly there should be a "WebSockets Sever Settings (4.x) Compat" button in the dropdown
  - click it and make sure it the "Enable Websockets server" box is checked as well as the "Enable authentication" box
  - change the "Password" field to whatever password you want then update the respective line in the config file
  - in whatever scene you want the tts to show in, create two text sources called "tts body" and "tts header"
  - style these however you want but make sure to check the "Read from file" tbox in the properties menu and give it the directories of ttsHeader.txt or ttsBody.txt respectively
  - do the same with another text source but called "snack status" for snackStatus.txt

### part VI - setting up tiltify
  - login to [tiltify developers](https://app.tiltify.com/developers)
  - click "Create application" and enter "https://localhost/" as the redirect url
  - once the app is created, scroll down and you should see "Client ID" and "Client Secret" at the bottom
  - paste these into the config file
  - go to "https://v5api.tiltify.com/oauth/authorize?client_id=CLIENT_ID_HERE&redirect_uri=https%3A%2F%2Flocalhost%2F&response_type=code&scope=public" after replacing "CLIENT_ID_HERE" with yours
  - paste the text after "code=" in the url into the config file

### part VII - setting up discord
  - login to [discord developers](https://discord.com/developers/applications)
  - make a new application for each discord bot you're using
  - in the app's bot settings right under username click to make a token then paste it into the config

### questions? comments? concerns?
### message kai_2910 on discord for the best chance of a timely response :)
