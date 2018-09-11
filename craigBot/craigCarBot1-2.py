# craigCarBot1-2.py
# author: Diego Magdaleno
# Craigslist bot that searches for cars desired by the user. Program
# only takes one or more users at a time but only takes one car search
# at a time (This can be changed later).
# Chagnes: More cleanup.
# Python 2.7
# Windows 10

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from Tkinter import *
from tkMessageBox import *
from datetime import date
import datetime
import calendar
import smtplib

def main():
	# Initilaize GUI.
	# Create Tkinter object.
	m = Tk()
	m.geometry("300x300")

	# Take user's email.
	emailLbl = Label(m, text="Enter your email: ")
	emailLbl.place(x=25, y=25)
	emailTxtBx = Entry(m)
	emailTxtBx.place(x=125, y=25)

	# Take the make of the car.
	makeLbl = Label(m, text="Make: ")
	makeLbl.place(x=25, y=100)
	makeTxtBox = Entry(m)
	makeTxtBox.place(x=100, y=100)

	# Take the model/type.
	modelLbl = Label(m, text="Model/Type: ")
	modelLbl.place(x=25, y=125)
	modelTxtBox = Entry(m)
	modelTxtBox.place(x=100, y=125)

	# Take the year range.
	yearRangeLbl = Label(m, text="Year Range: ")
	yearRangeLbl.place(x=25, y=150)
	yearRngTxtBox1 = Entry(m)
	yearRngTxtBox1.place(x=100, y=150)
	yearRngTxtBox1.place(width=50)
	dashLbl = Label(m, text=" - ")
	dashLbl.place(x=160, y=150)
	yearRngTxtBox2 = Entry(m)
	yearRngTxtBox2.place(x=190, y=150)
	yearRngTxtBox2.place(width=50)

	# Start bot/search.
	searchBtn = Button(m, text="Start", 
					   command=(lambda: runBot(m,
					   						   makeTxtBox.get(),
					   						   modelTxtBox.get(),
					   						   yearRngTxtBox1.get(),
					   						   yearRngTxtBox2.get(),
					   						   emailTxtBx.get())))
	searchBtn.place(x=125, y=225)

	m.mainloop()


