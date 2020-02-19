import scraper
import time

iteration = 0
while True:
	iteration += 1
	scraper.runScraper()
	print(f"get data ke - {iteration}")
	time.sleep(5)



