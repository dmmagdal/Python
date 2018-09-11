# craigCarBot.py
# author: Diego Magdaleno
# Craigslist bot that searches for cars desired by the user. Program
# only takes one or more users at a time but only takes one car search
# at a time (This can be changed later).
# Python 2.7
# Linux

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from Tkinter import *
from tkMessageBox import *
from datetime import date
import datetime
import calendar

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

	#yearRange = yearRangeTxtBox1.get() + " " + yearRangeTxtBox2.get()
	#print yearRange

	# Start bot/search.
	searchBtn = Button(m, text="Start", 
					   command=(lambda: searchCar(m,
					   							  makeTxtBox.get(),
					   							  modelTxtBox.get(),
					   							  yearRngTxtBox1.get(),
					   							  yearRngTxtBox2.get(),
					   							  emailTxtBx.get())))
	searchBtn.place(x=125, y=225)

	m.mainloop()


def searchCar(m, make, model, yearRange1, yearRange2, email):
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

	'''
	# Check time.
	print date.today()
	my_date = date.today()
	day_of_week = calendar.day_name[my_date.weekday()]
	print day_of_week
	time_of_day = datetime.datetime.now().strftime("%H:%M:%S")
	print time_of_day
	'''

	# Unblock when finished.
	'''
	# Infinite loop to cosntantly check the time.
	while True:
		#print date.today()
		my_date = date.today()
		day_of_week = calendar.day_name[my_date.weekday()]
		#print day_of_week
		time_of_day = datetime.datetime.now().strftime("%H:%M:%S")
		#print time_of_day

		# Run search M-W-F at noon.
		day1 = day_of_week == "Monday"
		day2 = day_of_week == "Wedensday"
		day3 = day_of_week === "Friday"
		dayCondition = day1 or day2 or day3
		if dayCondition and time_of_day == "12:00:00":
			# Create webdriver object (run in headless).
			firefox_options = Options()
			#firefox_options.add_argument('--headless')
			#firefox_options.add_argument('--window-size=1920x1080')
			firefox_driver = webdriver.Firefox(firefox_options=firefox_options)

			# Interact with webpage.
			firefox_driver.get("https://sfbay.craigslist.org/")
			searchBox = firefox_driver.find_element_by_id("query")

			#print yearRange

			# Run the seach in craigslist.
			querystring = newYearRange + " " + make + " " + model
			searchBox.click()
			searchBox.send_keys(querystring)
			searchBox.send_keys(Keys.ENTER)

			firefox_driver.pause(30)
			firefox_driver.close()
	'''

	# Create webdriver object (run in headless).
	firefox_options = Options()
	#firefox_options.add_argument('--headless')
	#firefox_options.add_argument('--window-size=1920x1080')
	firefox_driver = webdriver.Firefox(firefox_options=firefox_options)

	# Interact with webpage.
	firefox_driver.get("https://sfbay.craigslist.org/")
	searchBox = firefox_driver.find_element_by_id("query")

	#print yearRange

	# Run the seach in craigslist.
	querystring = newYearRange + " " + make + " " + model
	searchBox.click()
	searchBox.send_keys(querystring)
	searchBox.send_keys(Keys.ENTER)

	firefox_driver.implicitly_wait(5)

	# Retrieve total number of results.
	resultsNum = firefox_driver.find_element_by_xpath("//span[@class='totalcount']").text
	print resultsNum

	# Set the top number of the items on the page to 0.
	topNum = 0

	# Data list. Will write to file later.
	data = []

	# Iterate through the posts in a page.
	index = 0
	while topNum != resultsNum and int(resultsNum) != 0:
		# Retrieve the top number of the items on page.
		topNum = firefox_driver.find_element_by_xpath("//span[@class='rangeTo']").text
		print topNum
		#for entry in int(pageNum):

		'''
		# Get all entries on page.
		entries = firefox_driver.find_elements_by_class_name("result-row")
		print "length of entries: " + str(len(entries))
		visitedList = []
		'''
		'''
		for e in entries:
			firefox_driver.implicitly_wait(15)
			if e.get_property("data-pid") in visitedList:
				continue
			visitedList.append(e.get_property("data-pid"))
			e.click()

			
			# Click the the ad entry.
			#		hyperLink = firefox_driver.find_element_by_xpath("//a[@class='result-image gallery']")
			#		hyperLink.click()
			# Now in the ad, store data.
			# Data:url, title, body, pic, map address.
			

			# Get current url
			url = firefox_driver.current_url

			# Append data to list and write.
			data.append(url)

			# Go back to search page.
			firefox_driver.back()
			#print hyperLink
		'''

		scanEntries(firefox_driver, data)
		break

		#print type(pageNum)
		pass

	# Store current date.
	#timestamp = 

	# Write data to file.
	#writeFile(data, resultsName, timestamp)

	# Send user email with data
	#sendEmail(email, data)

	# Wait and close driver.
	firefox_driver.implicitly_wait(120)
	firefox_driver.close()


# This function scans all the entries in a page an saves the relavent
#	data.
# @param firefox_driver, webdriver in the bot.
# @return returns nothing.
def scanEntries(firefox_driver, data):
	# Create a list of entries that have already been visited (store
	# data-pid number of each entry).
	visitedList = []
	# Get a list of all results on the page.
	entriesList = firefox_driver.find_elements_by_class_name("result-row")
	for i in range(len(entriesList)):
		# Refresh entry list (every time the driver returns to the
		# search results page (current page)).
		newEntriesList = firefox_driver.find_elements_by_class_name("result-row")
		# Enter ad.
		newEntriesList[i].click()

		# Extract data from page.
		# Get current url.
		url = firefox_driver.current_url
		# Get title.
		#title = firefox_driver.find_element_by_id("titletextonly")
		# Get body.
		#body = firefox_driver.find_element_by_id("postingbody")
		# Store data to tuple.
		#returnedData = (url, title, body)

		# Store to the results file.
		#data.append(returnedData)
		data.append(url)

		# Return to results page.
		firefox_driver.back()


# This function writes the data to file.
# @param data,
# @param resultsNames,
# @param date,
# @return returns nothing.
def writeFile(data, resultsName, timestamp):
	# Open file.
	writeResults = open(resultsName, "a")
	writeResults.Write(date + "\n")
	for item in data:
		# TODO: Format item to strings and write.

		# TODO: Perform check to make sure items are not duplicate.

		# Write the item in the meantime.
		writeResults.write(item)
	# Final newline for the entry. Close file.
	writeResults.write("\n")
	writeResults.close()


# This function sends the user an email with the most recent search
#	results.
# @param
# @param
# @return returns nothing.
def sendEmail(email, data):
	pass


if __name__ == '__main__':
	main()