def runBot(m, make, model, yearRange1, yearRange2, email):
	# Check email is populated and at least two of the car parameters
	# are populated.
	yearCondition = yearRange1 == "" and yearRange2 == ""
	condition1 = make == "" and model == "" and yearCondition
	condition2 = make == "" and model == ""
	condition3 = make == "" and yearCondition
	condition4 = model == "" and yearCondition
	if email == "" or condition1 or condition2 or condition3 or condition4:
		errmsg = "Email must be filled out as well as at least two of"
		errmsgPt2 = " the search parameters."
		showerror("Error", errmsg + errmsgPt2)
		return
	# Check the year range to make sure that it's a populated with a
	# number.
	yearRange = yearRange1 + " " + yearRange2
	#newYearRange = ""
	newYearRange = yearRange
	years = yearRange.split(" ")
	if len(years) == 0:
		newYearRange = ""
	elif len(years) == 2:
		if years[0] != "" and years[1] != "":
			if not years[0].isdigit() or not years[1].isdigit():
				showerror("Error", "Years have to be numbers.")
				return
			else:
				newYearRange = years[0] + "-" + years[1]
		elif years[0] == "" and years[1] != "":
			if not years[1].isdigit():
				showerror("Error", "Years have to be numbers.")
				return
			else:
				newYearRange = years[1]
		elif years[0] != "" and years[1] == "":
			if not years[0].isdigit():
				showerror("Error", "Years have to be numbers.")
				return
			else:
				newYearRange = years[0]
	elif len(years) != 2:
		showerror("Error", "Check year range.")
		return

	# Close/destroy Tkinter object.
	m.destroy()

	# Print out the search to monitor what session is currently being
	# run.
	print "Search: " + newYearRange + " " + make + " " + model
	print "Email: " + email

	# Create a log file that stores when the bot last searched.
	lgNmPt1 = "logs_" + str(email).split("@")[0] + "_"
	lgNmPt2 = str(newYearRange) + "_" + str(make) + "_"
	logName = lgNmPt1 + lgNmPt2 + str(model) + ".txt"
	logFile = open(logName, "w+")
	header = "Bot: " + email
	sh1 = "Search: " + str(newYearRange)
	sh2 = " " + str(make) + " " + str(model)
	subHeader = sh1 + sh2
	logFile.write(header + "\n")
	logFile.write(subHeader + "\n")
	logFile.write("\n")
	logFile.close()

	# Open and write data to file.
	resultsNmPt1 = "Results_" + str(email).split("@")[0] + "_"
	resultsNmPt2 = str(newYearRange) + "_" + str(make)
	resultsNmPt3 = "_" + str(model)
	resultsName = resultsNmPt1 + resultsNmPt2 + resultsNmPt3 + ".txt"
	oldResults = open(resultsName, "w+")
	oldResults.write(header + "\n")
	oldResults.write(subHeader + "\n")
	oldResults.write("\n")
	oldResults.close()

	# UNBLOCK WHEN FINISHED.
	'''
	# Infinite loop to cosntantly check the time.
	while True:
		# Get current date (MM/DD/YYYY)
		currentDate = datetime.datetime.now().strftime('%m-%d-%Y')

		#print date.today()
		my_date = date.today()
		day_of_week = calendar.day_name[my_date.weekday()]
		#print day_of_week
		time_of_day = datetime.datetime.now().strftime("%H:%M:%S")
		#print time_of_day

		# Run search M-W-F at noon.
		day1 = day_of_week == "Monday"
		day2 = day_of_week == "Wedensday"
		day3 = day_of_week == "Friday"
		dayCondition = day1 or day2 or day3
		if dayCondition and time_of_day == "12:00:00":
			# Search the logs and make sure that there wasn't already
			# an entry that day.
			readLogs = open(logName, "r")
			logLines = readLogs.readlines()
			readLogs.close()

			# If there was an entry for that day, skip.
			if currentDate in logLines:
				continue
			# Otherwise, run a search. 
			else:
				# INSERT CODE HERE.
				# Write to logs with time.
				writeLogs = open(logName, "a")
				logPt1 = str(currentDate) + " "
				logPt2 = str(day_of_week) + "\n"
				writeLogs.write(logPt1 + logPt2)
				writeLogs.close()
				runCarSearch(newYearRange, make, model, email,
							 currentDate, resultsName)
	'''

	# CODE TO BE INSERTED INTO LOOP.
	# Get current date (MM/DD/YYYY)
	currentDate = datetime.datetime.now().strftime('%m-%d-%Y')
	runCarSearch(newYearRange, make, model, email, currentDate,
				 resultsName)


# This function runs the search on craigslist.
# @param takes no arguments.
# @return returns nothing.
def runCarSearch(newYearRange, make, model, email, curntDate, rsltNm):
	# Create webdriver object (run in headless).
	firefox_options = Options()
	#firefox_options.add_argument('--headless')
	#firefox_options.add_argument('--window-size=1920x1080')
	firefox_driver = webdriver.Firefox(firefox_options=firefox_options)

	# Interact with webpage.
	firefox_driver.get("https://sfbay.craigslist.org/")
	searchBox = firefox_driver.find_element_by_id("query")

	# Run the seach in craigslist.
	querystring = newYearRange + " " + make + " " + model
	searchBox.click()
	searchBox.send_keys(querystring)
	searchBox.send_keys(Keys.ENTER)

	firefox_driver.implicitly_wait(5)

	# Retrieve total number of results.
	tCountStr = "//span[@class='totalcount']"
	resultsNum = firefox_driver.find_element_by_xpath(tCountStr).text
	print "Total results: " + resultsNum

	# Set the top number of the items on the page to 0.
	topNum = 0

	# Data list. Will write to file later.
	data = []

	# If the search yeilded no results, send an email saying so.
	if int(resultsNum) == 0:
		sendEmail(email, data)
		return

	#Otherwise, copy the data and store it to the data list.
	while topNum != resultsNum and int(resultsNum) != 0:
		# Retrieve the top number of the items on page.
		rngPath = "//span[@class='rangeTo']"
		topNum = firefox_driver.find_element_by_xpath(rngPath).text
		print topNum

		scanEntries(firefox_driver, data)

		# Jump to next page.
		firefox_driver.implicitly_wait(5)
		nextPg = "//a[@class='button next']"
		if int(topNum) != int(resultsNum):
			nextPage = firefox_driver.find_element_by_xpath(nextPg)
			nextPage.click()

	# Write data to file.
	writeFile(data, rsltNm, curntDate)

	# Send user email with data
	sendEmail(email, data)

	# Wait and close driver.
	firefox_driver.implicitly_wait(5)
	firefox_driver.close()


