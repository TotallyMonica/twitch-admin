#!/usr/bin/env python3
import sys
import os
from time import sleep

# Static variables for time conversion
global MINUTES
global HOURS
global DAYS

MINUTES = 60
HOURS = 3600
DAYS = 86400
WEEKS = DAYS * 7

def timer(time, finish="", file=True):
    # Clear out file
    if file:
        with open('timer.txt', 'w') as filp:
            filp.write("")
    
    # Determine how many different positions there are
    positions = time.count(':')

    # Split on : (if available) and put them into the relevant positions
    if positions == 4:
        splitTime = time.split(':')
    elif positions == 3:
        splitTime = [None] + time.split(':')
    elif positions == 2:
        splitTime = [None, None] + time.split(':')
    elif positions == 1:
        splitTime = [None, None, None] + time.split(':')
    elif positions == 0:
        splitTime = [None, None, None, None, time]
    
    # Convert all integers that are currently strings to integers
    for i in range(len(splitTime)):
        if splitTime[i] and splitTime.isdigit():
            splitTime[i] = int(splitTime[i])

    # Convert all the times to seconds
    seconds = 0
    for i in range(len(splitTime)):
        if not splitTime[i]:
            continue
        elif i == 0:
            seconds = seconds + (splitTime[i] * WEEKS)
        elif i == 1:
            seconds = seconds + (splitTime[i] * DAYS)
        elif i == 2:
            seconds = seconds + (splitTime[i] * HOURS)
        elif i == 3:
            seconds = seconds + (splitTime[i] * MINUTES)
        elif i == 4:
            seconds = seconds + splitTime[i]
    
    # Make a duplicate of the seconds variable to subtract over
    # Only reason a duplicate is used to maintain the number of positions used
    manipSeconds = seconds

    # Loop while there's still time remaining
    while manipSeconds > 0:
        friendlyTime = ""

        # Create the friendly string
        if int(seconds / WEEKS) > 0:
            friendlyTime = f'{manipSeconds / WEEKS}:'
        if int(seconds / DAYS) > 0:
            friendlyTime = friendlyTime + f'{manipSeconds / DAYS}:'
        if int(seconds / HOURS) > 0:
            friendlyTime = friendlyTime + f"{int(manipSeconds / HOURS):02}:"
        if int(seconds / MINUTES) > 0:
            friendlyTime = friendlyTime + f"{int(manipSeconds / MINUTES):02}:"
        friendlyTime = friendlyTime + f"{int(manipSeconds % MINUTES):02}"

        # Print the friendly string and write to file
        print(friendlyTime)
        if file:
            with open('timer.txt', 'w') as filp:
                filp.write(friendlyTime)
        
        # Subtract 1 from manipSeconds, and wait a second
        manipSeconds = manipSeconds - 1
        sleep(1)
    
    # Return the finish string
    return finish

def main():
    countdown = '5'
    print(timer(countdown))

if __name__ == '__main__':
    main()