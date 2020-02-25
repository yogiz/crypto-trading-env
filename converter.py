import numpy as np

def normalization(row, maxVal=0, minVal=0) :
	if not maxVal:
		maxVal = float(row[np.argmax(row)])
	if not minVal:
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


''' 
second convert strategy, 
take precentation representation of that data from all column that
having same value type. Forexample, buy price and sell price that two column basically having same type of value.
'''

def get_rel_max_min(list_arr):
	arr = np.concatenate(list_arr,axis=None)
	ar_max = arr[np.argmax(arr)]
	ar_min = arr[np.argmin(arr)]
	return  (float(ar_max), float(ar_min))

def rel_normalization(list_arr):  # normalization list of array that have relation value
	max_val, min_val = get_rel_max_min(list_arr)
	new_arr = []
	for item in list_arr:	
		new_arr.append(normalization(item,max_val, min_val))
	return new_arr

def get_and_compare_max_min(old_max_min, arr):
	new_max = arr[np.argmax(arr)]
	new_min = arr[np.argmin(arr)]
	new_max = float(new_max)
	new_min = float(new_min)
	if old_max_min :
		if old_max_min[0] > new_max :  # if old max bigger than new max, no need update the max val
			new_max = old_max_min[0]
		if old_max_min[1] < new_min :  # if old min smaller than new min, no need update the min val
			new_min = old_max_min[1]

	return [new_max, new_min]

def rel_convert_ticker(ticker_raw): # [high,low,vol_btc,vol_idr,last,buy,sell,server_time]

	ticker_raw = np.array(ticker_raw)
	ticker_raw = np.transpose(ticker_raw) 

	# normalize price val = high,low,last,buy,sell
	list_array = (ticker_raw[0], ticker_raw[1],ticker_raw[4], ticker_raw[5], ticker_raw[6])
	new_arr = rel_normalization(list_array)

	# normalize vol btc, vol idr, server time
	v_btc = normalization(ticker_raw[2])
	v_idr = normalization(ticker_raw[3])
	s_time = normalization(ticker_raw[7])

	return [new_arr[0],new_arr[1],v_btc, v_idr, new_arr[2],new_arr[3],new_arr[4],s_time]

def rel_convert_depth(depth_raw): # curently still error
	'''
	depth_raw(i) ___ BUY __ price (150 row)
			  	|		|__ amount (150 row)
		||		|
		||		|__  SELL__ price (150 row)
		||		 		|__ amount (150 row)
	   ****
	    **

	  (LIMIT)
	'''
	# find general max and min in depth data
	price_max_min = []
	amount_max_min = []
	for depth in depth_raw:
		for buysell in depth:
			price_max_min = get_and_compare_max_min(price_max_min, buysell[0])
			amount_max_min = get_and_compare_max_min(amount_max_min, buysell[1])
			

	new_depth = []
	for depth in depth_raw:
		new_buysell = []
		for buysell in depth:
			new_price=[]
			new_amount=[]
			for price in buysell[0]:
				print(normalization(price,price_max_min[0], price_max_min[1]))
				new_price.append(normalization(price,price_max_min[0], price_max_min[1]))
			for amount in buysell[1]:
				new_amount.append(normalization(amount,amount_max_min[0], amount_max_min[1]))
			new_buysell.append([new_price, new_amount])
		
		new_depth.append(new_buysell)

	print(new_depth)