#!/usr/bin/env python3

# Custom libraries
from chatbot.chatbot import TwitchBot
from timer.Timer import timer

# Misc libraries
import json
import threading
from os import system, name, getcwd

def menu():
    while True:
        if name == 'nt':
            system('cls')
        elif name == 'posix':
            system('clear')

        print("TotallyMonica's Twitch Dashboard")
        print("--------------------------------")

        print("Options:")
        print("\t1. Start a timer")
        print("\t2. Load a chat")
        userInput = input()

        if userInput == '1':
            print("How long?")
            length = input()
            timerThread = threading.Thread(target=timer, args=(length), daemon=True)
        elif userInput == '2':
            print("Which chat?")
            chat = input()
            chatBot = TwitchBot(secrets['username'], secrets['client_id'], secrets['client_secret'], secrets['token'], chat)
            chatThread = threading.Thread(target=chatBot.start, name='chatThread', daemon=True)

def main():
    global secrets
    with open('files/secrets.json') as filp:
        secrets = json.load(filp)
    
    # Initialize chatbot
    chatBot = TwitchBot(secrets['username'], secrets['client_id'], secrets['client_secret'], secrets['token'], secrets['channel'])
    chatThread = threading.Thread(target=chatBot.start, name='chatThread', daemon=True)
    chatThread.start()

    # Initialize timer
    timerThread = threading.Thread(target=timer, args=("2:00", "It's start time!" f'{getcwd()}/timer.txt'), daemon=True)
    timerThread.start()

    menu()
if __name__ == "__main__":
    main()