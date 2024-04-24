#!/usr/bin/env python3

import json

# instantiate an empty dict
wallet = {}

# add a team member
wallet['aashiq'] = {'balance': 100}

with open('wallet.json', 'w') as f:
    json.dump(wallet, f)