#!/usr/bin/env python3
import json
import os

def editArg(arg):
    with open('args.json', 'r') as filp:
        args = json.load(filp)

    print("Editing " + arg)
    print(f"\tShorthand: {arg['shorthand']}")
    print(f"\tLonghand: {arg['longhand']}")
    print(f"\tValue: {arg['value']}")
    print(f"\tRequired: {arg['required']}\n")

    print("What would you like to modify?")
    print("1. Name")
    print("2. Shorthand")
    print("3. Longhand")
    print("4. Value")
    print("5. Required")

    userInput = 

def editArgs():
    # Confirm arguments file exists
    if argFileExists():
        existingArgs = []
        count = 0

        # Load the arguments
        with open('args.json', 'r') as filp:
            args = json.load(filp)

        # Print current arguments and add them to a list
        print("Current arguments:")
        for arg in args:
            count += 1
            existingArgs.append(arg)
            print(f"{count}: {arg}")

        # Prompt the user for an input
        print("Choose an argument or enter 0 to exit")
        try:
            userInput = int(input())

        # Catch the user from inputting a non-integer option
        except ValueError:
            badInput()
            editArgs()

        # If the user inputs a negative number or a number larger than the number of options
        if userInput > count or userInput < 0:
            badInput("Press the number corresponding to the argument that you'd like to modify.")
            editArgs()

        else:
            editArg(existingArgs[count - 1])

    else:
        validInput = False

        # Determine if the user wants to create an args file.
        while not validInput:
            print("An arguments file does not currently exist. Would you like to create one?")
            userInput = input("(Y/n) ")

            # User says yes
            if userInput.lower() == "yes" or userInput.lower() == "y":
                createArgFile()
                validInput = True
                return(editArgs())

            # User says no
            elif userInput.lower() == "no" or userInput.lower() == "n":
                print("Exiting...")
                validInput = True
                return None

            # No valid input received
            else:
                print("Invalid input received\n")


def provide(arguments):
    parsedArgs = []
    requiredArgs = []

    if not argFileExists():
        createArgFile()

    with open('args.json', 'r') as filp:
        argDB = json.load(args.json)

    with arg in argDB:
        if arg['shorthand'] in arguments:
            parsedArgs.append(arg)
        elif arg['longhand'] in arguments:
            parsedArgs.append(arg)
        elif arg['required']:
            requiredArgs.append(arg)

    if len(requiredArgs) != 0:
        error = "Required arguments missing. Missing arguments:"
        for arg in requiredArgs:
            error = error + "\n\t" + arg

        raise ValueError(error)

def argFileExists():
    return os.path.exists('args.json')

def createArgFile():
    file = open('args.json', 'w')
    file.close()

def badInput(prompt):
    print("Invalid input received.")
    print(prompt)
    print("Press enter to continue")
    input()