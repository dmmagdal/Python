# compareTickerLists2.py
# author: Diego Madaleno
# A slightly different version of compareTickerLists.py, this works
# with a different file in the tickerLists folder.
# A quick helper script for the project that checks all the ticker
# and matches the names (description) across markets (lists). Not for
# use in actual program. NOTE: Only compare NYSE and NASDAQ markets.
# Options on the CBOE are not avialable for either market.
# Python 3.6
# Linux


import os
import csv


def main():
	# Load each file's contents (except the first line. That's useless
	# text).
	nasdaqContents = openFile("\\Tickerlists\\companyListNASDAQ.csv")
	nyseContents = openFile("\\Tickerlists\\companyListNYSE.csv")
	#print(nasdaqContents[0])
	#print(nyseContents[0])
	#print(str(72*"-"))

	# Using only the names of companies (description) from each list,
	# identify the matches across lists.
	nasdaqNames = []
	nyseNames = []
	for nasRow in nasdaqContents:
		nasdaqNames.append(nasRow[1])
	for nyseRow in nyseContents:
		nyseNames.append(nyseRow[1])
		
	allThree = []
	for nasdaqName in nasdaqNames:
		#if nasdaqName in nyseNames and nasdaqName in cboeNames:
		#if nasdaqName in nyseContents and nasdaqName not in allThree:
		if nasdaqName in nyseNames and nasdaqName not in allThree:
			allThree.append(nasdaqName)

	print("Companies that exist on both NYSE and NASDAQ markets:")
	for name in allThree:
		print(name)
	print("Total names: "+str(len(allThree)))


# Open a specified file and return its contents.
# @param, fileTitle: the title/path of the file.
# @return, returns a list of lines from the file.
def openFile(fileTitle):
	# Open file.
	file = open(os.getcwd()+fileTitle, "r")
	fileReader = csv.reader(file, delimiter=",")
	# Save file lines to list.
	data = []
	for row in fileReader:
		if "Symbol" in row[0]:
			continue
		else:
			data.append(row)
	# Close file.
	file.close()
	# Return the list.
	return data


if __name__ == '__main__':
	main()
