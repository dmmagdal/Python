# getHistoricNasdaq.py
# author: Diego Magdaleno
# Python program to access historical stock data. Only gets the last 30
# days so far by default.
# Python 3.6

import os
import sys
import requests
import csv
from bs4 import BeautifulSoup as bsoup


def main():
	# Check length of file args.
	if len(sys.argv) != 2:
		print("Error: Usage python getHistoricNasdaq.py <ticker>")
		exit(1)

	# String for ticker symbol.
	ticker = sys.argv[1].lower()

	# Url String.
	nasdaqStr = 'https://www.nasdaq.com/symbol/'+ticker+'/historical'

	# Request from url.
	#payloadData = {"ddlTimeFrame": "10y"}
	#req1 = requests.post(nasdaqStr, data=payloadData)
	req1 = requests.get(nasdaqStr)

	# Load contents of request into bs4 and parse with html parser.
	soup = bsoup(req1.content, 'html.parser')

	# Historical data pulled from the url. Store it.
	data = []
	tables = soup.find_all("table")
	# if tables is None:
	# 	print("Found no tables")
	# else:
	# 	#print(tables[2])
	# 	entries = tables[2].find_all("td")
	# 	#print(entries)
	# 	for e in entries:
	# 		#print(e.text.strip("\n").strip())
	# 		data.append(e.text.strip("\n").strip())
	entries = tables[2].find_all("td")
	for e in entries:
		data.append(e.text.strip("\n").strip())


	# Data extracted.
	# for point in data[6:]:
	# 	print(point)
	# print(len(data[6:]))
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
	fileTitle = os.getcwd()+"\\NASDAQ\\nasdaq_"+ticker+"_History.csv"
	if os.path.exists(fileTitle):
		writeToCSV(fileTitle, "a", rows) 
	else:
		writeToCSV(fileTitle, "w", rows)


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
