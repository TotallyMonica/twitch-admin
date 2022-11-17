#!/usr/bin/env python3

'''
Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

    http://aws.amazon.com/apache2.0/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

Modifications 2021 by RikiRC

Adaptation to Helix 2022 by TotallyMonica
'''

import irc.bot, requests, json, threading, time, sys

class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, client_id, client_secret, token, channel, chat):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token.removeprefix("oauth:")
        self.channel = '#' + channel.lower()
        self.chat = chat

        # Get the channel id, we will need this for v5 API calls
        body = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials'
        }
        keys = requests.post('https://id.twitch.tv/oauth2/token', body).json()
        url = 'https://api.twitch.tv/helix/users?login=' + channel
        headers = {
            'Client-ID': client_id,
            'Authorization': 'Bearer ' + keys['access_token']
        }

        r = requests.get(url, headers=headers).json()

        self.channel_id = r['data'][0]['id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        url = 'https://api.twitch.tv/helix/users?login=' + channel
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+self.token)], username, username)

    def on_welcome(self, c, e):
        print('Joining ' + self.channel)

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)
        print('Joined ' + self.channel)
        # c.privmsg(self.channel, "Connected!")

    def on_pubmsg(self, c, e):
        # If a chat message starts with an exclamation point, try to run it as a command
        pointer = e.source.index('!')
        author = e.source[:pointer]
        channel = e.target[1:]
        output = f'{author}@{channel}: {e.arguments[0]}'
        
        print(output)

        if self.chat:
            # Make chat readable for OBS
            with open('chat.txt', 'a') as filp:
                pointer = 0

                for char in output:
                    filp.write(char)
                    pointer += 1

                    if pointer == 30:
                        pointer = 0
                        filp.write('\n')
                    
                filp.write('\n')
        
        if e.arguments[0][:1] == '!':
            cmd = e.arguments[0].split(' ')[0][1:]
            print('Received command: ' + cmd)
            self.do_command(e, cmd)
        return

    def do_command(self, e, cmd):
        c = self.connection

        # Poll the API to get current game.
        if cmd == "game":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, str(r['display_name']) + ' is currently playing ' + str(r['game']))

        # Poll the API the get the current status of the stream
        elif cmd == "title":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, str(r['display_name']) + ' channel title is currently ' + str(r['status']))

        # Provide basic information to viewers for specific commands
        elif cmd == "raffle":
            message = "This is an example bot, replace this text with your raffle text."
            c.privmsg(self.channel, message)
        elif cmd == "schedule":
            message = "This is an example bot, replace this text with your schedule text."
            c.privmsg(self.channel, message)

        # The command was not recognized
        else:
            c.privmsg(self.channel, "Did not understand command: " + cmd)

def manageTextSize(length=25):
    while True:
        lines = []

        # Load the chat file, each line as its own item
        with open('chat.txt', 'r') as filp:
            print(filp)

            lines = filp.read().split('\n')
            print(lines)
        
        # Determine if the chat needs to be cleaned up
        if len(lines) > length:
            newLines = lines[-length:]

            # Write new purged chat
            with open('chat.txt', 'w') as filp:
                for line in newLines:
                    pointer = 0
                    filp.write(line)
                    pointer += 1
                    
                    if pointer == 30:
                        filp.write('\n')

                    if not line == newLines[-1]:
                        filp.write('\n')
        time.sleep(0.1)


def main():
    # Load secrets
    with open('secrets.json') as filp:
        secrets = json.load(filp)

    if '--chat' in sys.argv:
        chat = True
    else:
        chat = False

    # Clear out chat
    with open('chat.txt', 'w') as filp:
        filp.write("")
    
    print('Waiting 20 seconds to help prevent ratelimiting issues')
    time.sleep(20)

    # Initialize client 1
    majorBot = TwitchBot(secrets['username'], secrets['client_id'], secrets['client_secret'], secrets['token'], 'alpharad')
    majorThread = threading.Thread(target=majorBot.start, name='majorThread')
    majorThread.start()

    # Initialize client 2
    time.sleep(20)
    tygrBot = TwitchBot(secrets['username'], secrets['client_id'], secrets['client_secret'], secrets['token'], 'codemiko', chat)
    tygrThread = threading.Thread(target=tygrBot.start, name='tygrThread')
    tygrThread.start()

    if chat:
        # Ensure the chat doesn't get too long
        cleanChatThread = threading.Thread(target=manageTextSize, name = 'cleanChatThread')
        cleanChatThread.start()

if __name__ == "__main__":
    main()
