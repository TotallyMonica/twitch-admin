#!/usr/bin/env python3

def parseRawMsg(rawMsg):
    ptr = 0
    parsedMessage = {  
        "tags": None,
        "source": None,
        "command": None,
        "parameters": None
    }

    rawTags = None
    rawSource = None
    rawCommand = None
    rawParams = None

    # Check if there are any tags provided
    if rawMsg[0] == '@':
        endPointer = rawMsg.index(' ')
        rawTags = rawMsg[1:endPointer]
        ptr = endPointer + 1

    # Check for the source
    # If no source, it's a ping
    if rawMsg[ptr] == ":":
        endPointer = rawMsg.index(' ', ptr)
        rawSource = rawMsg[ptr:endPointer]
        ptr = endPointer + 1

    try:
        endPointer = rawMsg.index(":", ptr)
        rawCommand = rawMsg[ptr:endPointer].lstrip()

    except ValueError:
        ptr = len(rawMsg)

    if endPointer != len(rawMsg):
        ptr = endPointer + 1
        rawParams = rawMsg[ptr:]

    parsedMessage["command"] = parseCommand(rawCommand)

    if parsedMessage["command"] == None:
        return None
    else:
        if rawTags != None:
            parsedMessage["tags"] = parseTags(rawTags)

        parsedMessage["source"] = parseSource(rawSource)

        if rawParams != None and rawParams[0] == "!":
            parsedMessage["command"] = parseParams(rawParams, parsedMessage["command"])

    return parsedMessage

def parseTags(rawTags):
    ignoredTags = ['client-nonce', 'flags']

    dictParsedTags = {}
    splitTags = rawTags.split(';')
    for tag in splitTags:
        parsedTag = tag.split('=')
        if parsedTag[1] == None or parsedTag[1] == "":
            tagValue = None
        else:
            tagValue = parsedTag[1]

        if parsedTag[0] == "badge-info":
            if tagValue != None:
                tmpDict = {}
                badges = tagValue.split(',')

                for pair in badges:
                    badgeParts = pair.split('/')
                    tmpDict[badgeParts[0]] = badgeParts[1]

                dictParsedTags[parsedTag[0]] = tmpDict
            else:
                dictParsedTags[parsedTag[0]] = None

        elif parsedTag[0] == "emotes":
            if tagValue != None:
                dictEmotes = {}
                emotes = tagValue.split('/')

                for emote in emotes:
                    emoteParts = emote.split(':')
                    textPositions = []
                    positions = emoteParts[1].split(',')

                    for position in positions:
                        positionParts = position.split('-')

                        textPosition = {
                            'startPosition': positionParts[0],
                            'endPosition': positionParts[1]
                        }

                    dictEmotes[emoteParts[0]] = textPositions

                dictParsedTags[parsedTag[0]] = dictEmotes

        elif parsedTag[0] == "emote-sets":
            emoteSetIds = tagValue.split(',')
            dictParsedTags[parsedTag[0]] = emoteSetIds

        elif parsedTag[0] == "badges":
            if tagValue != None:
                dictBadges = {"badges": []}
                badges = tagValue.split(',')

                for badge in badges:
                    textPositions = []
                    positions = badge.split('/')
                    textPosition = {
                        'name': positions[0],
                        'length': positions[1]
                    }

                    dictBadges["badges"].append(textPosition)

                dictParsedTags.update(dictBadges)

    return dictParsedTags

def parseCommand(rawCmd):
    cmdParts = rawCmd.split(' ')
    parsedCmd = None

    if cmdParts[0] == "PRIVMSG":
        parsedCmd = {
            "command": cmdParts[0],
            "channel": cmdParts[1]
        }

    elif cmdParts[0] == "PING":
        parsedCmd = {
            "command": cmdParts[0]
        }

    elif cmdParts[0] == "CAP":
        parsedCmd = {
            "command": cmdParts[0],
            "isCapRequestEnabled": cmdParts[2] == 'ACK'
        }

    elif cmdParts[0] == "GLOBALUSERSTATE":
        parsedCmd = {
            "command": cmdParts[0] 
        }

    elif cmdParts[0] == "ROOMSTATE":
        parsedCmd = {
        "command": cmdParts[0],
        "channel": cmdParts[1]
        }

    elif cmdParts[0] == "RECONNECT":
        print("The IRC server is going down momentarily.")
        parsedCmd = {
            "command": cmdParts[0]
        }

    elif cmdParts[0] == "421":
        print("Unsupported IRC command")

    elif cmdParts[0] == "001":
        parsedCmd = {
            "command": cmdParts[0], 
            "channel": cmdParts[1]
        }

    elif cmdParts[0] == "376": 
        print(int(cmdParts[0]))

    elif cmdParts[0] == "JOIN" or cmdParts[0] == "PART" or cmdParts[0] == "NOTICE" or cmdParts[0] == "CLEARCHAT" or cmdParts[0] == "HOSTTARGET" or cmdParts[0] == "USERSTATE" or cmdParts[0] == "002" or cmdParts[0] == "003" or cmdParts[0] == "004" or cmdParts[0] == "353"   or cmdParts[0] == "366" or cmdParts[0] == "372" or cmdParts[0] == "375":
        print(f"No need to respond to {cmdParts[0]}")

    else:
        print(f"Unexpected command: {cmdParts[0]}")

    return parsedCmd

def parseSource(rawSrc):
    if rawSrc == None or rawSrc == "":
        return None
    else:
        srcParts = rawSrc.split('!')
        if len(srcParts) == 2:
            output = {
                "nick": srcParts[0],
                "host": srcParts[1]
            }
        else:
            output = {
                "nick": None,
                "host": srcParts[0]
            }

        return output

def parseParams(rawParams, cmd):
    ptr = 0
    cmdParts = rawParams[ptr + 1:].lstrip()
    try:
        paramsPtr = cmdParts.index(' ')
        cmd.update({"botCommand": cmd[0:paramsPtr].lstrip(), "botCommandParams": cmd[paramsPtr:].lstrip()})
    except ValueError:
        cmd.update({"botCommand": cmdParts[0:].lstrip()})

    return(cmd)