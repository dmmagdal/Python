# netsetup.py
# author: Diego Magdaleno
# Part of the Wrench2 library, this program runs on the raspberry pi
# and checks the network status of the machine. The machine will
# already try to sign into the most open wifi, but if this is a school
# network, it checks to make sure that the certificate is signed in or
# not before sending out the ip address.
# Python 3.6
# Linux

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

def main():
	# Create webdriver object (run in headless).
	# firefox_options = Options()
	# firefox_options.add_argument('--headless')
	# firefox_options.add_argument('--window-size=1920x1080')
	# firefox_driver = webdriver.Firefox(firefox_options=firefox_options)

	# Initialize Chrome selenium web driver.
	chromeOpts = Options()
	# chromeOpts.add_argument('--headless')
	chromeOpts.add_argument('--incognito')
	chromeOpts.add_argument('--window-size=1920x1080')
	chrome_driver = webdriver.Chrome(options=chromeOpts)

	# Check the connectivity on wifi
	# Interact with webpage.
	url = "https://resreg.ucsc.edu:9443/clientStatus.!%5E"
	url2 = "https://www.ucsc.edu/"
	# firefox_driver.get(url)
	chrome_driver.get(url)

	# If the page is not redirected to the ucsc site.
	# if firefox_driver.currenturl() != url2:
	# 	# Open file with login crentials.
	# 	login = open("credentials.txt", 'r')
	# 	lines = login.readlines()
	# 	username = lines[0].split("\r\n")[0]
	# 	password = lines[1].split("\r\n")[0]
	# 	login.close()
	# 	# Use login credentials on webpage.
	# 	idbox = firefox_driver.find_element_by_id("")
	# 	idbox.click()
	# 	idbox.send_keys(username)
	# 	pwdbox = firefox_driver.find_element_by_id("")
	# 	pwdbox.click()
	# 	pwdbox.send_keys(password)
	# 	checkbutton = firefox_driver.find_element_by_id("")
	# 	checkbutton.click()
	# 	enterbutton = firefox_driver.find_element_by_id("")
	# 	enterbutton.click()
	if chrome_driver.currenturl() != url2:
		# Open file with login crentials.
		login = open("credentials.txt", 'r')
		lines = login.readlines()
		username = lines[0].split("\r\n")[0]
		password = lines[1].split("\r\n")[0]
		login.close()
		# Use login credentials on webpage.
		idbox = chrome_driver.find_element_by_id("")
		idbox.click()
		idbox.send_keys(username)
		pwdbox = chrome_driver.find_element_by_id("")
		pwdbox.click()
		pwdbox.send_keys(password)
		checkbutton = chrome_driver.find_element_by_id("")
		checkbutton.click()
		enterbutton = chrome_driver.find_element_by_id("")
		enterbutton.click()

	# Close the webdriver, the wifi is setup.
	# firefox_driver.close()
	chrome_driver.close()

	## Send out the ip address.
	#os.system("ifconfig > network.txt")

	print("Wifi configured.")


if __name__ == '__main__':
	main()
