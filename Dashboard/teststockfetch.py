# teststockfetch.py
# author: Diego Magdaleno
# Small test program that can fetch real time stock info from a market
# given a ticker symbol and parse the data from the page.
# Needs to be able to get 52hi, 52lo, op, cl, current price, volume
# traded, previous closing.


import requests
import sys
#import selenium
from bs4 import BeautifulSoup as bsoup
#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.keys import Keys
#import json


def main():
	if len(sys.argv) != 3:
		print("Error: Usage python teststockfetch.py <market> <ticker>")
		exit(1)

	# String for ticker symbol.
	ticker = sys.argv[2].lower()

	# String for markets
	nyseStr = 'https://www.nyse.com/quote/'+ticker.upper()
	nasdaqStr = 'https://www.nasdaq.com/symbol/'+ticker+'/real-time'
	cboeStr = 'http://www.cboe.com/delayedquote/advanced-charts?ticker='+ticker.upper()

	print(ticker)
	print(nyseStr)
	print(nasdaqStr)
	print(cboeStr)

	# Pull real time stock data (format should be generic)
	# For nyse https://www.nyse.com/quote/TICKER_SYMBOL_ALL_UPPER
	# For nasdaq https://www.nasdaq.com/symbol/TICKER_SYMBOL_ALL_LOEWR/real-time
	# For cboe http://www.cboe.com/delayedquote/advanced-charts?ticker=TICKER_SYMBOL_ALL_LOWER
	# Where TICKER_SYMBOL is the ticker for a company in that respective
	#	market.
	#req = requests.get('https://www.nyse.com/quote/MSFT')
	req = requests.get(nyseStr)
	# Work on NASDAQ for the moment while I sort out NYSE later.
	#req2 = requests.get('https://www.nasdaq.com/symbol/msft/real-time')
	req2 = requests.get(nasdaqStr)
	req3 = requests.get(cboeStr)

	# Print contents of request.
	#print(req.content)
	soup = bsoup(req.content, 'html.parser')
	#print(soup.prettify().encode('utf-8'))

	# Working. IGNORE NOW.
	#print(req2.content)
	soup2 = bsoup(req2.content, 'html.parser')
	#print(soup2.prettify().encode('utf-8'))

	soup3 = bsoup(req3.content, 'html.parser')

	print("\n")

	# Extract an attribute. TEST CODE FOR METHOD. IGNORE NOW.
	# lastSaleVal = soup2.find('span', id='quotes_content_left__LastSale')
	# print(lastSaleVal)
	# print(type(lastSaleVal))
	# print(lastSaleVal.text)
	# print("\n\n\n")

	# Check which market was written (Only works on NYSE and NASDAQ for
	# now).
	if sys.argv[1] == 'nyse':
		getNYSE(sys.argv[2], soup)
	elif sys.argv[1] == 'nasdaq':
		getNASDAQ(sys.argv[2], soup2)
	elif sys.argv[1] == 'cboe':
		getCBOE(sys.argv[2], soup3)
	else:
		print("Error: Please enter a valid market")
		exit(1)

	exit(0)


# Extract necessary data from NYSE
def getNYSE(ticker, soup):
	# The NYSE data is loaded with AJAX/Javascript and can't be read
	# with requests library. Instead, we'll be using the selenium
	# module and the chrome driver for windows. This may have to be
	# handled later for a more universal/ cross platform approach.
	#chrDriver = webdriver.Chrome;

	# Aborted using selenium for now. Looking for other alternatives 
	# before going back and making a mess.


	# lastSale = soup2.find('span', {'class': 'd-dquote-datablock-value'})
	# netChange = soup2.find('span', id='quotes_content_left__NetChange')
	# #upDown = soup2.find('div', id='_updownimage')
	# pctChange = soup2.find('span', id='quotes_content_left__PctChange')
	# lastSaleVol = soup2.find('span', id='quotes_content_left__Volume')
	# prevClose = soup2.find('span', id='quotes_content_left__PreviousClose')
	# todayLo = soup2.find('span', id='quotes_content_left__TodaysLow')
	# todayHi = soup2.find('span', id='quotes_content_left__TodaysHigh')
	# Lo52 = soup2.find('span', id='quotes_content_left__52WeekLow')
	# Hi52 = soup2.find('span', id='quotes_content_left__52WeekHigh')
	
	#listOfData = soup.find_all('span', {'class': 'd-dquote-datablock-value'})
	#listOfData = soup.find_all('div', {'class': 'd-containter  d-nowrap d-justify-start d-align-start d-flex-fix d-dquote-body d-scroll-y'})
	#listOfData = soup.find_all('div', class_='d-dquote-datablock')
	listOfData = soup.find_all('div')
	#listOfData = soup.find_all('span', class_='d-dquote-datablock-value')
	#listOfData = soup.find_all(text='Last:')
	#print(listOfData)
	#print(len(listOfData))
	file = open('temp.txt', 'w')
	for el in listOfData:
		#print(el.get('div'))
		#print(el['class'])
		#print(el)
		#print()
		file.write(str(el))
		file.write("\n")
	#print(type(listOfData[0]))
	file.close()
	upDown = None


