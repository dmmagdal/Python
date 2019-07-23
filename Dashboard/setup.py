# setup.py
# author: Diego Magdaleno
# Simple script that sets up all files and directories for the program.
# Python 3.6
# Linux


import platform
import os
import sys
import subprocess
import cryptography
from cryptography.fernet import Fernet
from getpass import getpass


# Variable for the setup settings.
setting = None


def main():
	# Get the Host OS.
	# Windows = Windows
	# Mac = Darwin
	# Linux = Linux
	opSys = platform.system()

	# Check command arguments.
	check1 = notValidArgs()
	setting = check1[1]
	if check1[0]:
		print("Useage: python setup.py <clean>")
		exit(1)

	#print("In "+str(setting)+" mode.")

	# Check python version and install dependencies.
	try:
		versionDependencies()
		print("")
	except:
		print("Error: No Python 3 detected or dependencies failed to install.")
		print("Exiting setup.")
		exit(1)

	# Set up folders/files for logs.
	try:
		logSetup(opSys, setting)
	except:
		print("Error: Setting up the folders and files for logs failed.")
		print("Exiting setup.")
		exit(1)

	# Set up folders/files for users.
	try:
		userSetup(opSys, setting)
	except:
		print("Error: Setting up the folders and files for users failed.")
		print("Exiting setup.")
		exit(1)

	# Set up folders/files for markets.
	try:
		marketSetup(opSys, setting)
	except:
		print("Error: Setting up the folders and files for markets failed.")
		print("Exiting setup.")
		exit(1)

	# Set up folders/files for tickers.
	try:
		tickerSetup(opSys, setting)
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
		options = "clean"
		if args[1] != options:
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


# Detect python version and acquire all dependencies. Raises an
# exception if something goes wrong.
# @param: takes no arguments.
# @return: returns nothing.
def versionDependencies():
	# Get the version of python.
	pyVersion = sys.version.split(" ")
	#print(pyVersion)
	# If the version is not python 3 of some kind, raise an exception.
	if pyVersion[0][0] != "3":
		raise Exception("Incompatible python version.")
	# Install all dependencies from the requirements document.
	moduleReqs = open("requirements.txt", "r")
	modules = moduleReqs.readlines()
	moduleReqs.close()
	for module in modules:
		try:
			subprocess.run("pip install "+module.strip("\n"))
		except:
			try:
				subprocess.run("pip3 install "+module.strip("\n"))
			except:
				raise Exception("pip not installed or module not found.")
	# At this point, all python 3 modules are installed and we're ready
	# to proceed with the rest of the setup.
	return


# Set up the paths and files. Raises an exception if something goes
# wrong.
# @param: opSys, the string detailing the host OS.
# @param: setting, the string detailing the current setting for the
#	setup program.
# @return: returns nothing.
def logSetup(opSys, setting):
	# Format slashes.
	slash = "/"
	if opSys == "Windows":
		slash = "\\"
	# Check to see if the directory and subdirectories exist. If they
	# don't, create them.
	logDir1 = "."+slash+"Logs"+slash+"CBOE"
	logDir2 = "."+slash+"Logs"+slash+"NYSE"
	logDir3 = "."+slash+"Logs"+slash+"NASDAQ"
	# Running check on first directory path.
	if not os.path.exists(logDir1):
		os.path.mkdir(logDir1)
	elif not os.path.isdir(logDir1):
		os.remove(logDir1)
		os.path.mkdir(logDir1)
	# Running check on first directory path.
	if not os.path.exists(logDir2):
		os.path.mkdir(logDir2)
	elif not os.path.isdir(logDir2):
		os.remove(logDir2)
		os.path.mkdir(logDir2)
	# Running check on first directory path.
	if not os.path.exists(logDir3):
		os.path.mkdir(logDir3)
	elif not os.path.isdir(logDir3):
		os.remove(logDir3)
		os.path.mkdir(logDir3)
	# If the setting is "clean", make sure all directories and
	# subdirectories are empty of files.
	if setting == "clean":
		# Remove files in "./Logs/CBOE".
		for file1 in os.listdir(logDir1):
			if os.path.isfile(logDir1+slash+file1):
				os.remove(logDir1+slash+file1)
		# Remove files in "./Logs/NYSE".
		for file2 in os.listdir(logDir2):
			if os.path.isfile(logDir2+slash+file2):
				os.remove(logDir2+slash+file2)
		# Remove files in "./Logs/NASDAQ".
		for file3 in os.listdir(logDir3):
			if os.path.isfile(logDir3+slash+file3):
				os.remove(logDir3+slash+file3)
		# Remove files in "./Logs".
		for fileS in os.listdir("."+slash+"Logs"):
			if os.path.isfile("."+slash+"Logs"+slash+fileS):
				os.remove("."+slash+"Logs"+slash+fileS)
	# By now, all necessary log directories and files are available and
	# ready.
	return


