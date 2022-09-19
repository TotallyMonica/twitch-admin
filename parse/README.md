# Parsing the message
## Twitch's documentation was nonexistent so hopefully this provides better documentation
----------------------------------------
## Tag Extraction
1. Check if there is an @ at the beginning of the message
2. Look for the first space
3. Substring at position 1 to the index of the first space to rawTagsComponent
4. Move the pointer to the endIdx + 1.
5. Proceed to Source Extraction

## Source Extraction
1. Check if the index is at a :, then move the index by 1 if yes
	* If there is none, it's a `PING` command
2. Set the ending index to the index of the first space after the current pointer
3. Substring the current pointer to the ending index to rawSourceComponent
4. Move the current pointer to the ending index + 1
5. Continue to Command Extraction

## Command Extraction
1. Set the ending index to the first : after the current pointer
2. If there is no :, set it to the end of the message.
3. Substring the current pointer to the ending index to rawCommandComponent
4. Remove any whitespaces before and after the command
5. Continue to Parameter Extraction

## Parameters Extraction
1. Check if the ending index is the length of the message
2. If it isn't, then set the current pointer to the ending index + 1
3. Substring the current pointer to the end of the message to rawParameterComponent

## Tag Parsing
1. Set tags `client-nonce` `flags` to be ignored
2. Create empty dict dictParsedTags
3. split tags at ; to splitTags
4. For each tag,
	1. Split at = to parsedTag
	2. Set tagValue to null if parsedTag[1] == "" or parsedTag[1] otherwise
5. Switch on parsedTag[0] and follow one of the following possibilities
	1. `badge-info`:
		1. If tagValue is not null, then do the following
			1. Create an empty dict
			2. Split tagValue at , to badges
			3. For each badge as pair, do the following:
				1. Split each pair at / to badgeParts
				2. Set dict[badgeParts[0]] to badgeParts[1]
			4. Set dictParsedTags to dict
		2. If it's not, then set dictParsedTags to null
	2. `emotes`:
		1. If tagValue does not equal null,
			1. Create dictEmotes as an empty dict
			2. Split tagValue at / to emotes
			3. For each emote,
				1. Split emote at : to emoteParts
				2. Create textPositions as an empty list
				3. Split emoteParts[1] at , to positions
				4. For each position,
					1. Split position at - to positionParts
					2. Add positionParts[0] as startPosition to textPositions in JSON format
					3. Add positionParts[1] as endPosition to textPositions in JSON format
				4. Set textPositions to dictEmotes[emoteParts[0]]
			4. Set dictEmotes to dictParsedTags[parsedTag[0]]
		2. Otherwise, set dictParsedTags[pasredTag[0]] to null
	3. `emote-sets`:
		1. Split tagValue at , to emoteSetIds
		2. Set emoteSetIds to dictParsedTags[parsedTag[0]]
	4. `badges`: Do nothing
	5. `default`: set tagValue to dictParsedTags[parsedTag[0]] if it is not ignored.

## Command Parsing
1. Split the command at spaces to commandParts
2. Follow one of the following possibilities for commandParts[0]:
	1. `PRIVMSG` - Return commandParts[0] as command and commandParts[1] as channel in JSON format
	2. `PING` - Return commandParts[0] as command in JSON format
	3. `CAP` - Return commandParts[0] as command and the validity of commandParts[2] == ACK as isCapRequestEnabled in JSON format
	4. `GLOBALUSERSTATE` - Return commandParts[0] as command in JSON format
	5. `ROOMSTATE` - Return commandParts[0] as command and commandParts[1] as channel in JSON format
	6. `RECONNECT` - Print that the IRC server is going down and return commandParts[0] as command in JSON format
	7. `421` - Print an unsupported IRC command and return null
	8. `001` - Return commandParts[0] as command and commandParts[1] as channel in JSON format
	9. `376` - Print the numeric message of commandParts[0] and return null
	10. `JOIN`, `PART`, `NOTICE`, `CLEARCHAT`, `HOSTTARGET`, `USERSTATE`, `002`, `003`, `004`, `353`, `366`, `372`, `375` - Do nothing
	11. `Default`: Print an unexpected command with that value

## Source Parsing
1. If rawSourceComponent is null, return null
2. Otherwise, do the following:
	1. Split rawSourceComponent at ! to sourceParts (In this case, ! is your prefix)
	2. Return the following in JSON format:
		1. sourceParts[0] if sourceParts.length == 2, null if it's not as nick
		2. sourceParts[1] if sourceParts.length == 2, sourceParts[0] if it's not as host 

## Paramter Parsing
1. Set the current pointer to 0
2. Take the substring of the current pointer and the pointer + 1 from rawParameterComponent as commandParts and remove any whitespaces
3. Get the index of the first space and set to paramsIdx
4. If a space couldn't be found, set command['botCommand'] to commandParts.
5. Otherwise, get the substring of the current pointer and paramsIdx and set to commands['botCommands']
6. Set commands['botCommandParams'] to the substring of commandParts at paramsIdx and remove any whitespaces
7. Return the command to parsedMessage['command']