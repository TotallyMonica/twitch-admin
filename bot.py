#!/usr/bin/env python3
import socket
import json
import irc

def init():
    secrets = json.load(open("files/secrets.json", "r"))

    server = 'irc.chat.twitch.tv'
    port = 6667
    nickname = 'majoryoshibot'
    token = secrets["oauth"]
    channel = '#' + secrets['channel']

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

def running(server):
    commands = json.load(open("files/commands.json"), "r")
    

def main():
    server = init()