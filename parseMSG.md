1. Takes raw IRC message and looks for the first space
2. Substrings the start to the index of the first space
3. Sets the pointer to the index + 1
4. Confirms that the pointer is at the colon
5. Sets the ending index to the first space after the index
6. Substrings to the second space
7. Moves the pointer to the ending index + 1
	* Split the string at space
8. Sets the ending index at the first : of the initial message
9. If there is no :, set the ending index to the last character of the raw IRC message
10. Moves the ending index one over
11. Substrings at the current pointer and the ending index and removes any whitespaces from the beginning and end of the command.
	* Set to rawCommandComponent
12. If the ending index is not the length of the raw IRC message (parameters are provided), substring out the parameters
	* Set parameters to rawParametersComponent
13. Parse rawCommandComponent to parsedCommand
14. If parsedCommand is null, return null
15. If there are tags, parse the tags
