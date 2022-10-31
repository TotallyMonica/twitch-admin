#!/usr/bin/env python3
import socket
import irc.bot
import json
import threading
import time
import sys
import os
from datetime import datetime
import traceback

import parse.message as message
#import parse.args as argparse

def init(waitLength=1):
    global PREFIX
    global USERNAME
    global CHANNEL
    global twitch

    with open("files/secrets.json", "r") as filp:
        secrets = json.load(filp)

    print("Opened secrets")

    # Define login information
    SERVER = 'irc.chat.twitch.tv'
    PORT = 6667
    USERNAME = secrets['username']
    TOKEN = secrets['oauth']
    CHANNEL = f"#{secrets['channels'][0]}"
    PREFIX = secrets['prefix']
    URL = 'https://api.twitch.tv/kraken/users?login=' + CHANNEL

    try:
    # Connect with twitch
        twitch = socket.socket()
        twitch.connect((SERVER, PORT))
        print("Connected to twitch")

        # Authenticate with twitch
        twitch.send(f'PASS {TOKEN}\n'.encode('utf-8'))
        print("Logged in with the oauth token")
        twitch.send(f'CAP REQ :twitch.tv/tags twitch.tv/membership twitch.tv/commands\n'.encode('utf-8'))
        print("Retrieved tags")
        twitch.send(f'NICK {USERNAME}\n'.encode('utf-8'))
        print(f"Username set to {USERNAME}")
        twitch.send(f'JOIN {CHANNEL}\n'.encode('utf-8'))
        print(f"Joined channel {CHANNEL}")

    except ConnectionResetError:
        print(f"Connection got reset, retrying in {waitLength} seconds...")
        time.sleep(waitLength)
        init(waitLength * 2)

def sendMsg(msg, msgType="PRIVMSG"):
    msgType = msgType.upper()

    if msgType == "PONG":
        formattedMsg = f'{msgType} :tmi.twitch.tv\n'
    else:
        formattedMsg = f'{msgType} {CHANNEL} :{msg}\n'

    if verbose:
        print("Sending " + formattedMsg)

    twitch.send(formattedMsg.encode('utf-8'))

def readCommand(chatMsg):
    requestedCmd = ""
    requestedArgs = []
    # Open the commands database
    # With its current configuration the bot can still be running and an updated database can be provided
    with open('files/commands.json', 'r') as filp:
        database = json.load(filp)

    # Make the chat message provided friendly
    try: 
        requestedCmd = chatMsg['botCommand']
    except KeyError:
        return None
    
    try:
        requestedArgs = chatMsg['botCommandParams'].split(" ")
    except KeyError:
        requestedArgs = []

    # Check to see if an alias was used
    for cmd in database:
        try:
            for alt in database[cmd]['alias']:
                if requestedCmd == alt:
                    if verbose: 
                        print(f"{requestedCmd} matches alias {alt} for {cmd}")
                    requestedCmd = cmd

        except KeyError:
            if verbose:
                print(cmd + " has no aliases")

    # Check if requested command is in the database
    # First, remove the prefix and the newline at the end
    if requestedCmd in database:
        chatCmd = requestedCmd
        output = database[chatCmd]['output']

        msg = database[requestedCmd]['output']

        if verbose:
            print(f"{chatCmd} was sent")

        sendMsg(msg)

    elif verbose:
        print(f"Received invalid command {chatMsg['botCommand']}")

def running():
    if logging:
        filename = f'chat-{CHANNEL}-{datetime.now()}.log'

    try:
        while True:
            rawResp = twitch.recv(2048)
            resp = rawResp.decode('utf-8')

            if len(resp) != 0:
                print(f"\n{datetime.now()}: Got message")
                chatMsg = message.parseRawMsg(resp)

                if verbose:
                    print(resp + "\n")
                    # print(chatMsg)

                # Run if a command was requested
                if chatMsg and chatMsg['command']['command'] == "PRIVMSG":
                    print(chatMsg)
                    print(chatMsg['command'])

                    with open(filename, 'a') as chat:
                        chat.write(f"{datetime.now()}: {resp}\n")

                print("Waiting for message...")
                resp = None

            else:
                print("Something broke. Put your break point here!")
                twitch.send(f'PART\n'.encode('utf-8'))
                twitch.close()
                time.sleep(5)
                init()

    # Catch all exceptions, if you constantly connect and disconnect Twitch thinks your DDoSing them.
    except Exception as e:
        print("An unexpected error occurred.")
        print("Error:")
        traceback.print_exc()
        print("Would you like to keep running?")
        userInput = input("(y/n): ")
        if userInput.lower() == 'y':
            print('Attempting to rerun. If this happens again you might want to check your commands json.')
            running()
        elif userInput.lower() == 'n':
            print("Exiting...")
        else:
            print("Invalid input detected. Defaulting to no.")
            print("Exiting...")

def main():
    init()
    running()
    twitch.close()

if __name__ == "__main__":
    global verbose
    global logging

    verbose = True
    logging = True

    try: 
        main()
    except KeyboardInterrupt:
        print("^C received, exiting.")
        print("Cleaning up...")
        twitch.close()

        print("Thanks for using my chatbot!")
        print("Leave any feedback on the github page, https://github.com/TotallyMonica/twitch-admin")
