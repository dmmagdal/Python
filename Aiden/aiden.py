# adien.py
# This is a voice activate desktop assistant capable of running quick
# web searches and activating apps.
# python 3.6.5
# windows 10

import keyboard as kb
import speech_recognition as sr
import sys
import os
import ctypes
import gtts as gTTS
import pyttsx3
import random
import geocoder
from datetime import datetime
from tkinter import *
from tkinter.messagebox import *
from time import sleep
from urllib.request import urlopen


def main():
	# If the program was already setup, skip it.
	#print(progSetup())
	if not progSetup():
		print("Setting up the config file.")
		setupConfigs()

	# Detect if the computer is online or offline as well as set the
	# voice recogEngine variable.
	online = False
	vRecogEng = "Sphinx"
	if connected2Internet():
		print("Connected to the Internet")
		online = True
	else:
		print("Not connected to Internet")
	#exit(0)

	# If there is internet connection, use Google's voice recognition
	# engine.
	if online == True:
		vRecogEng = "Google"
	# Otherwise, use CMU Sphinx engine.
	#print(vRecogEng)
	#exit(0)

	# Initialize the text to speach engine (Default is used, windows
	# default is David male).
	engine = pyttsx3.init()

	# Say a greeting after booting on.
	greeting = randSelectGr()
	engine.say(greeting)
	randNum = random.randint(1, 10)
	if online and randNum%2 == 0:
		engine.say("I'm online and ready.")
	elif not online:
		engine.say("I have no internet connection at the moment.")
	engine.runAndWait()
	exit(0)

	# Determine pronoun.
	pronoun = "sir"
	configFile = open("configFile.txt", "r")
	cfgLines = configFile.readlines()
	for line in cfgLines:
		if "female" in line:
			pronoun = "ma'am"
	configFile.close()

	# Retrieve user location.
	geo = geocoder.ip('me')
	city = geo.city
	state = geo.state
	country = geo.country

	# Listen for commands.
	r = sr.Recognizer()
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		print("say something")
		audio = r.listen(source)

	# Set speech recognition engine.
	if vRecogEng == "Sphinx":
		try:
			print("Sphinx thinks you said " + r.recognize_sphinx(audio))
		except sr.UnknownValueError:
			print("Sphinx could not understand audio")
		except sr.RequestError as e:
			print("Sphinx error; {0}".format(e))
	elif vRecogEng == "Google":
		try:
			print("Google speech recognition thinks you said " + r.recognize_google(audio))
		except sr.UnknownValueError:
			print("Google speech recognition could not understand audio")
		except sr.RequestError as e:
			print("Could not request results from Google speech recognition service; {0}".format(e))

	'''
	try:
		print("Sphinx thinks you said " + r.recognize_sphinx(audio))
	except sr.UnknownValueError:
		print("Sphinx could not understand audio")
	except sr.RequestError as e:
		print("Sphinx error; {0}".format(e))
	'''

	'''
	# Requires Internet access but is more accurate than CMU Sphinx
	# engine.
	try:
		print("Google speech recognition thinks you said " + r.recognize_google(audio))
	except sr.UnknownValueError:
		print("Google speech recognition could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Google speech recognition service; {0}".format(e))
	'''

	#run a search
	searchArgs = ""


# Check for the existance of a setup configuration file. If it does
# exist, then return True, otherwise return False.
# @param takes no arguments.
# @return returns a boolean with the status of whether the setupconfig
# file currently exists. 
def progSetup():
	filepath = os.getcwd()
	if sys.platform == 'win32':
		filepath += '//configFile.txt'
	else:
		filepath += '/configFile.txt'
	return os.path.isfile(filepath)


