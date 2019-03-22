# getHistoricNasdaq.py
# author: Diego Magdaleno
# Python program to access historical stock data. Only gets the last 30
# days so far by default.
# Python 3.6

import os
import sys
import requests
from bs4 import BeautifulSoup as bsoup


def main():
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

	# Data pulled from the url. Store it.
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

	# Break data into rows.
	rows = []
	for entry in range(len(data)):
		row = []
		row.append(data[entry%6])
		row.append(data[(entry+1)%6])
		row.append(data[(entry+4)%6])
		row.append(data[(entry+3)%6])
		row.append(data[(entry+2)%6])
		row.append(data[(entry+1)%6])
		row.append(data[(entry+5)%6])
		entry = entry+6

	# If the file doesn't exist, create a new file.

	# Otherwise, append data to the existing file.

	# Write data to csv.
	fileTitle = os.getcwd()+"\\NASDAQ\\nasdaq_"+ticker+"_History.csv"
	file = open(fileTitle, "w")
	writeFile = csv.writer(file, delimiter=",",
							quotechar="|", quoting=csv.QUOTE_MINIMAL)
	writeFile.writerow(["Date", "Open Price", "Closing Price", "Low",
						"High", "52Hi", "52Lo", "Volume"])
	for line in range(len(data)/6):
		row = data[:]
		writeFile.writerow()

	# Close file.
	file.close()


if __name__ == '__main__':
	main()