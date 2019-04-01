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
from tkinter import *
import socket
from win10toast import ToastNotifier


def main():
	# Check log file for last runtime.
	lastRun = checkLog()
	print("Program last run on "+lastRun+"\n")

	# If the program has not been run today, run all operations.
	currTime = datetime.datetime.now()
	prevTime = datetime.datetime.strptime(lastRun, "%Y-%m-%d %H:%M:%S.%f")
	diff = currTime - prevTime
	if diff.days > 0:
		print("It has been at least a day since last run")
		# Append the current time to the log.
		appendLog(currTime)
		appendInvest(loadInvest())# Temporary until there can be
								  # updates.
	else:
		print("It has not been a day since last run")

	# Load investment data.
	investments = loadInvest()
	print("Investments Data:")
	#print(investments)
	#print(type(investments))
	#print(len(investments))

	# Set investment variables (parse data into a more usable format).
	accntVals = investments[0].split(",")
	for point in range(len(accntVals)):
		accntVals[point] = accntVals[point].strip("\n").lstrip(" ")
		print(accntVals[point])

	print(str(72*"-"))
	# Load investment data (parse data into a more usable format).
	investmentData = []
	if len(investments) != 1:
		investmentData[1:]
		for dataPt in range(len(investmentData)):
			investmentData[dataPt] = investmentData[dataPt].strip("\n")
			print(investmentData[dataPt])
	else:
		print("No investments saved.")

	#accntVals = investments.split(",")[:4]
	#for val in accntVals:
	#	val = round(float(val), 2)
	#investDataStr = investments.split(",")[4:]

	loadLogin()
	# UNCOMMENT LATER
	#loadGUI(accntVals, investmentData)

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
	return [startingVal.strip("\n")]


# Append (current) investments to the investments logs.
# @param, newInvestments: the string of investment data to be appended
#	to the logs.
# @return, returns nothing.
def appendInvest(newInvestments):
	investmentFile = open("investmentLogs.txt", 'a')
	#investmentFile.write(newInvestments+"\n")
	for line in newInvestments:
		investmentFile.write(line+"\n")
	investmentFile.close()


# Give a Windows 10 notification.
# @param, title: a string that makes up the title of the notification.
# @param, msg: a string that makes up the notification message body.
# @return, returns nothing.
def notifyWin(title, msg):
	notify = ToastNotifier()
	notify.show_toast(title, msg)


# Display the log in screen for the user.
# @param, takes no arguments.
# @return, returns nothing.
def loadLogin():
	# Initialize GUI.
	m = Tk()
	m.title("Dashboard LogIn")
	m.geometry("300x400")
	
	# Entry boxes for username, password, and server IP.
	usernameLbl = Label(m, text="username")
	passwordLbl = Label(m, text="password")
	serverIPLbl = Label(m, text="server ip")
	username = Entry(m)
	password = Entry(m)
	serverIP = Entry(m)

	# Checkbox to remember user.
	var = IntVar()
	rememberMe = Checkbutton(m, text="Remember Me", variable=var,
							 command=(lambda x: rememberUser(var)))

	# Buttons for logging in, creating a new user, or if a user forgot
	# their password.
	logInBtn = Button(m, text="Log In",
					  command=(lambda: logIn(m,
					  						 username.get(),
					  						 password.get(),
					  						 serverIP.get())))
	newUserBtn = Button(m, text="New User",
						command=(lambda: createNewUser(m,
													serverIP.get())))
	forgotPassBtn = Button(m, text="Forgot Passord",
						   command=(lambda: forgotPassword(m,
						   							serverIP.get())))

	# Layout the widgets.
	usernameLbl.grid(column=0, row=1, sticky="E")
	username.grid(column=1, row=1, sticky="E")
	passwordLbl.grid()
	password.grid(column=1, row=2, pady=10)
	serverIPLbl.grid()
	serverIP.grid(column=1, row=3, pady=10)
	rememberMe.grid(column=1, row=4)
	logInBtn.grid(column=1, row=5)
	newUserBtn.grid(column=1, row=7, pady=25)
	forgotPassBtn.grid(column=1, row=8)

	m.mainloop()


# Log into the user's account on the server.
# @param, m: a tkinter object of the login window.
# @param, username: a string from the tkinter entry that contains the
#	user's username.
# @param, password: a string from the tkinter entry that contains the
#	user's password.
# @param, serverIP: a string that contains the ip address of the server
#	the user wants to connect to.
# @return, returns nothing.
def logIn(m, username, password, serverIP):
	# Check if any of the parameters are empty.
	entryList = [username, password, serverIP]
	if None in entryList:
		# Print Error messagebox. Exit method.
		return
	# Try connecting to server. Upon successful connection, load data
	# to client and close the login page. Otherwise, print Error
	# messagebox and exit method.
	pass


# Create a new user account on the server.
# @param, m: a tkinter object of the login window.
# @param, serverIP: a string that contains the ip address of the server
#	the user wants to connect to.
# @return, returns nothing.
def createNewUser(m, serverIP):
	# Try logging into server under "newGuest" account. Upon successful
	# connection, have the user fill out a new form with their 
	# credentials. Then redirect back to the login page. Otherwise,
	# print Error messagebox and exit method.
	try:
		pass
	except Exception as e:
		raise e
	pass


# User forgot their password. Redirect them to a window where they can
# enter the email they used when they registered.
# @param, m: a tkinter object of the login window.
# @param, serverIP: a string that contains the ip address of the server
#	the user wants to connect to.
# @return, returns nothing.
def forgotPassword(m, serverIP):
	# Try logging into the server under "otherGuest" account (different
	# from "newGuest"). Upon successful connection, have the user enter
	# their email into a form and have the program send a recovery
	# email with their password. Otherwise, print Error messagebox and
	# exit method.
	pass


# Load the first GUI's page.
# @param, accntVals: Load all account values from the logs.
# @param, investmentData: Load all investments from the user's logs.
# @return, returns nothing.
def loadGUI(accntVals, investmentData):
	# Initialize GUI.
	m = Tk()
	m.title("Dashboard Client")
	m.geometry("675x550")

	# Listbox and listbox for previous console data.
	scrollbar = Scrollbar(m)
	console = Listbox(m, width=80, height=20,
					  yscrollcommand=scrollbar.set)
	consoleEntry = Entry(m)
	scrollbar.pack(side="left")
	console.pack(side="left")
	consoleEntry.pack(side="left")

	
	m.mainloop()


if __name__ == '__main__':
	main()
