# Twitch Admin Panel
An administrative control panel written in Python

-----------------------------
## How to use

### Linux
1. Install `python3`
	* This has been tested with 3.10.6, running older versions is unsupported.
	* Check this with `python3 --version` in your terminal
2. Clone the project and enter it.
3. Create a folder called files.
4. In this folder, create two JSON files: `commands.json` and `secrets.json`.
5. In `secrets.json`, add your bot's username, your twitch channel name, and your oauth token
	* You can get this from https://twitchapps.com/tmi/


Copy and paste commands:
```bash
git clone --recursive https://github.com/TotallyMonica/twitch-admin
cd twitch-admin
mkdir files
touch {commands,secrets}.json
```

## To do - Chatbot
 * ~~Keep alive~~ Done September 19th 2022
 * Process who sent what
 	* `simulate-user.py` is the current testing ground for this
 	* ~~Manage badges~~ Done on September 19th 2022
 * Join different channel
 	* Done in theory, possible argument to override this?
 * Load custom secrets
 * ~~Add commands~~ Done on September 19th, 2022
 * ~~Import commands from Json/CSV~~ Done on September 18th, 2022
 * First time startup for commands and secrets