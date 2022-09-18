#!/usr/bin/env python3

# Simulate a message here
username = "chatter123"
stream = "majoryoshi"
message = "toby fox: imma do what people call a pro gamer move"
ircOutput = ":" + username + "!" + username + "@" + username + ".tmi.twitch.tv PRIVMSG #" + stream + ":" + message

# Split that simulated message to be parsed, then print output
splitIrc = ircOutput.split(':')

print(ircOutput)
print(splitIrc)
print(len(splitIrc))

print()
print()
print()
print()
print()

# Identify the sender
sender = ""
for char in splitIrc[1]:
	if char == ':':
		continue
	elif char == '!':
		break
	else:
		sender = sender + char

# Check to make sure the split irc output is exactly a length of 3
# If it isn't it's likely the sender used a : in their message
chatMsg = ""

if len(splitIrc) == 3:
	chatMsg == splitIrc[2]
elif len(splitIrc) > 3:
	for part in splitIrc:
		if not part == splitIrc[0] and not part == splitIrc[1]:
			chatMsg = chatMsg + part

# Print the identified chatter and the message
print(f"Chatter identified: {sender}")
print(f"Their message: {chatMsg}")