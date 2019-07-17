# createTickerLogs.py
# author: Diego Magdaleno
# Simple script not part of the actual code base. This just creates 
# the initial ticker historic log files for all tickers in a market.


import sys
import platform


# Variable that stores the host OS.
opSys = None


def main():
	# Get the Host OS.
	# Windows = Windows
	# Mac = Darwin
	# Linux = Linux
	opSys = platform.system()

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

	# Create the ticker history logs.
	createCBOETickerHistLogs(cboeTickers)
	createNYSETickerHistLogs(nyseTickers)
	createNASDAQTickerHistLogs(nasdaqTickers)


# Extract the tickers from the txt file (first item when split by \t
# tab character). Skip first line.
# @param: fileLines, a list of all lines in the file.
# @return: returns a list of all ticker symbols in the file.
def getTickers(fileLines):
	tickerlist = []
	for line in fileLines[1:]:
		tickerlist.append(line.split("\t")[0])
	return tickerlist


# Iterate through each ticker in the ticker list for the cboe market
# and create a new blank history log file for that ticker in the
# specified path in the Logs folder.
# @param: cboeTickers, a list of all ticker strings for the cboe
#	market.
# @return: returns nothing.
def createCBOETickerHistLogs(cboeTickers):
	path = None
	if opSys == "Windows":
		path = "Logs\\CBOE\\"
	else:
		path = "Logs/CBOE/"

	for ticker in cboeTickers:
		#subprocess.run("touch "+path+ticker+"_HistLogs.txt")
		histLog = open(path+ticker+"_HistLogs.txt", 'w+')
		histLog.close()


# Iterate through each ticker in the ticker list for the nyse market
# and create a new blank history log file for that ticker in the
# specified path in the Logs folder.
# @param: nyseTickers, a list of all ticker strings for the nyse
#	market.
# @return: returns nothing.
def createNYSETickerHistLogs(nyseTickers):
	path = None
	if opSys == "Windows":
		path = "Logs\\CBOE\\"
	else:
		path = "Logs/CBOE/"

	for ticker in nyseTickers:
		#subprocess.run("touch "+path+ticker+"_HistLogs.txt")
		histLog = open(path+ticker+"_HistLogs.txt", 'w+')
		histLog.close()


# Iterate through each ticker in the ticker list for the nasdaq market
# and create a new blank history log file for that ticker in the
# specified path in the Logs folder.
# @param: nasdaqTickers, a list of all ticker strings for the nasdaq
#	market.
# @return: returns nothing.
def createNASDAQTickerHistLogs(nasdaqTickers):
	path = None
	if opSys == "Windows":
		path = "Logs\\CBOE\\"
	else:
		path = "Logs/CBOE/"

	for ticker in nasdaqTickers:
		#subprocess.run("touch "+path+ticker+"_HistLogs.txt")
		histLog = open(path+ticker+"_HistLogs.txt", 'w+')
		histLog.close()


if __name__ == '__main__':
	main()
