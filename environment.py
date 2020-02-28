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
amount = amount to trade
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
NOW = int(time.time())

TR_TYPE = ['buy', 'sell']
TR_STATUS = ['process', 'done']

# create database
def init_profile(dbname):
	con = sql_connect(dbname)
	create_table(con,"balance","(id INTEGER PRIMARY KEY, timecode, idr, btc)")
	create_table(con,"trades","(id INTEGER PRIMARY KEY, trade_id, timecode, market, trans_type, price, amount, fee, status)")
	create_table(con,"history","(id INTEGER PRIMARY KEY, trade_id, timecode, opentime, closetime, openprice, closeprice, profit)")

# balance table
def init_balance(dbname,idr=1_000_000,btc=0):
	con = sql_connect(dbname)
	crs = con.cursor()
	balance = [NOW,idr,btc]
	crs.execute('INSERT INTO balance(timecode, idr, btc) VALUES (?,?,?)', balance)
	db_close(con)

def check_balance(dbname, id=1):
	con = sql_connect(dbname)
	crs = con.cursor()
	crs.execute("SELECT * FROM balance WHERE id=?",[id])
	rows = crs.fetchall()
	db_close(con)
	return rows[0]

def update_balance(dbname,col,val,id=1):
	con = sql_connect(dbname)
	crs = con.cursor()
	# query = f"UPDATE balance SET {col} = {val} WHERE id={id}"
	crs.execute("UPDATE balance SET ?=? WHERE id=?", [col,val,id])
	# query = f"UPDATE balance SET timecode = {NOW} WHERE id={id}"
	crs.execute("UPDATE balance SET timecode=? WHERE id=?", [NOW, id])
	db_close(con)


# trades table

def trade_id(market):
	return hash(str(NOW) + market)

def buy_trade(dbname, market, price, amount):
	trd_id = trade_id(market)

	con = sql_connect(dbname)
	crs = con.cursor()
	trade = [trd_id, NOW, market, TR_TYPE[0], price, amount, TR_STATUS[0]]
	crs.execute('INSERT INTO trades(trade_id, timecode, market, trans_type, price, amount, status) VALUES (?,?,?,?,?,?,?)', trade)
	db_close(con)

	return trd_id

def tr_status_done(dbname, tr_type, trd_id):
	con = sql_connect(dbname)
	crs = con.cursor()
	crs.execute("UPDATE trades SET status=? WHERE trade_id=? AND trans_type=?",[TR_STATUS[1], trd_id, tr_type])
	db_close(con)

def sell_trade(dbname,trd_id, price):
	con = sql_connect(dbname)
	crs = con.cursor()

	# check if the id exist
	crs.execute('SELECT id, market, trans_type, amount, status from trades WHERE trade_id=?', [trd_id])
	fetch = crs.fetchall()
	market = fetch[0][1]
	tr_type = fetch[0][2]
	amount = fetch[0][3]
	status = fetch[0][4]
	if len(fetch) == 1 and tr_type == TR_TYPE[0] and  status == TR_STATUS[1] :
		trade = [trd_id, NOW, market, TR_TYPE[1], price, amount, TR_STATUS[0]]
		crs.execute('INSERT INTO trades(trade_id, timecode, market, trans_type, price, amount, status) VALUES (?,?,?,?,?,?,?)', trade)
	else :
		print('sell - failed!')
	db_close(con)

def trade_is_complete(dbname, trd_id):
	con = sql_connect(dbname)
	crs = con.cursor()

	crs.execute('SELECT * from trades WHERE trade_id=?', [trd_id])
	fetch = crs.fetchall()

	idx = [0,1] if (fetch[0][4] == TR_TYPE[0]) else [1,0]   # idx[0] = index buy, idx[1] = index sell
	# if len(fetch) == 2 and (fetch[idx[0]][4] + fetch[idx[1]][4]) == (TR_TYPE[0] + TR_TYPE[1]) :
	# 	opentime =
	# 	closetime =
	# 	openprice =
	# 	closeprice =
	# 	profit =



# history database




# init_profile(DBNAME)
# init_balance(DBNAME)
# update_balance(DBNAME,'btc',0.01)

# asd = buy_trade(DBNAME, 'btc_idr', '130000000', '0.0001')
# asd = buy_trade(DBNAME, 'btc_idr', '150000000', '0.0001')
# tr_status_done(DBNAME, TR_TYPE[1], -909172858584983695)
# sell_trade(DBNAME, -909172858584983695, '13000000')
# trade_is_complete(DBNAME, -909172858584983695)
