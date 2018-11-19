# p2pChat.py
# author: Diego Magdaleno
# Create a LAN peer to peer chat app in python3
# Python 3.6
# Linux

import socket
import os
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


# Run arp -a command on console.
def arp():
	os.system("arp -a > arpdata.txt")
	datafile = open("arpdata.txt", "r")
	lines = datafile.readlines()
	for line in lines:
		#print(line.split("\n")[0])
		if "dynamic" in line:
			print(line.split("\n")[0])
	datafile.close()

def main():
	# Detect system's os.
	opSys = detectOS()
	print(opSys)

	# Retrieve ARP data.
	arpDat = arp()
	
	pass


if __name__ == '__main__':
	main()
