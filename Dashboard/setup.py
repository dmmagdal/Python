# setup.py
# author: Diego Magdaleno
# Simple script that sets up all files and directories for the program.
# Python 3.6
# Linux


import platform
import os
import sys


# Variable for the setup settings.
setting = None


def main():
	# Check command arguments.
	check1 = notValidArgs()
	setting = check1[1]
	if check1[0]:
		print("Useage: python setup.py <clean/debug>")
		exit(1)

	print("In "+str(setting)+" mode.")

	# Check python version and install dependencies.
	try:
		versionDependencies()
	except:
		print("Error: No Python 3 detected or dependencies failed to install.")
		print("Exiting setup.")
		exit(1)

	# Set up folders/files for logs.
	try:
		logSetup()
	except:
		print("Error: Setting up the folders and files for logs failed.")
		print("Exiting setup.")
		exit(1)

	# Set up folders/files for users.
	try:
		userSetup()
	except:
		print("Error: Setting up the folders and files for users failed.")
		print("Exiting setup.")
		exit(1)

	# Set up folders/files for markets.
	try:
		marketSetup()
	except:
		print("Error: No Python 3 detected or dependencies failed to install.")
		print("Exiting setup.")
		exit(1)

	# Set up folders/files for tickers.
	try:
		tickerSetup()
	except:
		print("Error: Setting up the folders and files for tickers failed.")
		print("Exiting setup.")
		exit(1)

	# All setup is completed. Exit program.
	print("Setup completed.")
	print("Welcome to Dashboard.")
	exit(0)


# Check to see if the command arguments are valid.
# @param: takes no arguments.
# @return: returns a tuple with a boolean on whether the command line
#	arguments are valid and what the current setting is.
def notValidArgs():
	# Load command line arguments to a variable
	args = sys.argv
	# Check the length of the command line arguments. If there are
	# actually optional arguments, check to see which ones they are.
	if len(args) == 2:
		# Make sure tha the option argument is either "debug" or
		# "clean".
		options = ["debug", "clean"]
		if args[1] not in options:
			#return True
			return (True, "")
		#setting = args[1]
		#return False
		return (False, args[1])
	# If there are more arguments than necessary, return false.
	elif len(args) > 2:
		#return True
		return (True, "")
	# Otherwise (there are no arguments), initiate "default" setup.
	else:
		#setting = "default"
		#return False
		return (False, "default")


if __name__ == '__main__':
	main()
