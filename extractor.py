#!/usr/bin/env python
"""
This file is contain function to extract json data from database and convert to array.
Also we transpose the array, so each row have same data type.

"""


import json
import numpy as np

def extract_ticker(tiker_data): 
	t_json = json.loads(tiker_data)
	t_json = t_json['ticker']

	high = t_json['high']
	low = t_json['low']
	vol_btc = t_json['vol_btc']
	vol_idr = t_json['vol_idr']
	last = t_json['last']
	buy = t_json['buy']
	sell = t_json['sell']
	server_time = t_json['server_time']


	return   [high,low,vol_btc,vol_idr,last,buy,sell,server_time] # [high,low,vol_btc,vol_idr,last,buy,sell,server_time]

def extract_depth(depth_data): 
	d_json = json.loads(depth_data)
	d_buy = d_json['buy']
	d_sell = d_json['sell']
	buy =  np.transpose(d_json['buy'])
	sell =  np.transpose(d_json['sell'])

	return [buy, sell]   # [ [buy (price, amount)]  --  [sell (price, amount)] ] 


def extract_trades(trades_data): 
	td_json = json.loads(trades_data)
	trades = []
	for i in range(len(td_json)) :
		trade = td_json[str(i)]
		if (trade['type'] == 'buy') :
			trade_type = 1
		else :
			trade_type = 0
		trades.append([ 
			trade['date'],
			trade['price'],
			trade['amount'],
			trade_type])

	trades = np.transpose(trades)
	return trades  # [ [date], [price], [amount], [type (1 = buy, 0 = sell)] ]