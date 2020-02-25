#!/usr/bin/env python

import yaml
import db
import json
import numpy as np
import matplotlib.pyplot as plt
from extractor import extract_ticker,extract_trades,extract_depth, extract_actionable_price
from converter import rel_convert_ticker,rel_convert_depth, normalization, convert_ticker, convert_trades, convert_depth

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

LIMIT = config['limit']
MIN_AMOUNT = config['min-actionable-amount']

####################
### RUN THE DATA ###
####################

load_market_data = db.load_market_data(["ticker","trades","depth"],"btc_idr",LIMIT,"crypto.db")
ticker_raw = []
trades_raw = []
depth_raw = []
timecode = []
for load  in load_market_data :
	timecode.append(load[0])
	ticker_raw.append(extract_ticker(load[1]))
	# trades_raw.append(extract_trades(load[2]))
	depth_raw.append(extract_depth(load[3]))


act_price = extract_actionable_price(depth_raw, MIN_AMOUNT)

timecode_converted = normalization(timecode)
ticker_converted = convert_ticker(ticker_raw)
depth_converted = convert_depth(depth_raw)
trades_converted = convert_trades(trades_raw)
act_price_converted = [normalization(act_price[0]), normalization(act_price[1])]

rel_ticker = rel_convert_ticker(ticker_raw)
ticker_test = np.transpose(ticker_raw)

print(timecode)

# plt.plot(timecode_converted,ticker_converted[6], color="b")
# plt.plot(timecode_converted,act_price_converted[1], color="r")
# plt.show()
