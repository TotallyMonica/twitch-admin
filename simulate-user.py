#!/usr/bin/env python3

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

# Simulate a message here
ircOutput = '@badge-info=subscriber/16;badges=subscriber/12,broadcaster/1,glhf-pledge/1;client-nonce=aebf822fae5243bcbb938c6f85bad73c;color=#8A2BE2;display-name=MajorYoshi;emotes=305663024:46-55/305505101:3-14/305505090:16-25/300511961:27-35/300148455:37-44;first-msg=0;flags=;id=bae98156-0580-4209-829a-b3324abebed9;mod=0;returning-chatter=0;room-id=87867790;subscriber=0;tmi-sent-ts=1663553847734;turbo=0;user-id=87867790;user-type= :majoryoshi!majoryoshi@majoryoshi.tmi.twitch.tv PRIVMSG #majoryoshi :hi'

# Split that simulated message to be parsed, then print output
splitIrc = ircOutput.split(':')

print(ircOutput)
print("\n\n\n\n")

ptr = 0

rawTags = None;
rawSource = None; 
rawCommand = None;
rawParams = None;

# Check if there are any tags provided
if ircOutput[0] == '@':
	endPointer = ircOutput.index(' ')
	rawTags = ircOutput[1:endPointer]
	ptr = endPointer + 1

# Check for the source
# If no source, it's a ping
if ircOutput[ptr] == ":":
	endPointer = ircOutput.index(' ', ptr)
	rawSource = ircOutput[ptr:endPointer]
	ptr = endPointer + 1

try:
	endPointer = ircOutput.index(":", ptr)
	rawCommand = ircOutput[ptr:endPointer].lstrip()

except ValueError:
	ptr = len(ircOutput)

if endPointer != len(ircOutput):
	ptr = endPointer + 1
	rawParams = ircOutput[ptr:]

print("Raw tags: " + rawTags + "\n")
print("Raw source: " + rawSource + "\n")
print("Raw tags: " + rawCommand + "\n")
print("Raw params: " + rawParams)
print("\nParsed tags:", parseTags(rawTags))

