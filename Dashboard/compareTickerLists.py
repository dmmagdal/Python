# compareTickerLists.py
# author: Diego Madaleno
# A quick helper script for the project that checks all the ticker
# and matches the names (description) across markets (lists). Not for
# use in actual program. NOTE: Only compare NYSE and NASDAQ markets.
# Options on the CBOE are not avialable for either market.
# Python 3.6
# Linux


import os


def main():
	# Load each file's contents (except the first line. That's useless
	# text).
	nasdaqContents = openFile("\\Tickerlists\\NASDAQtickerlist.txt")[1:]
	nyseContents = openFile("\\Tickerlists\\NYSEtickerlist.txt")[1:]
	#cboeContents = openFile("\\Tickerlists\\CBOEtickerlist.txt")[1:]

	# Using only the names of companies (description) from each list,
	# identify the matches across lists.
	nasdaqNames = []
	nyseNames = []
	#cboeNames = []
	for nasRow in nasdaqContents:
		nasdaqNames.append(nasRow.split("\t")[1].strip("\n"))
	for nyseRow in nyseContents:
		nyseNames.append(nyseRow.split("\t")[1].strip("\n"))
	#for cboeRow in cboeContents:
	#	cboeNames.append(cboeRow.split("\t")[1].strip("\n"))
		
	allThree = []
	for nasdaqName in nasdaqNames:
		#if nasdaqName in nyseNames and nasdaqName in cboeNames:
		if nasdaqName in nyseNames:
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
	# Save file lines to list.
	data = file.readlines()
	# Close file.
	file.close()
	# REturn the list.
	return data


if __name__ == '__main__':
	main()