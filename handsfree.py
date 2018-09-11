# handsfree.py
# Uses voice commands to navigate webpages and between open applications on a desktop

import keyboard as kb
import speech_recognition as sr
import selenium
import ctypes
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os


def main():
	#changeWin()
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("say something")
		audio = r.listen(source)

	try:
		print("Sphinx thinks you said " + r.recognize_sphinx(audio))
	except sr.UnknownValueError:
		print("Sphinx could not understand audio")
	except sr.RequestError as e:
		print("Sphinx error; {0}".format(e))

	#run a search
	searchArgs = ""
	

	'''
	try:
		print("Google speech recognition thinks you said " + r.recognize_google(audio))
	except sr.UnknownValueError:
		print("Google speech recognition could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Google speech recognition service; {0}".format(e))
	'''


def changeWin():
	# alt-tab
	'''
	if os.name == "nt":
		user32 = ctypes.windll.user32
		user32.keybd_event(0x12, 0, 0, 0) # Alt
		sleep(0.1)
		user32.keybd_event(0x09, 0, 0, 0) # Tab
		sleep(0.1)
		user32.keybd_event(0x09, 0, 2, 0) # ~Tab
		sleep(0.1)
		user32.keybd_event(0x12, 0, 2, 0) # ~Alt
	elif os.name == "posix":
		cll = ctypes.cdll.
	'''
	'''
	for i in range(0, 3):
		kb.press("alt+tab")
		sleep(0.1)
		kb.release("alt+tab")
	'''
	kb.press("alt+tab")
	sleep(0.1)
	kb.release("alt+tab")


def openBrowser(searchArgs, headStat=None):
	chrome_options = None
	# If the headless status is not "None", then open the browser out
	# of headless
	if headStat != None:
		# Set the Chrome options for headless.
		chrome_options = Options()
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--window-size=1920x1080")

	# Create new selenium webdriver (Chrome).
	chrDriver = webdriver.Chrome(chrome_options=chrome_options)
	chrDriver.get("https://www.google.com/")

	# Run a search in chrome.
	searchElem = chrDriver.find_element_by_id("lst-1b")
	searchElem.click()
	searchElem.send_keys(searchArgs)
	searchElem.send_keys(Keys.ENTER)
	return chrDriver


if __name__ == '__main__':
	main()