# Set up the config file that is created upon the first run of the
# program.
# @param takes no arguments.
# @return returns nothing.
def setupConfigs():
	titleFont = ("Helvetica", 14)
	regfont = ("Helvetica", 12)
	smfont = ("Helvetica", 8)

	# Create a form application for the user to fill out necessary data
	# for the program to run.
	setupFm = Tk()
	setupFm.geometry("500x500")
	setupLbl = Label(setupFm, text="Please fill out the form below.",
					 font=titleFont)
	setupLbl.place(x=100, y=10)

	fNameLbl = Label(setupFm, text="First name: ", font=regfont)
	fNameLbl.place(x=75, y=55)
	fNmEntr = Entry(setupFm)
	fNmEntr.place(x=165, y=57)

	lNameLbl = Label(setupFm, text="Last name: ", font=regfont)
	lNameLbl.place(x=75, y=95)
	lNmEntr = Entry(setupFm)
	lNmEntr.place(x=165, y=97)

	genderLbl = Label(setupFm, text="Gender: ", font=regfont)
	genderLbl.place(x=75, y=165)
	gvar = StringVar()
	gvar.set("male")
	maleChkBtn = Radiobutton(setupFm, text="male", variable=gvar,
							 value="male")
	maleChkBtn.place(x=150, y=167)
	femaleChkBtn = Radiobutton(setupFm, text="female", variable=gvar,
								value="female")
	femaleChkBtn.place(x=250, y=167)

	emailLbl = Label(setupFm, text="Email: ", font=regfont)
	emailLbl.place(x=75, y=230)
	emEtr = Entry(setupFm)
	emEtr.place(x=165, y=232)
	epwdLbl = Label(setupFm, text="Password: ", font=regfont)
	epwdLbl.place(x=75, y=270)
	pwdEtr = Entry(setupFm, show="*")
	pwdEtr.place(x=165, y=272)
	epwdLblSm = Label(setupFm, text="For your email", font=smfont)
	epwdLblSm.place(x=165, y=290)

	saveBtn = Button(setupFm, text="Save", 
					 command=(lambda: writeConf(setupFm, fNmEntr.get(),
												lNmEntr.get(),
												gvar.get(),
												emEtr.get(),
												pwdEtr.get())))
	saveBtn.place(x=230, y=325)

	setupFm.mainloop()


# Write to the setupConfig file.
# @param form, the submittion form to configure the user on setup.
# @param firstN, the user's first name.
# @param lastN, the user's last name.
# @param gender, the user's gender.
# @param email, the user's email address.
# @param password, the user's password for their email address.
# @return returns nothing.
def writeConf(form, firstN, lastN, gender, email, password):
	# Check to make sure all fields are filled out.
	emptyStr = ""
	entries = [firstN, lastN, email, password]
	if emptyStr in entries:
		#print(entries)
		#print("In the error")
		errorMsg = "Please fill out all entry boxes."
		showerror("Error", errorMsg)
		return

	# Open/create config file.
	configFile = open("configFile.txt", "w+")
	# Write entries to file.
	configFile.write("Name: " + str(firstN) + " " + str(lastN) + "\n")
	configFile.write("Gender: " + str(gender) + "\n")
	configFile.write("Email: " + str(email) + "\n")
	configFile.write("Password: " + str(password) + "\n")
	configFile.write("\n")

	# Get OS details and writing to the config file.
	platforms = {
		'linux1' : 'Linux',
		'linux2' : 'Linux',
		'darwin' : 'OS X',
		'win32' : 'Windows'
	}
	if sys.platform not in platforms:
		configFile.write("OS not recognized.\n")
	else:
		configFile.write("OS: " + str(platforms[sys.platform]) + "\n")

	#configFile.write("Phone: " + str(phone))
	# Close config file.
	configFile.close()
	# Close the setup form.
	form.destroy()


# Return a boolean to see if the program is connected to the internet.
# @param takes no arguments.
# @return returns a boolean with the status of whether the program has
# internet access or not.
def connected2Internet():
	# If the program can open this simple webpage, then there is
	# internet access, otherwise return false.
	try:
		urlopen("https://www.google.com", timeout=10)
		return True
	except:
		return False


# Randomly select a greeting from the greetings file.
# @param takes no arguments.
# @return returns a string greeting.
def randSelectGr():
	# Open the greetings file and load its contents to a list.
	grFile = open("greetings.txt", "r")
	lines = grFile.readlines()
	# Close the file and return the random choice.
	greeting = random.choice(lines)
	while not appropriateTime(greeting):
		greeting = random.choice(lines)
	return greeting

# Determine if a greeting is appropriate giving the time.
# @param greeting, greeting string.
# @return returns a boolean determining if a greeting is appropriately
# timed.
def appropriateTime(greeting):
	# Check the greeting string. If it's one of the three below, check
	# the time and see if the greeting matches the time.
	timedGr = ["Good morning.", "Good evening.", "Good afternoon."]
	curTime = str(datetime.now())
	hour = int(curTime.split(" ")[1].split(":")[0])
	if timedGr[0] == greeting and hour < 12:
		return True
	elif timedGr[1] == greeting and hour >= 12 and hour < 17:
		return True
	elif timedGr[2] == greeting and hour >= 17:
		return True
	elif greeting in timedGr:
		return False
	return True


# Change windows. Works like "alt tab".
# @param takes no arugments.
# @return returns nothing.
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