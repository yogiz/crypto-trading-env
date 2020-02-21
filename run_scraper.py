#!/usr/bin/env python

import scraper
import time

iteration = 0
while True:
	iteration += 1
	scraper.run_scraper("crypto.db")
	print(f"get data ke - {iteration}")
	time.sleep(60)
