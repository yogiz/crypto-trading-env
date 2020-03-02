#!/usr/bin/env python
"""
This is environmental part. All trades transaction function are defined here.

- check balance
- trade history
- trade (buy, sell)
- get Order info
- cancel order

----------------
| trades table |
----------------
this table is for active order and also current portofolio, if trade already done (after buy, then sell). Then the record will be deleted, and moved to history table

id = autoincrement id
trade_id = this is trade id, buy and sell record will have same trade id. So we can identify is the trade alredy done ( buy then sell).
timecode = unix timestamp
market = this is market pair (e.i btc_idr, eth_btc)
type = buy or sell
price = trade price
amount = amount to trade ( In BUY transaction AMOUNT is the amount in currency to buy with (BTC_IDR, amount = IDR amount).
						   In SELL transaction AMOUNT is the amount of the currency want to sell (BTC_IDR = BTC amount) )
status = [process, finish]

-----------------
| history table |
-----------------
The completed trade (but then sell) from trade table, will be deleted from trades table, and moved to this table.

id = autoincrement id
trade_id = this trade_id having same value with the trade table.
timecode = unix timestamp
opentime = this is basically is timecode in the buy record in trade table. (time when the coin is bought)
closetime = this is basically is timecode in the sell record in trade table. (time when the coin is sell)
openprice = this is price in the buy record in trade table.(price when the coin is bought)
closeprice = this is price in the sell record in trade table.(price when the coin is sell)

"""

from db import sql_connect, create_table, db_close
import time

DBNAME = "profile.db"
TR_TYPE = ['buy', 'sell']
TR_STATUS = ['process', 'done']
TR_STAGE = ['buy_process', 'buy_done', 'sell_process', 'sell_done']

TR_FEE = 0.003

# create database
def init_profile(con):
	create_table(con,"balance","(id INTEGER PRIMARY KEY, timecode, idr, btc)")
	create_table(con,"trades","(id INTEGER PRIMARY KEY, trade_id, timecode, market, trans_type, price, amount, fee, status)")
	create_table(con,"history","(id INTEGER PRIMARY KEY, trade_id, timecode, opentime, closetime, openprice, closeprice,openamount, closeamount, profit, percent_profit)")

# balance table
def init_balance(crs,idr=1_000_000,btc=0):
	balance = [int(time.time()),idr,btc]
	crs.execute('INSERT INTO balance(timecode, idr, btc) VALUES (?,?,?)', balance)


def check_balance(crs, id=1):
	crs.execute("SELECT * FROM balance WHERE id=?",[id])
	rows = crs.fetchall()
	return rows[0]

def update_balance(crs,col,val,id=1):
	crs.execute("UPDATE balance SET ?=? WHERE id=?", [col,val,id])
	crs.execute("UPDATE balance SET timecode=? WHERE id=?", [int(time.time()), id])

# trades table
def trade_fee(price, amount, mode = 0): # MODE = 0 is Buy transaction, 1 and other is Sell transaction
	if mode :
		return float(price) * float(amount) * TR_FEE
	else :
		return float(amount) * TR_FEE

def trade_id(market):
	return hash(str(int(time.time())) + market)

def buy_trade(crs, market, price, amount): # AMOUNT from the currency to buy with, for ex. BTC_IDR = IDR amount
	trd_id = trade_id(market)
	fee = trade_fee(price, amount)
	trade = [trd_id, int(time.time()), market, TR_TYPE[0], price, amount, fee, TR_STATUS[0]]
	crs.execute('INSERT INTO trades(trade_id, timecode, market, trans_type, price, amount, fee, status) VALUES (?,?,?,?,?,?,?,?)', trade)
	return trd_id

def tr_status_done(crs, tr_type, trd_id):
	crs.execute("UPDATE trades SET status=? WHERE trade_id=? AND trans_type=?",[TR_STATUS[1], trd_id, tr_type])


def sell_trade(crs,trd_id, sell_price):
	# check if the id exist
	crs.execute('SELECT id, market, trans_type, amount, price, status from trades WHERE trade_id=?', [trd_id])
	fetch = crs.fetchall()
	market = fetch[0][1]
	tr_type = fetch[0][2]
	idr_amount = fetch[0][3]
	buy_price = fetch[0][4]
	status = fetch[0][5]
	if len(fetch) == 1 and tr_type == TR_TYPE[0] and  status == TR_STATUS[1] :
		btc_amount = float(idr_amount) / float(buy_price)
		fee = trade_fee(sell_price, btc_amount, 1)
		trade = [trd_id, int(time.time()), market, TR_TYPE[1], sell_price, btc_amount, fee, TR_STATUS[0]]
		crs.execute('INSERT INTO trades(trade_id, timecode, market, trans_type, price, amount, fee, status) VALUES (?,?,?,?,?,?,?,?)', trade)
	else :
		print('sell - failed!')


def trade_is_complete(crs, trd_id):
	crs.execute('SELECT * from trades WHERE trade_id=?', [trd_id])
	fetch = crs.fetchall()
	if len(fetch) == 2:
		idx = [0,1] if (fetch[0][4] == TR_TYPE[0]) else [1,0]   # idx[0] = index buy, idx[1] = index sell
		buy = fetch[idx[0]]
		sell = fetch[idx[1]]
		if buy[4] == TR_TYPE[0] and sell[4] == TR_TYPE[1] and buy[8] == sell[8] == TR_STATUS[1] :
			timecode = int(time.time())
			opentime = buy[2]
			closetime = sell[2]
			openprice = buy[5]
			closeprice = sell[5]
			openamount = buy[6]
			closeamount = sell[6]
			# profit =  ((BTC amount - sell fee) * sell Price ) - (IDR amount - buy fee)
			profit = ( ( float(closeamount) * float(closeprice) ) - float(sell[7]) ) - ( float(openamount) - float(buy[7]) )
			percent_profit = (profit / float(openamount)) * 100
			return [trd_id, timecode, opentime, closetime, openprice, closeprice, openamount, closeamount, profit, percent_profit]
		else :
			return 0
	else :
		return 0

def delete_trade(crs, trd_id):
	crs.execute('DELETE FROM trades WHERE trade_id=?', [trd_id])


# history database
def create_history(crs, data):
	crs.execute("INSERT INTO history(trade_id, timecode, opentime, closetime, openprice, closeprice, openamount, closeamount, profit, percent_profit) VALUES(?,?,?,?,?,?,?,?,?,?)", data)

def check_trade(crs, trd_id):
	data = trade_is_complete(crs, trd_id)
	if data :
		print("trade complete found!")
		delete_trade(crs, trd_id)
		print("creating history!")
		create_history(crs, data)




#########
# Example
########

# db connection
con = sql_connect(DBNAME)
crs = con.cursor()

# setup db, load balance
init_profile(con)
init_balance(crs)

# buying
test_buy = buy_trade(crs, 'btc_idr', '124833800', '2000000')
tr_status_done(crs, TR_TYPE[0], test_buy)

# sell
sell_trade(crs, test_buy, '144833800')
tr_status_done(crs, TR_TYPE[1], test_buy)

# move to history table
check_trade(crs, test_buy)

# close connection
db_close(con)
