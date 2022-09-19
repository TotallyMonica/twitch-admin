#!/usr/bin/env python3
import socket
import json
import irc
import threading
import parse.message as message

def init():
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
    USERNAME = 'majoryoshibot'
    TOKEN = secrets['oauth']
    CHANNEL = '#' + 'majoryoshi' #secrets['channel']
    PREFIX = secrets['prefix']

    # Connect with twitch
    twitch = socket.socket()
    twitch.connect((SERVER, PORT))
    print("Connected to twitch")

    # Authenticate with twitch
    twitch.send(f'PASS {TOKEN}\n'.encode('utf-8'))
    print("Logged in with the oauth token")
    twitch.send(f'CAP REQ :twitch.tv/tags twitch.tv/commands\n'.encode('utf-8'))
    print("Retrieved tags")
    twitch.send(f'NICK {USERNAME}\n'.encode('utf-8'))
    print(f"Username set to {USERNAME}")
    twitch.send(f'JOIN {CHANNEL}\n'.encode('utf-8'))
    print(f"Joined channel {CHANNEL}")

def sendMsg(msg, msgType="PRIVMSG"):
    msgType = msgType.upper()

    if msgType == "PONG":
        formattedMsg = f'{msgType} :tmi.twitch.tv\n'
    else:
        formattedMsg = f'{msgType} {channel} :{msg}\n'

    if verbose:
        print("Sending " + formattedMsg)

    twitch.send(formattedMsg.encode('utf-8'))

def readCommand(chatMsg):
    # Open the commands database
    # With its current configuration the bot can still be running and an updated database can be provided
    with open('files/commands.json', 'r') as filp:
        database = json.load(filp)

    # Make the chat message provided friendly
    requestedCmd = chatMsg['botCommand'].lower().lstrip()

    while "\n" in requestedCmd or "\b" in requestedCmd:
        print(chatMsg)
        print("Remove another char?")
        userInput = input("y/n: ")
        if userInput.lower() == 'y':
            requestedCmd = requestedCmd[0:-1]
        elif userInput.lower() == 'n':
            break

    if requestedCmd[-1] == "\n":
        print(b'{requestCmd}')


    # Check to see if an alias was used
    for cmd in database['commands']:
        try:
            for alt in database['commands'][cmd]['alias']:
                if requestedCmd == alt:
                    if verbose: 
                        print(f"{requestedCmd} matches alias {alt} for {cmd}")
                    requestedCmd = cmd

        except KeyError:
            if verbose:
                print(cmd + " has no aliases")

    # Check if requested command is in the database
    # First, remove the prefix and the newline at the end
    if requestedCmd in database["commands"]:
        chatCmd = requestedCmd
        output = database["commands"][chatCmd]['output']

        msg = database['commands'][requestedCmd]['output']

        if verbose:
            print(f"{chatMsg[0]} sent {chatCmd}")
        
        sendMsg(msg)

    elif verbose:
        print(f"Received invalid command {chatMsg['botCommand']}")

def running():
    # try:
    while True:
        resp = twitch.recv(2048).decode('utf-8')

        if verbose:
            print(resp)

        if resp != "":
            if verbose:
                print(resp)

            chatMsg = message.parseRawMsg(resp)
            print(chatMsg)
            # Handle twitch's keep alives
            if resp == 'PING':
                twitch.send('PONG ' + parsedMessage)

            # Run if a command was requested
            elif chatMsg != None and chatMsg['command']['command'] == "PRIVMSG":
                readCommand(chatMsg['command'])

    # Catch all exceptions, if you constantly connect and disconnect Twitch thinks your DDoSing them.
    # except Exception as e:
    #     print("An unexpected error occurred.")
    #     print("Error:")
    #     print(e)
    #     print("Would you like to keep running?")
    #     userInput = input("(y/n): ")
    #     if userInput.lower() == 'y':
    #         print('Attempting to rerun. If this happens again you might want to check your commands json.')
    #         running()
    #     elif userInput.lower() == 'n':
    #         print("Exiting...")
    #     else:
    #         print("Invalid input detected. Defaulting to no.")
    #         print("Exiting...")

def main():
    init()
    running()
    twitch.close()

if __name__ == "__main__":
    global verbose
    verbose = True
    try: 
        main()
    except KeyboardInterrupt:
        print("^C received, exiting.")
        print("Cleaning up...")
        twitch.close()

        print("Thanks for using my chatbot!")
        print("Leave any feedback on the github page, https://github.com/TotallyMonica/twitch-admin")