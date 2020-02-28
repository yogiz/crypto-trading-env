#!/usr/bin/env python

"""
This file contain function needed to connect with database.

"""

import sqlite3
from sqlite3 import Error
from time import ctime
import json

def sql_connect(dbname="crypto.db"):
    try:
        con = sqlite3.connect(dbname)
        return con
    except Error:
        print(Error)

def db_close(con):
    con.commit()
    con.close()


def create_table(con, table_name, cols):
    crs = con.cursor()
    crs.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='"+ table_name+ "'")
    exist = int(crs.fetchone()[0])
    # print(table_name + ' = ' + str(exist))
    if(exist == 0) :
        crs.execute("CREATE TABLE " + table_name + cols )
        con.commit()
        crs.close()
    # else :
    #     print('Database exist!')

def write_market_todb(market, data, dbname):
    con = sql_connect(dbname)
    cols = '(timecode,ticker,trades,depth)'
    create_table(con, market, cols)
    try :
        crs = con.cursor()
        crs.execute('INSERT INTO '+ market +'(timecode,ticker,trades,depth) VALUES (?,?,?,?)', [data[0],json.dumps(data[1]),json.dumps(data[2]),json.dumps(data[3])])
        con.commit()
        crs.close()
    except sqlite3.Error as error:
        with open('log/db.log', 'a') as f:
            now = ctime()
            f.writelines( now + " - Fail to insert in database, err: " +  str(error) + "\n")
    finally:
        if (con):
            con.close()


# def write_market_todb(market,data):
#     con = sql_connect()
#     insert_data(market,data)



def load_market_data(cols,market,limit,dbname,order='DESC') :
    rows = [];
    arg_col = 'timecode'
    for col in cols :
        arg_col += f',{col}'

    query = f'SELECT * FROM (SELECT {arg_col} FROM {market} ORDER BY timecode {order} LIMIT {limit})ORDER BY timecode ASC;'
    
    con = sql_connect(dbname)
    try :
        crs = con.cursor()
        crs.execute(query)
        rows = crs.fetchall()
        con.commit()
        crs.close()
    except sqlite3.Error as error:
        with open('log/db.log', 'a') as f:
            now = ctime()
            f.writelines( now + " - Fail to load data, err: " +  str(error) + "\n")
    finally:
        if (con):
            con.close()
    return rows