# scraper.py
# author: Diego Magdaleno
# This part of the dashboard scrapes the markets for all ticker symbols
# and is after live both live data/prices and historic data. It scrapes
# every 3 seconds or so. This takes a lot from the prototype
# teststockfetch.py. Not all methods may be implemented.
# Python 3.6
# Linux


import threading
import requests
import time
import os
import sys
import platform
import csv
import random
import datetime
from bs4 import BeautifulSoup as bsoup


# Variable that stores the host OS.
opSys = None

def main():
	# Get the Host OS.
	# Windows = Windows
	# Mac = Darwin
	# Linux = Linux
	opSys = platform.system()
	print("OS: "+opSys)

	# Open the list of tickers for each market.
	cboefile = None
	nysefile = None
	nasdaqfile = None
	if opSys == "Windows":
		cboefile = open("Tickerlists\\CBOEtickerlist.txt", 'r')
		nysefile = open("Tickerlists\\NYSEtickerlist.txt", 'r')
		nasdaqfile = open("Tickerlists\\NASDAQtickerlist.txt", 'r')
	else:
		cboefile = open("/Tickerlists/CBOEtickerlist.txt", 'r')
		nysefile = open("/Tickerlists/NYSEtickerlist.txt", 'r')
		nasdaqfile = open("/Tickerlists/NASDAQtickerlist.txt", 'r')

	# Load all tickers to memory
	cboeTickers = getTickers(cboefile.readlines())
	nyseTickers = getTickers(nysefile.readlines())
	nasdaqTickers = getTickers(nasdaqfile.readlines())

	# Close the list of tickers for each market.
	cboefile.close()
	nysefile.close()
	nasdaqfile.close()

	counter = 0

	# Activate scraping.
	while True:
		# Initialize thread pools.
		#thr1 = threading.Thread(target=getCBOE, args=(cboeTickers,))
		#thr2 = threading.Thread(target=getNYSE, args=(nyseTickers,))
		thr3 = threading.Thread(target=getNASDAQ, args=(nasdaqTickers))

		# Start threads.
		#thr1.start()
		#thr2.start()
		thr3.start()

		# Wait for all threads to be executed.
		#thr1.join()
		#thr2.join()
		thr3.join()

		# Pause for a random interval between 0 to 5 seconds
		#pause = random.randint(0, 5)
		#time.sleep(5)

		sys.stdout.write("Scaped all markets "+str(counter))
		sys.stdout.flush()
		#print("Scaped all markets "+str(counter))
		counter += 1



# Extract the tickers from the txt file (first item when split by \t
# tab character). Skip first line.
# @param: fileLines, a list of all lines in the file.
# @return: returns a list of all ticker symbols in the file.
def getTickers(fileLines):
	tickerlist = []
	for line in fileLines[1:]:
		tickerlist.append(line.split("\t")[0])
	return tickerlist


# Extract market data for each ticker and save it to the appropriate
# file (CBOE).
# @param: cboeTickers, a list of all ticker symbols on the cboe.
# @return: returns nothing.
def getCBOE(cboeTickers):
	for ticker in cboeTickers:
		requestCBOE(ticker)


# Extract market data for each ticker and save it to the appropriate
# file (NYSE).
# @param: nyseTickers, a list of all ticker symbols on the nyse.
# @return: returns nothing.
def getNYSE(nyseTickers):
	for ticker in nyseTickers:
		requestNYSE(ticker)


# Extract market data for each ticker and save it to the appropriate
# file (NASDAQ).
# @param: nasdaqTickers, a list of all ticker symbols on the nasdaq.
# @return: returns nothing.
def getNASDAQ(nasdaqTickers):
	for ticker in nasdaqTickers:
		requestNASDAQ(ticker)


# Send a request to CBOE and parse the data to the appropriate file.
# @param: ticker, the string that is the ticker symbol for the company
#	in that market.
# @return: returns nothing.
def requestCBOE(ticker):
	# Make sure the ticker string is all lowercase.
	ticker = ticker.lower().strip("\r\n")

	# First, scrape and extract historical data.
	scrapeCBOEHistoric(ticker)
	pass


# Send a request to NYSE and parse the data to the appropriate file.
# @param: ticker, the string that is the ticker symbol for the company
#	in that market.
# @return: returns nothing.
def requestNYSE(ticker):
	# Make sure the ticker string is all lowercase.
	ticker = ticker.lower().strip("\r\n")

	# First, scrape and extract historical data.
	scrapeNYSEHistoric(ticker)
	
	# Next, scrape the current price for the ticker.


# Send a request to NASDAQ and parse the data to the appropriate file.
# @param: ticker, the string that is the ticker symbol for the company
#	in that market.
# @return: returns nothing.
def requestNASDAQ(ticker):
	# Make sure the ticker string is all lowercase.
	ticker = ticker.lower().strip("\r\n")

	# First, scrape and extract historical data.
	scrapeNASDAQHistoric(ticker)
	pass


# Scrape the historic data from CBOE given a ticker.
# @param: ticker, the string that is the ticker symbol for the company
#	in that market.
# @return: returns nothing.
def scrapeCBOEHistoric(ticker):
	pass


# Scrape the historic data from NYSE given a ticker.
# @param: ticker, the string that is the ticker symbol for the company
#	in that market.
# @return: returns nothing.
def scrapeNYSEHistoric(ticker):
	pass


