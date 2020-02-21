#!/usr/bin/env python

"""
This file contain function for scraping market data through API.

"""

import db
import yaml
import requests
import datetime
import time
from time import ctime, time, sleep


with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

URL_API = config['url-api']


def write_log(name,message) :
	with open(name, 'a') as f :
		now = ctime()
		f.writelines(now + '  -  '+ message + '\n')

def getData(market,data_type,trial_time=5):

	url = f"{URL_API}/{market}/{data_type}"
	fail = True

	for i in range(trial_time):
		response = requests.get(url=url)
		if response.status_code == 200 :
			json_data = response.json()
			fail = False
			break

	if fail :
		write_log("log/scraper.log",f"error getting {market} data, status {response.status_code}")
		return(False)
	else :
		return(json_data)


def getMarket(market):
	data_types = ['ticker', 'trades', 'depth']
	data = []
	data.append(int(time()))
	for data_type in data_types:
		dt = getData(market,data_type)
		if(dt) :
			if isinstance(dt, list) : # if data is list, convert to json obj
				old_dt = dt
				dt = {}
				for i in range(len(old_dt)) :
					dt[i] = old_dt[i]
			data.append(dt)
	if (len(data) == 4):
		return(data)
	else :
		return(False)

def run_scraper(dbname):
	markets = config['market']
	for market in markets :
		data = getMarket(market)
		db.write_to_db(market,data,dbname)
		if not market == markets[-1]: # if not last market apply delay
			sleep(config['delay-each-market'])


###############		
# run scraper #
###############



