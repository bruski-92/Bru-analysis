#Requests Library for OAuth and JSON parsing
import requests
import json
from requests_oauthlib import OAuth1
from requests_oauthlib import OAuth1Session

#ConfigParser for reading config file
import configparser

#CSV to dump data to CSV File
import csv

#Get Keys
def getKeys():
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config['KEYS']['wcl_public_key']
    secret_key = config['KEYS']['wcl_private_key']
    return api_key, secret_key

#URL and Authentication/Request
#Request Character Name and Reject if not found
def initialRequest(api_key, secret_key):
    name = raw_input("Please enter your Characters Name:")
    wcl = OAuth1Session(api_key, client_secret=secret_key)
    url = 'https://www.warcraftlogs.com:443/v1/report/fights/NLKn6xgdWJ9b1FY8?api_key=' + api_key
    responseJSON = wcl.get(url)
    #print(responseJSON.json())
    #print(r.json()), r.text, r.encoding, r.headers['content-type'], r.status_code
    json_data = json.loads(responseJSON.text)
    nameFound = False
    for names in json_data['friendlies']:
        if name == names['name']:
            nameFound = True
            break
    if nameFound:
        continueAnalysis(api_key, secret_key, wcl)
    else:
        print("No Character with that name found within the Logs, Try Again")

#Character Found, Analysis of Logs Commences
def continueAnalysis(api_key, secret_key, wcl):
    print("Continuing Analysis...")
    
keys = getKeys()
initialRequest(keys[0], keys[1])