# This function scans all the entries in a page an saves the relavent
#	data.
# @param firefox_driver, webdriver in the bot.
# @param data, the list of data from the search.
# @return returns nothing.
def scanEntries(firefox_driver, data):
	# Create a list of entries that have already been visited (store
	# data-pid number of each entry).
	visitedList = []
	# Get a list of all results on the page.
	entrStr = "result-row"
	priceStr = "result-price"
	entriesList = firefox_driver.find_elements_by_class_name(entrStr)
	for i in range(len(entriesList)):
		# Refresh entry list (every time the driver returns to the
		# search results page (current page)).
		newEntrLs = firefox_driver.find_elements_by_class_name(entrStr)
		# Entry prices (list).
		entrPrLs = firefox_driver.find_elements_by_class_name(priceStr)
		# Get price.
		price = str(entrPrLs[i].text)
		# Enter ad.
		newEntrLs[i].click()

		# Extract data from page.
		# Get current url.
		url = str(firefox_driver.current_url)
		# Get title.
		titleStr = "titletextonly"
		title = firefox_driver.find_element_by_id(titleStr).text.encode('utf-8')
		#prStr = "price"
		#price2 = str(firefox_driver.find_element_by_class_name(prStr))
		# OPTION 2: pull entire title string (requires parsing for
		# retrieving specific data).
		#pTTxt = "postingtitletext"
		#wTitle = firefox_driver.find_element_by_class_name(pTTxt).text.encode(utf-8)

		# Store data to tuple.
		#returnedData = (url, wTitle)
		returnedData = (url, title, price)

		#print returnedData

		# Store to the results file.
		data.append(returnedData)
		#data.append(url)

		# Return to results page.
		firefox_driver.back()
		#print i


# This function writes the data to file.
# @param data, the list of data from the search.
# @param resultsNames, the name of the results file.
# @param timestamp, the current time when the scan was done.
# @return returns nothing.
def writeFile(data, resultsName, timestamp):
	# Open file to store existing data to a list.
	readResults = open(resultsName, "r")
	lines = readResults.readlines()
	readResults.close()
	# Open file to append new data.
	writeResults = open(resultsName, "a")
	writeResults.write(timestamp + "\n")
	for item in data:
		# Format item to strings and write.
		itemLine = formatEntry(item)
		# Perform check to make sure items are not duplicate.
		# Duplicates will not be rewritten. Checks by title.
		if item[1] in lines:
			data.remove(item)
		else:
			# Write the item in the meantime.
			writeResults.write(itemLine)
	# Final newline for the entry. Close file.
	writeResults.write("\n")
	writeResults.close()


# Formats the tuple item from data list.
# @param item, the tuple stored in the data list.
# @return returns a string of the data stored in item, formated for
#	writing to the log file.
def formatEntry(item):
	url = item[0]
	title = item[1]
	price = item[2]
	retStr = price + "\n" + title + "\n" + url + "\n\n"
	print retStr
	return retStr


# This function sends the user an email with the most recent search
#	results.
# @param email, the email address of the user.
# @param data, the list of data from the search.
# @param server, the server object to send the email.
# @return returns nothing.
def sendEmail(email, data):
	# Create objects for sending email.
	# Make server object and store bot's user credentials.
	server = smtplib.SMTP('smtp.gmail.com', 587)
	un = "craigcarb1224@gmail.com"
	ps = "Xe3fentur87!!"
	# Connect to server.
	server.ehlo()
	server.starttls()
	server.ehlo()
	# Log into server.
	server.login(un, ps)
	# Return message.
	msg = ""
	# If the data list is empty, there was no new data to send.
	if len(data) == 0:
		msg = "Sorry, no results found this time."
	# Otherwise, send the data.
	else:
		# Iterate through the list and store items in a string.
		for item in data:
			msg += formatEntry(item)
	# Send email.
	server.sendmail(un, email, msg)
	# First argument is source, second is target recipient.

	# Exit server.
	server.quit()


if __name__ == '__main__':
	main()
