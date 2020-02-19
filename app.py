import yaml
import db
import json
import numpy as np
import matplotlib.pyplot as plt

with open('config.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    


load_data = db.load_data(["ticker"],"btc_idr",10)
ticker_raw = []
for load  in load_data :

	t_json = json.loads(load[1])
	t_json = t_json['ticker']

	tmcd = load[0]
	high = t_json['high']
	low = t_json['low']
	vol_btc = t_json['vol_btc']
	vol_idr = t_json['vol_idr']
	last = t_json['last']
	buy = t_json['buy']
	sell = t_json['sell']
	server_time = t_json['server_time']

	ticker_raw.append([tmcd,high,low,vol_btc,vol_idr,last,buy,sell,server_time])

ticker_raw = np.array(ticker_raw)
ticker_raw = np.transpose(ticker_raw) # transpose to make each row contain same data type

# convert data to get value between 0 and 1
ticker_converted = []
for line in ticker_raw :
	maxLine = line[np.argmax(line)]
	minLine = line[np.argmin(line)]
	step = float(maxLine) - float(minLine)

	curLine = []
	for item in line :
		if (step):
			convert_data = float(item) - float(minLine)
			if convert_data :
				convert_data = convert_data / step
			else :
				convert_data = 0.0
		else :
			convert_data = 0.0
		curLine.append(convert_data)
		# print(convert_data)
	ticker_converted.append(curLine)

print(ticker_converted)
