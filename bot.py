#!/usr/bin/env python3
import socket
import json
import irc

with open("files/secrets.json", "r") as file:
    secrets = json.load(file)

    server = 'irc.chat.twitch.tv'
    port = 6667
    nickname = 'majoryoshibot'
    token = secrets["oauth"]
    # channel = '#majoryoshi'
    print("What twich channel would you like to join?")
    channel = input()

    if channel[0] != "#"
        channel = "#" + channel

    readbuffer= ""

    sock = socket.socket()
    sock.connect((server, port))
    print("connected")

    sock.send(f'PASS {token}\n'.encode('utf-8'))
    print("logged in")

    sock.send(f'NICK {nickname}\n'.encode('utf-8'))
    print(f"Nickname set to {nickname}")

    sock.send(f'JOIN {channel}\n'.encode('utf-8'))
    print(f"Joined channel {channel}")

    while True:
        resp = sock.recv(2048).decode('utf-8')
        print(resp)