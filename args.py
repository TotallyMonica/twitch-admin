#!/usr/bin/env python3
# The only reason why this exists is because I hate argparse

import json

def parseArgs(args):
	with open('args.json', 'r') as filp:
		argsDB = json.load(filp)

	for arg in argsDB:
		if arg['short'] in args or arg['long']:
			return arg