# Set up the users folder and admin/default accounts (if necessary).
# Raises an exception if something goes wrong.
# @param: opSys, the string detailing the host OS.
# @param: setting, the string detailing the current setting for the
#	setup program.
# @return: returns nothing.
def userSetup(opSys, setting):
	# Format slashes.
	slash = "/"
	if opSys == "Windows":
		slash = "\\"
	# Check to see if the directory and subdirectories exist. If they
	# don't, create them.
	userDir = "."+slash+"Users"
	if not os.path.exists(userDir):
		os.path.mkdir(userDir)
	elif not os.path.isdir(userDir):
		os.remove(userDir)
		os.path.mkdir(userDir)
	# Depending on the setting, we'll create the administrator/default
	# account a certain way.
	print("Setting up administrator/default account.")
	# Set the key for the encryption function blank for now. This will
	# be set later on in the method depending on the options chosen by
	# the user.
	key = ""
	# If the setting is "clean", make sure there are no subfolders and
	# old encryption key files.
	if setting == "clean":
		cleanDir(opSys, userDir)
	# Otherwise, in "default" mode, the user can either enter their
	# credentials for a new admin account or ignore it and continue on.
	elif setting == "default":
		keyExists = keyExist(opSys, userDir)
		adminExists = adminExist(opSys, userDir)
		if len(os.listdir(userDir)) > 0 and keyExists and adminExists:
			print("There already exists a dek and account(s).")
			resp = input("Do you wish to add a new account? [y/n]")
			bothyn = "y" in resp and "n" in resp
			neitheryn = not "y" in resp and not "n" in resp
			while bothyn or neitheryn:
				resp = input("Do you wish to add a new account? [y/n]")
			# If the user didn't want to add a new account, then exit
			# the method/return.
			if "n" in resp:
				return
			# Otherwise, the user wants to create a new admin profile
			# (continue on down below).
		else:
			# This condition runs if either the dek file is missing,
			# there are no account profiles, or there is nothing in the
			# directory. In all of these cases, the "./Users" folder is
			# cleaned like it would be in setting = "clean" and the
			# user must create a new profile and a new key will be
			# generated.
			print("Error: There is either a missing dek or admin account.")
			print("Attempting to resolve by cleaning directory.")
			cleanDir(opSys, userDir)
			print("Directory cleaned. \nRecovery successful.")
			print("Proceeding with administrator setup.")
	# Credendials to admin profile set up by the user.
	adminUser = input("Enter your desired username: ")
	adminPassword = getpass("Enter your desired password: ")
	adminPasswordReEnter = getpass("Re-Enter your password: ")
	# Check that the passwords entered match.
	while adminPassword != adminPasswordReEnter:
		print("Error: Passwords you entered do not match.\n")
		adminPassword = getpass("Enter your desired password: ")
		adminPasswordReEnter = getpass("Re-Enter your password: ")
	email = input("Enter your desired email: ")
	# Mild check that some sort of email was entered.
	while "@" not in email:
		print("Error: Please enter a valid email.\n")
		email = input("Enter your desired email: ")
	# Credentials are set. Time to encrypt the user profile and set up
	# their folders. The string encrypted is in the following format:
	# user[+admin]+email+password.
	adminUserString = adminUser+" admin "+email+" "+adminPassword
	# Depeding on the setting, either generate a new key or use the old
	# one.
	if setting = "clean" or not keyExists(opSys, userDir):
		# Generate a new encryption key for all accounts.
		key = Fernet.generate_key()
	else:
		# Find and open the dek to retrieve the encryption key.
		keyFile = open(userDir+slash+"dek.key", 'rb')
		key = keyFile.read()
		keyFile.close()
	# Encode the user string.
	adminUserBytes = adminUserString.encode()
	# Create an encryption function based on the key.
	encryptFunc = Fernet(key)
	# Encrypt the byte data given the encryption function.
	encryptedUser = encryptFunc.encrypt(adminUserBytes)
	# Create a 


# This recursive function takes the path of a folder and cleans out its
# contents as well as deletes its subdirectories and their contents.
# @param: opSys, the string detailing the host OS.
# @param: path, the string containing the path of the target directory
#	we want to empty.
# @return: returns nothing.
def cleanDir(opSys, path):
	# Format slashes.
	slash = "/"
	if opSys == "Windows":
		slash = "\\"
	# For every item in the current directory "./path"
	for obj in os.listdir(path):
		# Removes files in immediate folder "./path".
		if os.path.isfile(path+slash+obj):
			os.remove(path+slash+obj)
		# Removes subdirectories (users) from immediate folder
		# "./path" and deletes their contents.
		elif os.path.isdir(path+slash+obj):
			# Recursively call the function on the subdirectory 
			#"./path/obj". This will return quickly if the subdirectory
			# is empty or only contains files. Then remove the
			# subdirectory since it's empty.
			cleanDir(opSys, path+slash+obj)
			os.remove(path+slash+obj)

# Check to see if the dek (key) file for users exists. Doesn't require
# any (admin) profiles to exist.
# @param: opSys, the string detailing the host OS.
# @param: path, the string containing the path of the Users directory.
# @return: returns a boolean on whether the desired file exists or not.
def keyExist(opSys, path):
	# Format slashes.
	slash = "/"
	if opSys == "Windows":
		slash = "\\"
	# Check to see if the specified file exists. Return the boolean.
	return os.path.exists(path+slash+"dek.key")


# Check to see if any admin profiles exist. Requires the dek file to
# exist too.
# @param: path, the string containing the path of the Users directory.
# @return: returns a boolean on whether the a user exists or not.
def adminExist(opSys, path):
	# Format slashes.
	slash = "/"
	if opSys == "Windows":
		slash = "\\"
	# Get the dek.
	keyFile = open("dek.key", "rb")
	lines = keyFile.readlines()
	keyFile.close()
	# Get the names of all subdirectories in "./Users".
	users = [fold for fold in os.listdir(path) if os.path.isdir(path+slash+fold)]
	# Decrypt all userstring keys


	# Check to see if the following log files are created yet. If not,
	# then initialize them to be blank.


if __name__ == '__main__':
	main()
