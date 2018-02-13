#Requests Library for OAuth
import requests
from requests_oauthlib import OAuth1
from requests_oauthlib import OAuth1Session

#ConfigParser for reading config file
import configparser

#Get Keys
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['KEYS']['wcl_public_key']
secret_key = config['KEYS']['wcl_private_key']


#URL and Authentication/Request
wcl = OAuth1Session(api_key, client_secret=secret_key)
url = 'https://www.warcraftlogs.com:443/v1/report/fights/NLKn6xgdWJ9b1FY8?api_key=' + api_key
r = wcl.get(url)
#print(r.json())

#print(r.json()), r.text, r.encoding, r.headers['content-type'], r.status_code
