#!/usr/bin/env python
"""
This is environmental part. All trades transaction function are defined here.


- check balance
- trade history
- trade (buy, sell)
- get Order info
- cancel order


"""

from db import sql_connect, create_table
import time

DBNAME = "profile.db"
NOW = int(time.time())

def init_profile(dbname):
	con = sql_connect(dbname)
	create_table(con,"balance","(id INTEGER PRIMARY KEY, timecode, idr, btc)")
	create_table(con,"trades","(id INTEGER PRIMARY KEY,timecode, market, type, price, amount, status)")
	create_table(con,"history","(id INTEGER PRIMARY KEY,timecode, opentime, closetime, closeprice, status)")

def init_balance(dbname,idr=1_000_000,btc=0):
	con = sql_connect(dbname)
	crs = con.cursor()
	balance = [NOW,idr,btc]
	crs.execute('INSERT INTO balance(timecode, idr, btc) VALUES (?,?,?)', balance)
	con.commit()
	crs.close()

def check_balance(dbname, id=1):
	con = sql_connect(dbname)
	crs = con.cursor()
	crs.execute(f"SELECT * FROM balance WHERE id={id}")
	rows = crs.fetchall()
	con.commit()
	crs.close()
	return rows[0]

def update_balance(dbname,col,val,id=1):
	con = sql_connect(dbname)
	crs = con.cursor()
	query = f"UPDATE balance SET {col} = {val} WHERE id={id}"
	crs.execute(query)
	query = f"UPDATE balance SET timecode = {NOW} WHERE id={id}"
	crs.execute(query)
	con.commit()
	crs.close()



# init_profile(DBNAME)
# init_balance(DBNAME)
# update_balance(DBNAME,'btc',0.01)