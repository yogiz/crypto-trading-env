#!/usr/bin/env python

import yaml
import db
import json
import numpy as np
import matplotlib.pyplot as plt
from extractor import extract_ticker,extract_trades,extract_depth
from converter import rel_convert_ticker,rel_convert_depth, normalization, convert_ticker, convert_trades, convert_depth

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

LIMIT = config['limit']

####################
### RUN THE DATA ###
####################

load_data = db.load_data(["ticker","trades","depth"],"btc_idr",LIMIT,"crypto.db")
ticker_raw = []
trades_raw = []
depth_raw = []
timecode = []
for load  in load_data :
	timecode.append(load[0])
	# ticker_raw.append(extract_ticker(load[1]))
	# trades_raw.append(extract_trades(load[2]))
	depth_raw.append(extract_depth(load[3]))

timecode_converted = normalization(timecode)
# ticker_converted = convert_ticker(ticker_raw)
depth_converted = convert_depth(depth_raw)
# trades_converted = convert_trades(trades_raw)


rel_ticker = rel_convert_ticker(ticker_raw)
print(depth_converted)

# plt.plot(timecode_converted,ticker_converted[6], color="b")
# plt.plot(timecode_converted,rel_ticker[6], color="r")

