# #!/usr/bin/env python
import random
import yaml
import db
import json
import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation

from extractor import extract_ticker,extract_trades,extract_depth
from converter import normalization, convert_ticker, convert_trades, convert_depth


LIMIT = 50
# plt.style.use('fivethirtyeight')


# def animate(i):
# 	load_market_data = db.load_market_data(["ticker","trades","depth"],"btc_idr",LIMIT,"crypto.db")
# 	ticker_raw = []
# 	for load  in load_market_data :
# 		ticker_raw.append(extract_ticker(load[0],load[1]))
# 	ticker_converted = convert_ticker(ticker_raw)
# 	plt.cla()
# 	plt.clf()
# 	plt.plot(ticker_converted[0],ticker_converted[5], color='blue')
# 	# plt.plot(ticker_converted[0],ticker_converted[], color='red')

# anim = FuncAnimation(plt.gcf(), animate, interval=6000)


# plt.tight_layout()
# plt.show()




from tkinter import *
from random import randint
 
# these two imports are important
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time
from threading import Thread


continuePlotting = False
 
def change_state():
	global continuePlotting
	if continuePlotting == True:
	    continuePlotting = False
	else:
	    continuePlotting = True
    
 
def data_points():
	load_market_data = db.load_market_data(["ticker"],"btc_idr",LIMIT,"crypto.db")
	ticker_raw = []
	for load  in load_market_data :
		ticker_raw.append(extract_ticker(load[0],load[1]))
	ticker_converted = convert_ticker(ticker_raw)

	# plt.plot(ticker_converted[0],ticker_converted[5], color='blue')
	# plt.plot(ticker_converted[0],ticker_converted[], color='red')

	return ticker_converted




def app():
	# initialise a window.
	root = Tk()
	root.config(background='white')
	root.geometry("700x700")

	lab = Label(root, text="Live Plotting", bg = 'white').pack()
	fig = Figure()

	ax = fig.add_subplot(111)
	ax.set_xlabel("X axis")
	ax.set_ylabel("Y axis")
	ax.grid()

	def DrawGraph():
		while True:
			ax.cla()
			ax.grid()
			dpts = data_points()
			ax.plot(dpts[0], dpts[5], marker='o', color='orange')
			graph.draw()
			time.sleep(10)

	graph = FigureCanvasTkAgg(fig, master=root)
	graph.get_tk_widget().pack(side="top",fill='both',expand=True)

	t1 = Thread(target=DrawGraph)
	t1.setDaemon(True)
	t1.start()

	# Refresher()
	root.mainloop()
 
if __name__ == '__main__':
    app()