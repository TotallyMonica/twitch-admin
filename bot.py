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
    channel = '#majoryoshibot'
    readbuffer= ""

    sock = socket.socket()
    sock.connect((server, port))
    print("connected")

    sock.send(f'PASS {token}\n'.encode('utf-8'))
    print("logged in")

    sock.send(f'NICK {nickname}\n'.encode('utf-8'))
    print("Nickname set")

    sock.send(f'JOIN {channel}\n'.encode('utf-8'))
    print("Joined channel")

    resp = sock.recv(2048).decode('utf-8')
    resp

    sock.close