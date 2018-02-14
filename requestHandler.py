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
    json_data = json.loads(responseJSON.text)
    fightInformation = getFightDetails(json_data)
    CharID = None
    for names in json_data['friendlies']:
        if name == names['name']:
            CharID = names['id']
            break
    if CharID:
        continueAnalysis(api_key, secret_key, wcl, CharID, name, fightInformation[0][1], fightInformation[0][2], fightInformation[0][3], 0)
    else:
        print("No Character with that name found within the Logs, Try Again")

#Character Found, Analysis of Logs Commences
def continueAnalysis(api_key, secret_key, wcl, CharID, CharName, startTime, endTime, bossPercentage, fightNo):
    print("Continuing Analysis...")
    url = 'https://www.warcraftlogs.com:443/v1/report/events/NLKn6xgdWJ9b1FY8?start=' + str(startTime) + '&end=' + str(endTime) + '&api_key=' + api_key
    responseJSON = wcl.get(url)
    json_data = json.loads(responseJSON.text)
    for data in json_data['events']:
        try:
            if CharID == data['sourceID']:
                print("Type: %s, ID: %s" % (data['type'], data['sourceID']))
        except KeyError:
            print("no Source Key - Skipped")
    try:
        if json_data['nextPageTimestamp']:
            continueAnalysis(api_key, secret_key, wcl, CharID, CharName, int(json_data['nextPageTimestamp']), endTime, bossPercentage, fightNo)
    except KeyError:
            print("End of Fight")
        
#Get Fight Start and End Times and Other Information
def getFightDetails(json_data):
    fightList = []
    for fights in json_data['fights']:
        fightInfo = []
        fightInfo.append(fights['id'])
        fightInfo.append(fights['start_time'])
        fightInfo.append(fights['end_time'])
        fightInfo.append(fights['bossPercentage'])
        fightList.append(fightInfo)
    return fightList
            
keys = getKeys()
initialRequest(keys[0], keys[1])