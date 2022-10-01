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

#    print("\nRaw values:")
#    print(f"\tTags: {rawTags}")
#    print(f"\tSource: {rawSource}")
#    print(f"\tCommand: {rawCommand}")
#    print(f"\tParams: {rawParams} \n")

    if rawCommand == None:
        return None
    
    else:
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
    # Split rawCmd at every space, set the output to cmdParts
    cmdParts = rawCmd.split(' ')
    parsedCmd = None

    # If the IRC command was PRIVMSG, return the command and the channel from cmdParts
    if cmdParts[0] == "PRIVMSG":
        parsedCmd = {
            "command": cmdParts[0],
            "channel": cmdParts[1]
        }

    # If the IRC command was PING, return the ping.
    elif cmdParts[0] == "PING":
        parsedCmd = {
            "command": cmdParts[0]
        }

    # If the IRC command was CAP, return the command and if cmdParts[2] is an ACK
    elif cmdParts[0] == "CAP":
        parsedCmd = {
            "command": cmdParts[0],
            "isCapRequestEnabled": cmdParts[2] == 'ACK'
        }

    # If the IRC command was GLOBALUSERSTATE, return the command
    elif cmdParts[0] == "GLOBALUSERSTATE":
        parsedCmd = {
            "command": cmdParts[0] 
        }

    # If the IRC command was ROOMSTATE, return the command and the channel from cmdParts
    elif cmdParts[0] == "ROOMSTATE":
        parsedCmd = {
        "command": cmdParts[0],
        "channel": cmdParts[1]
        }

    # If the IRC command was RECONNECT, print a warning to the output and return the command
    elif cmdParts[0] == "RECONNECT":
        print("The IRC server is going down momentarily.")
        parsedCmd = {
            "command": cmdParts[0]
        }

    # If the IRC command was 421, print a heads up of the unsupported command
    elif cmdParts[0] == "421":
        print("Unsupported IRC command")

    # If the IRC command was 001, return the command and the channel from cmdParts
    elif cmdParts[0] == "001":
        parsedCmd = {
            "command": cmdParts[0], 
            "channel": cmdParts[1]
        }

    # If the IRC command was 376, print the int value of the command
    elif cmdParts[0] == "376": 
        print(int(cmdParts[0]))

    # If the command is any of the following, don't bother responding
    # JOIN, PART, NOTICE, CLEARCHAT, HOSTTARGET, USERSTATE, 002, 003, 004, 353, 366, 372, 375
    elif cmdParts[0] == "JOIN" or cmdParts[0] == "PART" or cmdParts[0] == "NOTICE" or cmdParts[0] == "CLEARCHAT" \
     or cmdParts[0] == "HOSTTARGET" or cmdParts[0] == "USERSTATE" or cmdParts[0] == "002" or cmdParts[0] == "003" or cmdParts[0] == "004" \
     or cmdParts[0] == "353"   or cmdParts[0] == "366" or cmdParts[0] == "372" or cmdParts[0] == "375":
        print(f"No need to respond to {cmdParts[0]}")

    # It didn't meet any of the other requirements, so print a notice and the command.
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
#    print("\nparseParams()")
    ptr = 0
    if "\n" or "\b" in rawParams:
        rawParams = rawParams[0:-2]

    cmdParts = rawParams[(ptr + 1):].lstrip()

    try:
        paramsPtr = cmdParts.index(' ')
        cmd.update({
            "botCommand": cmdParts[0:paramsPtr],
            "botCommandParams": cmdParts[paramsPtr:].lstrip(),
            "isCommand": rawParams[0] == '!'
            })
    except ValueError:
        cmd.update({
            "botCommand": cmdParts[0:],
            "isCommand": rawParams[0] == '!'
            })

    return(cmd)
