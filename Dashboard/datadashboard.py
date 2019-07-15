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
from tkinter import messagebox
import socket
import cryptography
from cryptography.fernet import Fernet

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
	m.resizable(False, False)
	logoImg = PhotoImage(file="dblogo.png")
	logoLbl = Label(image=logoImg)
	logoLbl.grid(column=1, row=0, columnspan=1, padx=25, pady=15)
	
	# Entry boxes for username, password, and server IP.
	usernameLbl = Label(m, text="username")
	passwordLbl = Label(m, text="password")
	serverIPLbl = Label(m, text="server ip")
	username = Entry(m)
	password = Entry(m, show="*")
	serverIP = Entry(m)

	# Checkbox to remember user. This box will already be "checked"
	# upon loading if there exists a file called "remuser.txt" and
	# its contents can be loaded and decrypted to text. Those contents
	# are then loaded into the entries for username and password.
	# ServerIP is not stored.
	var = IntVar()

	# Check to see if file exits. Otherwise, continue as normal.
	if os.path.exists("remuser.txt") and os.path.isfile("remuser.txt"):
		# Since it does, load the files.
		file = open("remuser.txt", "rb")
		lines = file.readlines()
		file.close()
		keyFile = open("user.key", "rb")
		key = keyFile.read()
		keyFile.close()
		# Encrypted user data loaded in.
		user = lines[0]
		passw = lines[1]
		# Decrypt the data.
		f = Fernet(key)
		decrypUser = f.decrypt(user).decode("utf-8")
		decrypPass = f.decrypt(passw).decode("utf-8")

		# Set the entry values. Keep the listbox checked.
		username.insert(0, decrypUser)
		password.insert(0, decrypPass)
		var.set(1)

	# Checkbutton to remember a user or not.
	rememberMe = Checkbutton(m, text="Remember Me", variable=var,
							 onvalue=1, offvalue=0)

	# Buttons for logging in, creating a new user, or if a user forgot
	# their password.
	logInBtn = Button(m, text="Log In",
					  command=(lambda: logIn(m,
					  						 username.get(),
					  						 password.get(),
					  						 serverIP.get(),
					  						 var)))
	newUserBtn = Button(m, text="New User",
						command=(lambda: createNewUser(m,
													serverIP.get())))
	forgotPassBtn = Button(m, text="Forgot Passord",
						   command=(lambda: forgotPassword(m,
						   							serverIP.get())))

	# Layout the widgets.
	usernameLbl.grid(column=0, row=1)
	username.grid(column=1, row=1)
	passwordLbl.grid()
	password.grid(column=1, row=2, pady=10)
	serverIPLbl.grid(padx=15)
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
def logIn(m, username, password, serverIP, checked):
	# Check if any of the parameters are empty. None should be empty.
	entryList = [username, password, serverIP]
	if None in entryList or "" in entryList:
		# Print Error messagebox. Exit method.
		errStr = "Please fill out all entries before logging in."
		messagebox.showerror("Error", errStr)
		return

	# Depending of the variable from the checkbutton, either store the
	# input to a file encrypted if the button is toggled "on" or delete
	# the old file if the box is toggled to "off".
	if checked.get() == 1:
		# Generate new key. Store it to file.
		key = Fernet.generate_key()
		keyFile = open("user.key", "wb")
		keyFile.write(key)
		keyFile.close()
		# Encrypt the user data. First turn the strings to bytes with
		# encode().
		userBytes = username.encode()
		passBytes = password.encode()
		# Create an encryption function based on the key generated.
		f = Fernet(key)
		# Encrypt the byte data given the encryption function.
		encryptedUser = f.encrypt(userBytes)
		encryptedPass = f.encrypt(passBytes)
		# Write the data to file.
		file = open("remuser.txt", "wb")
		file.write(encryptedUser)
		file.write("\n".encode("utf-8"))
		file.write(encryptedPass)
		file.close()
	else:
		# Delete the files.
		os.remove("remuser.txt")
		os.remove("user.key")

	# Destroy the login window (Close it).
	m.destroy()

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
		# Try connecting to the server.
		connection = None

		# Once connected, load a GUI window for the user to enter their
		# new credentials.
		# Close the previous window.
		m.destroy()
		# New tkinter GUI object for the window.
		m2 = Tk()
		m2.title("Create New Dashboard Account")
		m2.geometry("300x400")
		m2.resizable(False, False)
		profileImg = PhotoImage(file="blankprofileicon.png")
		profileLbl = Label(image=profileImg)
		profileLbl.grid(column=1, row=0, columnspan=1, padx=25, pady=15)

		# Labels for the entries.
		newUserLbl = Label(m2, text="New Username")
		newPassLbl = Label(m2, text="New Password")
		newPassLbl2 = Label(m2, text="Re-enter Password")
		newUserEmailLbl = Label(m2, text="Your recovery email")

		# Entries for the new user to enter their information.
		newUser = Entry(m2)
		newPass = Entry(m2, show="*")
		newPass2 = Entry(m2, show="*")
		newUserEmail = Entry(m2)

		# Buttons to either affirm or cancel the registration.
		createUserBtn = Button(m2, text="Create Account", 
							command=(lambda: saveNewUser(newUser.get(),
													newPass.get(),
													newPass2.get(),
													newUserEmail.get(),
													connection,
													m2)))
		cancelBtn = Button(m2, text="Cancel", 
							command=(lambda: cancelEntry(m2)))

		# Place the widgets in the GUI.
		newUserLbl.grid(column=1, row=1, padx=105)
		newUser.grid(column=1, row=2)
		newPassLbl.grid(column=1, row=3)
		newPass.grid(column=1, row=4)
		newPassLbl2.grid(column=1, row=5)
		newPass2.grid(column=1, row=6)
		newUserEmailLbl.grid(column=1, row=7)
		newUserEmail.grid(column=1, row=8)
		createUserBtn.grid(column=1, row=12, pady=15)
		cancelBtn.grid(column=1, row=13)

		m2.mainloop()
	except Exception as e:
		raise e


