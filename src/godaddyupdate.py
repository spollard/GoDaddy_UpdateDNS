#!/usr/bin/env python

# ##
# Module: godaddyupdate.py
# Contributors: 
# RianaM - https://github.com/AngelicBrighteyes
# Description:
#     This module connects to GoDaddy through their API,
#     Gets the DNS Records that need updated from a JSON file
#     Gets the Domains for the DNS Records from a JSON file
#     finds the public IP address of the ISP that the script is running behind
#     For each Domain, grabs the current DNS A Records
#     For each DNS A Records in the domain it finds a match for the DNS Record
#     Then updates the DNS A Records ip address with the public isp ip address
# ##
import pif
import logging
import json
import pygodaddy

# Create a logger
logging.basicConfig(filename='godaddy.log', format='%(asctime)s', level=logging.INFO)

# Get the User Name & Password from a JSON file then Connect to GoDaddy
GODADDY_USERNAME = GetJson('config.json')['username']
GODADDY_PASSWORD = GetJson('config.json')['password']

client = pygodaddy.GoDaddyClient()
client.login(GODADDY_USERNAME, GODADDY_PASSWORD)