# Extract necessary data from NASDAQ
def getNASDAQ(ticker, soup2):
	# Note: lastSale = price at which stock last traded during normal
	# market hours (The last price it was traded at)
	# lastSaleVol = the volume of shares traded on the exchange during
	# normal market hours (The volume traded during the previous day)
	# Get data from real time graph.
	lastSale = soup2.find('span', id='quotes_content_left__LastSale')
	netChange = soup2.find('span', id='quotes_content_left__NetChange')
	#upDown = soup2.find('div', id='_updownimage')
	pctChange = soup2.find('span', id='quotes_content_left__PctChange')
	lastSaleVol = soup2.find('span', id='quotes_content_left__Volume')
	prevClose = soup2.find('span', id='quotes_content_left__PreviousClose')
	todayLo = soup2.find('span', id='quotes_content_left__TodaysLow')
	todayHi = soup2.find('span', id='quotes_content_left__TodaysHigh')
	Lo52 = soup2.find('span', id='quotes_content_left__52WeekLow')
	Hi52 = soup2.find('span', id='quotes_content_left__52WeekHigh')

	# Have a check so that if the items don't exist, that means the
	# page loaded is not correct.
	if None in [lastSale, netChange, pctChange, lastSaleVol, prevClose,
				todayLo, todayHi, Lo52, Hi52]:
		print("Error: Page loaded does not fit format.")
		exit(1)

	#print(upDown)
	upDown = None
	if (soup2.find('span', {'class': 'red'}) != None):
		#print("down")
		upDown = "\\/"
	else:
		#print("up")
		upDown = "/\\"

	# Print results of scrape.
	print("Last Sale:"+ lastSale.text)
	print("Net Change: "+ netChange.text+" "+ upDown)
	print("Percent Change: "+ pctChange.text)
	print("Last Sale Volume: "+ lastSaleVol.text)
	print("Previous Closing Value: "+ prevClose.text)
	print("Today's High/Low: "+ todayHi.text+"/"+todayLo.text)
	print("52 Week High/Low: "+ Lo52.text+"/"+Hi52.text)


# Extract necessary data from CBPE.
def getCBOE(ticker, soup3):
	lastSale = soup3.find('span', id='quotes_content_left__LastSale')
	netChange = soup3.find('span', id='quotes_content_left__NetChange')
	#upDown = soup2.find('div', id='_updownimage')
	pctChange = soup3.find('span', id='quotes_content_left__PctChange')
	lastSaleVol = soup3.find('span', id='quotes_content_left__Volume')
	prevClose = soup3.find('span', id='quotes_content_left__PreviousClose')
	todayLo = soup3.find('span', id='quotes_content_left__TodaysLow')
	todayHi = soup3.find('span', id='quotes_content_left__TodaysHigh')
	Lo52 = soup3.find('span', id='quotes_content_left__52WeekLow')
	Hi52 = soup3.find('span', id='quotes_content_left__52WeekHigh')

	# Have a check so that if the items don't exist, that means the
	# page loaded is not correct.
	if None in [lastSale, netChange, pctChange, lastSaleVol, prevClose,
				todayLo, todayHi, Lo52, Hi52]:
		print("Error: Page loaded does not fit format.")
		exit(1)

	#print(upDown)
	upDown = None
	if (soup3.find('span', {'class': 'red'}) != None):
		#print("down")
		upDown = "\\/"
	else:
		#print("up")
		upDown = "/\\"

	# Print results of scrape.
	print("Last Sale:"+ lastSale.text)
	print("Net Change: "+ netChange.text+" "+ upDown)
	print("Percent Change: "+ pctChange.text)
	print("Last Sale Volume: "+ lastSaleVol.text)
	print("Previous Closing Value: "+ prevClose.text)
	print("Today's High/Low: "+ todayHi.text+"/"+todayLo.text)
	print("52 Week High/Low: "+ Lo52.text+"/"+Hi52.text)


# Print html to file.
def print2File(lines, fileName=None):
	if fileName == None:
		file = open('temp.txt', 'w')
		for el in lines:
			file.write(str(el))
			file.write("\n")
		file.close()
	else:
		file = open(fileName, 'w')
		for el in lines:
			file.write(str(el))
			file.write("\n")
		file.close()


if __name__ == '__main__':
	main()