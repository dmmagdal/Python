# setup.py
# author: Diego Magdaleno
# Program that sets up the Python 3 environment for a user.
# Python 3.7
# Windows/MacOS/Linux


import os
import subprocess


def main():
	# Check for the requirements.txt file.
	if not os.path.exists("requirements.txt"):
		print("Error: Requirements file requirements.txt is not found.")
		exit(1)

	# Install all modules from requirements.txt
	command = subprocess.Popen("pip install -r requirements.txt", shell=True,
								stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	command_output, command_error = command.communicate()
	
	# Print the output of the command. If there was any error from the
	# installation process, print that out as well.
	print(command_output.decode("utf-8"))
	if command_error:
		print("Error: ")
		print(command_error.decode("utf-8"))
		exit(1)

	# Exit the program.
	exit(0)



if __name__ == '__main__':
	main()