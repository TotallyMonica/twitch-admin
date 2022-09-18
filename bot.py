#!/usr/bin/env python3
import socket
import json
import irc

def init():
    global prefix
    global nickname
    global channel

    with open("files/secrets.json", "r") as filp:
        secrets = json.load(filp)

    print("Opened secrets")

    server = 'irc.chat.twitch.tv'
    port = 6667
    nickname = 'majoryoshibot'
    token = secrets["oauth"]
    channel = '#' + secrets['channel']
    prefix = secrets['prefix']

    sock = socket.socket()
    sock.connect((server, port))
    print("connected")

    sock.send(f'PASS {token}\n'.encode('utf-8'))
    print("logged in")

    sock.send(f'NICK {nickname}\n'.encode('utf-8'))
    print(f"Nickname set to {nickname}")

    sock.send(f'JOIN {channel}\n'.encode('utf-8'))
    print(f"Joined channel {channel}")

    return sock

def parseMsg(ircMsg):
    sender = ""
    chatMsg = ""
    # Split that simulated message to be parsed, then print output
    splitIrc = ircMsg.split(':')
    
    for char in splitIrc[1]:
        if char == ':':
            continue
        elif char == '!':
            break
        else:
            sender = sender + char

    if sender == nickname:
        return

    # Check to make sure the split irc output is exactly a length of 3
    # If it isn't it's likely the sender used a : in their message
    if len(splitIrc) == 3:
        chatMsg = splitIrc[2]
    elif len(splitIrc) > 3:
        for part in splitIrc:
            if not part == splitIrc[0] and not part == splitIrc[1]:
                if part == splitIrc[-1]:
                    chatMsg = chatMsg + part
                else:
                    chatMsg = chatMsg + part + ":"

    # Don't include newlines in output
    chatMsg = chatMsg[0:-1]

    return [sender, chatMsg]

def sendMsg(msg):
    formattedMsg = f'PRIVMSG {channel} :{msg}\n'
    print("Sending " + formattedMsg)
    server.send(formattedMsg.encode('utf-8'))

def readCommand(chatMsg):
    # Open the commands database.
    # With its current configuration the bot can still be running and an updated database can be provided
    with open('files/commands.json', 'r') as filp:
        commands = json.load(filp)

    # Make the chat message provided friendly
    requestedCmd = chatMsg[1][1:-1].lower()

    # Check if requested command is in the database.
    # First, remove the prefix and the newline at the end
    if requestedCmd in commands["commands"]:
        chatCmd = requestedCmd
        output = commands["commands"][chatCmd]['output']

        print(f"{chatMsg[0]} sent {chatCmd}")
        msg = commands['commands'][requestedCmd]['output']

        print(msg)

        sendMsg(msg)
    else:
        print(f"Invalid command received")

def running():
    try:
        while True:
            resp = server.recv(2048).decode('utf-8')

            if resp != "":
                chatMsg = parseMsg(resp)
                if chatMsg != None and chatMsg[1][0] == prefix:
                    readCommand(chatMsg)

    # Catch all exceptions, if you constantly connect and disconnect Twitch thinks your DDoSing them.
    except Exception as e:
        print("An unexpected error occurred.")
        print("Error:")
        print(e)
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
    global server
    server = init()
    running()
    server.close()

if __name__ == "__main__":
    main()