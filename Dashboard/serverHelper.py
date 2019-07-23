# serverHelper.py
# author: Diego Magdaleno
# Module with helper functions for the main flask server.
# Python 3.6
# Linux


import platform
from scraper import getTickers


# Check that a ticker is valid and exists in any market.
# @param: ticker, the string that is the ticker symbol for the company
#	in that market.
# @return: returns a tuple of a boolean and the market's name.
def validTicker(ticker):
	# Set up the file path for the ticker list files (Checks OS that
	# the app is running on).
	path = None
	if platform.system() == "Windows":
		path = "TickerLists\\"
	else:
		path = "TickerLists/"
	marketList = ['CBOE', 'NASDAQ', 'NYSE']
	# Check every market's ticker list.
	for market in marketList:
		tickerFilePath = path+market+"tickerlist.txt"
		# Open the file and load all lines to memory. Then close the
		# file.
		tickerFile = open(tickerFilePath, 'r')
		tickers = getTickers(tickerFile.readlines())
		tickerFile.close()
		# Check that the ticker exists within the list.
		if ticker.upper() in tickers:
			# If the ticker is valid, return true and the market it
			# belongs to.
			return (True, market)
	# If the market wasn't found, then send back False and a blank
	# string where the market name would be.
	return (False, '')


# Check that the user is valid and exists in the server's files.
# @param: user, a tuple containing the user's credentials.
# @return: returns a tuple with a boolean and the user's id hash.
def validUser(user):
	# Set up the file path for the user files (Checks OS that the app
	# is running on).
	path = None
	if platform.system() == "Windows":
		path = "Users\\"
	else:
		path = "Users/"
	userFilePath = path+"usersList.txt"
	userFile = open(userFilePath, 'r')
	users = userFile.readlines()
	if user in users:
		return (True, user)
	return (False, '')
