# p2pChat.py
# author: Diego Magdaleno
# Create a LAN peer to peer chat app in python3
# Python 3.6
# Linux

import socket
import subprocess
import sys


# Detect the user's operating system.
def detectOS():
	# Initialize blank string for OS.
	opSys = ""
	# Linux OS.
	if sys.platform == "linux" or sys.platform == "linux2":
		opSys = "Linux"
	# Windows OS.
	elif sys.platform == "win32":
		opSys = "Windows"
	# Mac OS.
	elif sys.platform == "darwin":
		opSys = "MacOS"
	# Return OS string.
	return opSys


# Run arp -a command on console. Return a list of available devices
# found.
def arp(opSys):
	# Create a file that holds the results of the arp -a search and
	# send the command to console (arp -a works on linux, Mac, & Win).
	arpfile = open("arpdata.txt", "w")
	subprocess.Popen("arp -a", stdout=arpfile).wait()
	arpfile.close()

	# Read info from file.
	datafile = open("arpdata.txt", "r")
	lines = datafile.readlines()

	# Print contents of file.
	for line in lines:
		print(line.strip("\n"))

	# Network devices in machine and their respective information/
	# statuses.
	netDevs = ipfconfig(opSys)

	# Split contents of lines by interface. arpdict holds the
	# interfaces and ip address info in a dictionary.
	arpdict = dict()
	interface = []
	ipaddresses = []
	for l in range(len(lines)):
		# Skip blank lines between interfaces.
		if len(lines[l]) == 1:
			continue
		# Load interface and ip address data into respective lists and
		# then load that information to the dictionary.
		elif "Interface:" in lines[l]:
			interface.append(lines[l])
			l += 2
			while l != len(lines) and len(lines[l]) != 1:
				line = lines[l].strip("\n")
				ipaddresses.append(line.split())
				l += 1
			arpdict[interface[-1]] = ipaddresses
			ipaddresses = []
	#print(arpdict)

	# Match Interface with network devices in the machine. 

	# Search and print only dynamic ip addresses. Static ip addresses
	# reserved for hardware by network administrator.
	print("\n\n")
	tupList = []
	dynamicIps = []
	for key in arpdict:
		tup = [key, []]
		for value in key:
			if value[2] == "dynamic":
				dynamicIps.append(value)
		tup[1] = dynamicIps
		dynamicIps = []
		tupList.append(tup)

	# Close file.
	datafile.close()
	
	# Delete file.
	subprocess.Popen("rm arpdata.txt").wait()

	# Create a list of active devices by returning the addresses of 
	# static ips that were pinged successfully.
	activeDevices = pingactivDevs(tupList, opSys)

	return activeDevices


# Run ip/fconfig on console. Return devices and their info found.
def ipfconfig(opSys):
	# Run ip/fconfig command depending on OS.
	configfile = open("config.txt", "w")
	if opSys == "Windows":
		subprocess.Popen("ipconfig", stdout=configfile).wait()
	else:
		subprocess.Popen("ifconfig", stdout=configfile).wait()
	configfile.close()

	# Parse data returned by command in file.
	configdatfile = open("config.txt", "r")
	lines = configdatfile.readlines()

	# Dev list is to hold the header info for network devices on the
	# machine. Vals list holds the body below the header, the lines
	# holding the info for each device. Devices is the full dictionary
	# that stores the network devices and their associated info. This
	# variabl is returned by the function.
	dev = []
	vals = []
	devices = dict()

	# Parse the config data file based on windows format.
	if opSys == "Windows":
		# Parse data for Windows.
		for l in range(3, len(lines)):
			line = lines[l].strip("\n")
			#print(lines[l].strip("\n"))
			# Skip if line is blank.
			if len(line) == 0:
				#print("blank line")
				continue
			# Get devices and their associated info.
			elif "adapter" in line:
				#print("in adapter")
				# Append device header as a key in the dictionary.
				dev.append(lines[l].strip(":\n"))
				# Increment counter by 2 to skip blank line between
				# header and its body.
				l += 2
				# Append body lines to a values list. Stops when
				# encounters a blank line or the end of the list.
				while l != len(lines) and len(lines[l]) != 1:
					#print(len(lines[l]))
					#print("appending to vals")
					vals.append(lines[l])
					l += 1

				# After all body content is accounted for, add header
				# and body to dictionary as key, value pairs. Clear the
				# values list.
				devices[dev[-1]] = vals
				vals = []

		#for k in devices:
		#	print(k)
		#	print(devices[k])

	# Parse the config data file based on linux/mac format.
	else:
		pass

	# Close file.
	configdatfile.close()

	# Delete flie.
	subprocess.Popen("rm config.txt").wait()

	# Return data retrieved from file.
	return devices


def pingactivDevs(dynamicIps, opSys):

	pass


def main():
	# Detect system's os.
	opSys = detectOS()
	print(opSys)

	# Retrieve ARP data.
	arpDat = arp(opSys)


if __name__ == '__main__':
	main()
