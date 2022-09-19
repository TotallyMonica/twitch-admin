# Twitch Admin Panel
An administrative control panel written in Python

-----------------------------
## How to use
1. Install `python3`
	* This has been tested with 3.10.6, running older versions is unsupported.
	* Check this with `python3 --version` in your terminal
2. Clone the project and enter it.
3. Install the packages from `required.txt`
3. Create a folder called files.
4. In this folder, create two JSON files: `commands.json` and `secrets.json`.
5. In `secrets.json`, add your bot's username, your twitch channel name, and your oauth token in json format
	* You can get this from https://twitchapps.com/tmi/
6. In `commands.json`, add what commands you would like
7. Run `bot.py`


Copy and paste commands (Linux):
```bash
git clone --recursive https://github.com/TotallyMonica/twitch-admin
cd twitch-admin
pip3 install -r requirements.txt
mkdir files
touch files/{commands,secrets}.json
echo '{
  "username": "<REPLACE ME>",  
  "channel": "<REPLACE ME>", 
  "oauth": "<REPLACE ME>",  
  "prefix": ""  
}' > files/secrets.json
echo '{
        "command1": {
                "output": "This is an output",
                "alias": ["cmd1", "1"],
                "calls": ["help", "test", "hello"]
        },
        "test": {
                "output": "Test successful!"
        },
        "hello": {
                "output": "Hello, world!",
                "alias": ["world", "hw"]
        },
        "help": {
                "output": "All I do is talk, what do I know?",
                "calls": ["test", "hello"]
        },
        "alloftheabove": {
                "calls": ["help", "hello", "test", "command1"],
                "alias": ["aota", "all", "runall", "ra"]
        }
}' > files/commands.json
chmod +x bot.py
./bot.py
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