# Scrape the historic data from NASDAQ given a ticker.
# @param: ticker, the string that is the ticker symbol for the company
#	in that market.
# @return: returns nothing.
def scrapeNASDAQHistoric(ticker):
	# Check the logs to see if the stock has been scraped today. If so,
	# return.
	path = None
	if opSys == "Windows":
		path = "Logs\\NASDAQ\\"
	else:
		path = "Logs/NASDAQ/"
	nasdaqTickerLog = open(path+ticker+"_HistLogs.txt", 'r+')
	# Load the log entries and the current time to variables.
	logEntries = nasdaqTickerLog.readlines()
	currentDate = datetime.datetime.now()
	# Close the log file.
	nasdaqTickerLog.close()
	# If there are log entries and the most recent entry was done today
	# then skip the scraping and return.
	if len(logEntries) != 0 and logEntries[-1].strip("\n") - currentDate == 0:
		return

	# Otherwise, scrape the historic data for the ticker.
	# Url for historic data.
	nasdaqStr = 'https://www.nasdaq.com/symbol/'+ticker+'/historical'

	# Request data from url. If the request didn't go through, exit the
	# method (This can be due to a change in the url or from lack of 
	# internet connection).
	req1 = requests.get(nasdaqStr)
	if req1.status_code != 200:
		print("Exiting requestNASDAQ(). Bad request status_code.", flush=True)
		return

	# Load contents of request into bs4 and parse with html parser.
	soup = bsoup(req1.content, 'html.parser')

	# Historical data is pulled from the url. Store it.
	data = []
	tables = soup.find_all("table")
	entries = tables[2].find_all("td")
	for e in entries:
		data.append(e.text.strip("\n").strip())

	# Data extracted.
	data = data[6:]

	# Data format is [date, open, high, low, closing, volume].
	# Format for csv row is [date, open, close, low, high, 52hi, 52lo,
	#	volume].

	# Break data into rows.
	rows = []
	#print(len(data))
	entry = 0
	#for entry in range(len(data)):
	while entry < len(data):
		#print(entry)
		dataRow = data[entry:entry+6]
		row = ["", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0"]
		row[0] = dataRow[0] # date.
		row[1] = dataRow[1] # open.
		row[2] = dataRow[4] # close.
		row[3] = dataRow[3] # low.
		row[4] = dataRow[2] # high.
		row[7] = dataRow[5].replace(",", "") # volume.
		rows.append(row)
		entry = entry + 6 # increment counter by 6 to get to next row.
		#print(entry)

	# If the file doesn't exist, create a new file. Otherwise, append 
	# data to the existing file. (Current string is windows compatible
	# only).
	fileTitle = None
	if opSys == "Windows":
		fileTitle = os.getcwd()+"\\NASDAQ\\nasdaq_"+ticker+"_History.csv"
	else:
		fileTitle = os.getcwd()+"/NASDAQ/nasdaq_"+ticker+"_History.csv"
	if os.path.exists(fileTitle):
		# Given that we have to append data to the file, it's best to
		# Not append repeat information from the csv. Best way to do
		# that is by checking the dates that have already been loaded
		# in.
		# Load the existing dates from the csv.
		csvDates = readFromCSV(fileTitle)

		# Compare the dates in the current data with the ones pulled
		# from the csv. The ones that match are thrown out. The rest
		# are written.
		iterator = 0
		while len(rows) != 0 and iterator != len(rows):
			row = rows[iterator]
			if row[0] in csvDates:
				rows.remove(row)
			else:
				iterator = iterator + 1

		# Write the remaining content to the list.
		if len(rows) > 0:
			writeToCSV(fileTitle, "a", rows) 
	else:
		writeToCSV(fileTitle, "w", rows)
	

	# Now that we have the historic data saved to the csv, we need to
	# log it. Open the log file from the beginning of this method in
	# "a"ppend mode.
	


# Load the data from the csv.
# @param, fileTitle: the title/path of the file.
# @return, returns a datatype containing a list of all datas in the csv
#	file.
def readFromCSV(fileTitle):
	# List of dates to be returned.
	dateList = []

	# Open the file.
	file = open(fileTitle, "r")
	fileReader = csv.reader(file, delimiter=",")

	# Iterate through the rows, appending all dates to the list.
	for row in fileReader:
		if "Date" in row[0]:
			continue
		else:
			#print(row[0])
			dateList.append(row[0])

	# Close file.
	file.close()

	# Return the list.
	return dateList


# Write data to csv. 
# @param, fileTitle: the title/path of the file.
# @param, writeMode: the string that determines how to write to the
# 	file. Options are either "w", "r", "a" but should only include the
#	first and last one ("w"rite and "a"ppend). 
# @oaram, rows: the data that has to be written to the file.
# @return, returns nothing.
def writeToCSV(fileTitle, writeMode, rows):
	# Open the file.
	file = open(fileTitle, writeMode)
	writeFile = csv.writer(file, delimiter=",",
							quotechar=" ", quoting=csv.QUOTE_MINIMAL,
							lineterminator='\n')

	# Special condition for writing to the file. Have to include the 
	# headers.
	if writeMode == "w":
		writeFile.writerow(["Date", "Open Price", "Closing Price",
							"Low", "High", "52Hi", "52Lo", "Volume"])

	# Write the actualy rows to the file.
	for line in range(len(rows)):
		#print(rows[line][7].replace(",", ""))
		writeFile.writerow(rows[line])

	# Close file.
	file.close()


if __name__ == '__main__':
	main()