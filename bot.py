#!/usr/bin/env python3
import socket
import json
import irc

def init():
    global prefix

    with open("files/secrets.json", "r") as filp:
        secrets = json.load(filp)

    print("Opened secrets")
    print(secrets)

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

def readCommand(chatMsg):
    with open('files/commands.json', 'r') as filp:
        commands = json.load(filp)

    if "\n" in chatMsg[1]:
        print("newline detected")

    if chatMsg[1][1:-1] in commands["commands"]:
        print(f"{chatMsg[0]} sent {chatMsg[1][1:-1]}")
    else:
        print(f"Invalid command received")
        print(f"Received {chatMsg[1][1:-1]}, available commands are {commands['commands']}")

def running(server):
    while True:
        resp = server.recv(2048).decode('utf-8')

        if resp != "":
            chatMsg = parseMsg(resp)
            if chatMsg[1][0] == prefix:
                readCommand(chatMsg)
    

def main():
    server = init()
    running(server)

if __name__ == "__main__":
    main()