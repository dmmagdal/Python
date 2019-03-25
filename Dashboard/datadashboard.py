# datadashboard.py
# author: Diego Magdaleno
# This is an investment simulation program that utilizes several
# strategies to make decisions.
# Python 3.6
# Windows 10


import os
import sys
import datetime
import time
from win10toast import ToastNotifier


def main():
	# Check log file for last runtime.
	lastRun = checkLog()
	print("Program last run on "+lastRun+"\n")

	# If the program has not been run today, run all operations.
	currTime = datetime.datetime.now()
	#print(currTime)
	prevTime = datetime.datetime.strptime(lastRun, "%Y-%m-%d %H:%M:%S.%f")
	diff = currTime - prevTime
	if diff.days > 0:
		print("It has been at least a day since last run")
		appendLog(currTime)
		appendInvest(loadInvest())# Temporary until there can be
									   # updates.
	else:
		print("It has not been a day since last run")

	# Load investment data.
	investments = loadInvest()
	print("Investments Data:")
	print(investments)

	# Set investment variables (parse data into a more usable format)
	#accntVals = investments.split(",")[:4]
	#for val in accntVals:
	#	val = round(float(val), 2)
	#investDataStr = investments.split(",")[4:]

	# Enter infinite loop.
	#while True:
	#	continue


# Check to the last time the program has run. Return that timestamp.
# @param, takes no arguments.
# @return, returns a string that is the timestamp.
def checkLog():
	# Check to see if the logs file exists. If it doesn't, create the
	# log and write the current timestamp. Return the current
	# timestamp.
	if os.path.exists("logs.txt"):
		# Logs file does exist. Read the last entry.
		logFile = open("logs.txt", 'r')
		logLines = logFile.readlines()
		logFile.close()
		return logLines[len(logLines)-1].strip("\n")
	# File does not exits. Before returning current timestamp, create
	# the file and append this current time.
	logFile = open("logs.txt", 'w')
	timeStr = str(datetime.datetime.now())
	logFile.write(timeStr+"\n")
	logFile.close()
	return timeStr


# Append a the (current) timestamp to the logs.
# @param, timestamp: A string timestamp to be written to the logs.
# @return, returns nothing.
def appendLog(timestamp):
	logFile = open("logs.txt", 'a')
	logFile.write(str(timestamp)+"\n")
	logFile.close()


# Load the previous "day's" investment data from file.
# @param, takes not arugments.
# @return, returns a string of the most recent day's investment data.
def loadInvest():
	# Check to see if the investment file exists. If it doesn't, return
	# an arbitrary initial value.
	if os.path.exists("investmentLogs.txt"):
		# Logs file does exist. Read all lines to a list
		# (investmentsLines) and close the file.
		investmentFile = open("investmentLogs.txt", 'r')
		investmentsLines = investmentFile.readlines()
		investmentFile.close()
		# Find the endOfFile index (length of the read in list - 1).
		endOfFile = len(investmentsLines)-1
		# Iterate backwards through the list. Find the most recent
		# "header" entry for the file. Headers are the lines that
		# contain Date, BankAMT, InvestedAMT, NetWorth,
		# Total%ChngFromPrevDay. You can find the headers by looking
		# for the first line that doesn't start with a tab "\t", those
		# are lines that contain the list of current investments
		# (listOfInvestments).
		while endOfFile >= 0:
			if investmentsLines[0] != "\t":
				break
			else:
				endOfFile = endOfFile - 1 
		return investmentsLines[endOfFile:]
	# File does not exits. Before returning the string, create
	# the file and write in the starting values.
	investmentFile = open("investmentLogs.txt", 'w')
	startingVal = str(datetime.datetime.now())+" , 500, 0, 500, 0\n"
	investmentFile.write(startingVal) # Arbitrary value of money to
									  # invest.
	investmentFile.close()
	# Format for investments file:
	# Date, BankAMT, InvestedAMT, NetWorth, Total%ChngFromPrevDay
	#		[listOfInvestments]
	# Format for listOfInvestents:
	# Symbol, Exchange, NumShares
	# All investments in listOfInvestments List have their own line. So
	# the "header" of this data is the first list, then the 
	# listOfInvestments list follows after. The plan is to migrate this
	# so that every user has a file specific to them, but the file
	# format remains the same (apply to ALL log files).
	# Strings: Date, Symbol, Exchange
	# Floats (round to 2 decimal places): BankAMT, Invested, NetWorth,
	#	Total%ChngFromPrevDay
	# Ints: NumShares
	# ----------------------OLD FORMAT---------------------------------
	# Format for investments file:
	# BankAMT, InvestedAMT, NetWorth, Total%ChngFromPrevDay,
	#	[listOfInvestments]
	# Format for listOfInvestents:
	# [symbol, exchange, priceVal, NumShares, totalHoldingsVal,
	#	%ChangeFromPrevDay, prevPriceVal, AMTLoss/Gain] 
	# Note: all values in investment list are to be floats rounded to
	# 	two decimal places.
	# Note: all numerical values in the listOfInvestments are to be
	#	to be floats rounded to two decimal places.
	# -----------------------------------------------------------------
	return startingVal


# Append (current) investments to the investments logs.
# @param, newInvestments: the string of investment data to be appended
#	to the logs.
# @return, returns nothing.
def appendInvest(newInvestments):
	investmentFile = open("investmentLogs.txt", 'a')
	investmentFile.write(newInvestments+"\n")
	investmentFile.close()


# Give a Windows 10 notification.
# @param, title: a string that makes up the title of the notification.
# @param, msg: a string that makes up the notification message body.
# @return, returns nothing.
def notifyWin(title, msg):
	notify = ToastNotifier()
	notify.show_toast(title, msg)


if __name__ == '__main__':
	main()
