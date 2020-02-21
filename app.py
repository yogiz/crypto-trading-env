#!/usr/bin/env python

import yaml
import db
import json
import numpy as np
import matplotlib.pyplot as plt
from extractor import extract_ticker,extract_trades,extract_depth

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

LIMIT = config['limit']


def normalization(row) :
	maxVal = float(row[np.argmax(row)])
	minVal = float(row[np.argmin(row)])
	step = maxVal - minVal
	result = []
	for rw in row :
		if(step) :
			distance = float(rw) - minVal
			if(distance):
				result.append(distance / step)
			else:
				result.append(0.0)
		else :
			result.append(0.0)
	return result

def convert_ticker(ticker_raw): 
	ticker_raw = np.array(ticker_raw)
	ticker_raw = np.transpose(ticker_raw) # transpose to make each row contain same data type

	ticker_converted = []
	for row in ticker_raw :
		row = normalization(row)
		ticker_converted.append(row)

	return ticker_converted

def convert_trades(trades_raw) :
	trades = []
	for trade in trades_raw :
		cols = []
		for col in trade :
			cols.append(normalization(col))
		trades.append(cols)
			
	return trades

def convert_depth(depth_raw) :
	depth = []
	for dp in depth_raw :
		cols = []
		for col in dp :
			rows = []
			for row in col:
				rows.append(normalization(row))
			cols.append(rows)
		depth.append(cols)
	return depth
####################
### RUN THE DATA ###
####################

load_data = db.load_data(["ticker","trades","depth"],"btc_idr",LIMIT,"crypto.db")
ticker_raw = []
trades_raw = []
depth_raw = []
for load  in load_data :
	ticker_raw.append(extract_ticker(load[0],load[1]))
	trades_raw.append(extract_trades(load[0],load[2]))
	depth_raw.append(extract_depth(load[0],load[3]))

ticker_converted = convert_ticker(ticker_raw)
depth_converted = convert_depth(depth_raw)
trades_converted = convert_trades(trades_raw)





for depth in depth_converted : # in every each time
	transaction = depth[0]
	plt.plot(transaction[0],transaction[1])
	# for transaction in depth : # 2 - buy or sell
		# plt.plot(transaction[0],transaction[1])
		# for dt_type in transaction : # 2 - price or amount, each contain 150
		# 	print(len(dt_type))

plt.show()