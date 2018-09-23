# setup.py
# author: Diego Magdaleno
# setup script for the rest of the aiden program. If specific
# requirements are not met, then the setup will stop and the program
# not be installed. This assumes python is already installed.
# Python 3.6 or 2.7
# Linux

import os

# Write to console the version requirements.
print("This program requires Python 3.6+ to run.")

# Check python version.
try:
	os.system("python3 -V >> pyVer.txt")
except:
	os.system("python -V >> pyVer.txt")

verFile = open("pyVer.txt", "r")
line = str(verFile.readline()).strip("\n\r")

ver = line.strip("Python ")[1]
nums = ver.split(".")
if nums[0] != 3 or nums[1] < 6:
	print("Python version must be 3.6 or above. Install halted.")
	exit(0)

verFile.close()

# Setup module installations.
modules = open("modules.txt", "r")
mNames = modules.readlines()
for name in mNames:
	nm = str(name).strip("\n\r")
	os.system("pip3 install " + nm)
modules.close()

# Setup is complete.
print("Setup complete. Aiden is ready to run.")
exit(0)