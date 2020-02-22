#!/usr/bin/env python

import scraper
import time
from itertools import count

iteration = count()
while True:
	scraper.run_scraper("crypto.db")
	print(f"get data ke - {next(iteration)}")
	time.sleep(10)