# Save the data to the server.
# @param, newUser: the new user's username.
# @param, newPass: the new user's password.
# @param, newPass2: the new user's password. Should match its partner
#	above. Used to confirm the password. 
# @param, newUserEmail: the user's recovery email for their account.
# @param, conn: the connection to the server.
# @param, m2: a tkinter object of the new user creation window.
# @return, returns nothing.
def saveNewUser(newUser, newPass, newPass2, newUserEmail, conn, m2):
	# If the contents of the entries are blank, give an error message
	# and return.
	entryList = [newUser, newPass, newPass2, newUserEmail]
	if None in entryList or "" in entryList:
		errStr = "Please fill out all entries before logging in."
		messagebox.showerror("Error", errStr)
		return

	# If the passwords do not match, give an error message and return.
	if newPass != newPass2:
		errStr = "Please make sure your password matches."
		messagebox.showerror("Error", errStr)
		return

	# Send the save command and info to the server.

	# Destroy the window (Close it).
	m2.destroy()


# Closes the tkinter object passed in.
# @param, m: a tkinter object of a window.
# @return, returns nothing.
def cancelEntry(m):
	m.destroy()
	loadLogin()


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
	try:
		# Try connecting to the server.
		connection = None

		# Once connected, load a GUI window for the user to enter their
		# recovery password.
		# Close the previous window.
		m.destroy()
		# New tkinter GUI object for the window.
		m2 = Tk()
		m2.geometry("300x400")

		recEmailLbl = Label(m2, text="Recovery Email")
		recEmail = Entry(m2)
		recBtn = Button(m2, text="Send Recovery Email",
						command=(lambda: sendRecoveryEmail(m2,
													recEmail.get(),
													connection)))

		m2.mainloop()
	except Exception as e:
		raise e


# Send the command to the server to send the recovery email to the
# address specified.
# @param, m2: a tkinter object of the recovery email window.
# @param, recoveryEmail: the user's recovery email.
# @param, conn: the connection to the server.
# @return, returns nothing.
def sendRecoveryEmail(m2, recoveryEmail, conn):
	# If the contents of the entry are blank, give an error message
	# and return.
	if recoveryEmail == None or "" == recoveryEmail:
		errStr = "Please fill out all entries before logging in."
		messagebox.showerror("Error", errStr)
		return

	# Otherwise, send the command to the server to send the recovery
	# email to the address specified.

	# Destroy the window (Close it).
	m2.destroy()


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
