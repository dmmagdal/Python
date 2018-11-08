# facebooktest.py

import time
import facebook
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def getToken():
	# User's log in credentials.
	email = sys.argv[1]
	password = sys.argv[2]

	# Chrome webdriver object.
	chromeOpts = Options()
	chromeOpts.add_argument('--headless')
	chromeOpts.add_argument('--incognito')
	chromeOpts.add_argument('--window-size=1920x1080')
	chrome_driver = webdriver.Chrome(options=chromeOpts)

	# Access developer's website.
	url1 = "https://developers.facebook.com"
	chrome_driver.get(url1)

	# Click log in button.
	searchStr1 = "//div[@class='_3x57 _6e3y']"
	logIn = chrome_driver.find_element_by_xpath(searchStr1)
	logIn.click()

	# Log into facebook.
	emailBox = chrome_driver.find_element_by_id("email")
	emailBox.click()
	emailBox.send_keys(email)
	passwordBox = chrome_driver.find_element_by_id("pass")
	passwordBox.click()
	passwordBox.send_keys(password)
	passwordBox.send_keys(Keys.ENTER)

	# Jump to the this page to get user access token.
	url2 = "https://developers.facebook.com/tools/accesstoken/"
	chrome_driver.get(url2)

	# Extract user access token string from element and save it.
	searchStr2 = "//div[@class='lfloat _ohe']"
	token = chrome_driver.find_element_by_xpath(searchStr2).text

	# Close chrome web driver.
	chrome_driver.close()

	# Return access token.
	return str(token)


def main():
	# Check if there are appropriate number of arguments.
	if len(sys.argv) != 3:
		print("Usage: python facebooktest.py <username> <password>")
		exit(1)

	# Get user access token.
	token = getToken()

	# Load graph api given token.
	graph = facebook.GraphAPI(access_token=token)

	# Get user data from facebook (you).
	post = graph.get_object(id='me', fields='name')
	print(post)
	post2 = graph.get_object(id='me', fields='friends')
	print(post2['friends'])
	#post3 = graph.get_object(id='me', fields='friendlists')
	#print(post3)
	post3 = graph.get_connections(id='me', connection_name='friends')
	print(post3)
	#print(len(post3['data']))
	for k in post3['data']:
		print(k)
	post4 = graph.get_all_connections(id='me', connection_name='friends')
	print(post4)
	post5 = graph.get_all_connections(id='me', connection_name='groups')
	print(post5)

if __name__ == '__main__':
	main()
