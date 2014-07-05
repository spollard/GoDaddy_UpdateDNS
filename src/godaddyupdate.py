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

def GetJson(file):
    json_date = json.load(open(file, 'r'))
    return json_date

# Create a logger
logging.basicConfig(filename='godaddy.log', format='%(asctime)s', level=logging.INFO)

# Get the User Name & Password from a JSON file then Connect to GoDaddy
GODADDY_USERNAME = GetJson('config.json')['username']
GODADDY_PASSWORD = GetJson('config.json')['password']

client = pygodaddy.GoDaddyClient()
client.login(GODADDY_USERNAME, GODADDY_PASSWORD)

# Get the Domains and DNS A Records
dns_records = GetJson('config.json')['dns-records']
domains = GetJson('config.json')['domains']

# Get the current public IP Address
public_ip = pif.get_public_ip()
logging.debug('Retrieved Public IP Address of the ISP')

# For each domain get the DNS A Records,
# Then for each DNS A Record compare it to the dns_records
# If the DNS A Record and dns_record are the same attempt to update the GoDaddy DNS A Record
# If the Public IP address and the DNS A Record IP Address are different
# Then update the DNS A Record, do nothing otherwise
for domain in domains:
    records = client.find_dns_records(domain)
    logging.debug('Checking records for Domain: {0}'.format(domain))
    
    for record in records:
        logging.debug('Checking DNS Record: {0}'.format(record))
        fqdn = "{0}.{1}".format(record.hostname, domain)
        
        for dyn_record in dns_records:
            logging.debug('Check current ip[{0}] against old ip[{1}]'.format(record.value, public_ip))
            
            if public_ip != record.value:
                logging.debug('Updating {0}.value from {1} to {2}'.format(fqdn, record.value, public_ip))
                client.update_dns_record(fqdn, public_ip)