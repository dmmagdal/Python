# p2pChat0-2.py
# author: Diego Magdaleno
# Create a LAN peer to peer chat app in python3
# Changes: Beginning frame for client server model.
#		   Created first (Log in) page in GUI. Displays user's network
#				info.
#		   Cleaned up unused code.
# Python 3.6
# Linux

import socket
import subprocess
import sys
import socket
from threading import Thread
import tkinter as tk


class Server(object):
	ipList = []
	chatLog = []
	port = 33000
	hostIP = ""

	def __init__(self, port, hostIP):
		self.port = port
		self.hostIP = holds


	def __init__(self, port, hostIP, ipList, chatLog):
		self.port = port
		self.hostIP = holds
		self.ipList = ipList
		self.chatLog = chatLog


	def mainloop():
		pass

	def acceptConnections():
		pass


	def handleClient(client):
		pass

	def broadcast():
		pass



class Client(object):
	port = 33000
	hostIP = ""

	def __init__(self, port, hostIP):
		self.port = port
		self.hostIP = holds
		

	def send():
		pass

	def recieve():
		pass

	def mainloop():
		pass



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
# found. (Only lists devices found on subnet associated with user's ip
# address).	
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
			interface.append(lines[l].strip("\n"))
			l += 2
			while l != len(lines) and len(lines[l]) != 1:
				line = lines[l].strip("\n")
				ipaddresses.append(line.split())
				l += 1
			arpdict[interface[-1]] = ipaddresses
			ipaddresses = []
	#print(arpdict)

	# Count number of dynamic adresses in an interface. The one with
	# the most is selected by default.
	interfaceName = ""
	maxNumOfDynamics = 0
	for interf in arpdict:
		#print(interf)
		#print(arpdict[interf])
		localNumofDynamics = 0
		# Count all dynamic addresses per interface.
		for addr in arpdict[interf]:
			if addr[2] == "dynamic":
				localNumofDynamics += 1
		# If this interface has the highest number of dynamic ips so
		# far, store it to variable.
		if localNumofDynamics >= maxNumOfDynamics:
			maxNumOfDynamics = localNumofDynamics
			interfaceName = interf
	#print("\n")
	#print(interfaceName)
	#print(maxNumOfDynamics)

	dynamicLs = getDynamicIps(interfaceName, arpdict)
	#for i in dynamicLs:
	#	print(i)

	# Close file.
	datafile.close()
	
	# Delete file.
	subprocess.Popen("rm arpdata.txt").wait()

	return (interfaceName, dynamicLs)


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
	# variable is returned by the function.
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


# Retrieves a list of dynamic ip addresses given and interface that
# exists within the arp dictionary.
def getDynamicIps(interfaceName, arpdict):
	retList = []
	for addr in arpdict[interfaceName]:
		if addr[2] == "dynamic":
			retList.append(addr)
	return retList


# Get the type of interface that the user is currently connected to.
def getInterftype(opSys, interfaceName):
	# Network devices in machine and their respective information/
	# statuses.
	netDevs = ipfconfig(opSys)
	# Match Interface with network devices in the machine. 
	
	#print(netDevs)
	#for d in netDevs:
	#	# Print interface.
	#	print(d)
	#	# Print interface data.
	#	for l in netDevs[d]:
	#		print(l)

	# Find which interfaces matches the ipaddress 
	for d in netDevs:
		for l in netDevs[d]:
			if interfaceName in l:
				return d

	return "Unknown network interface"


# Refresh the listbox in the Log in page with all current ipaddresses.
def refreshOnlineDevLb(onlineDevsLb, ipaddresses):
	for i in range(1, len(ipaddresses)):
		string = "       ".join(ipaddresses[i])
		onlineDevsLb.insert(tk.END, string)


# Create "log in" page GUI with tkinter.
def page1(arpDat, opSys, interftype):
	interfaceName = arpDat[0]
	ipaddresses = arpDat[1]

	interfaceName = interfaceName.split(" ")[1]

	pg1 = tk.Tk()
	pg1.title("Setup")
	pg1.geometry("500x450")
	pg1.configure(background="black")

	titleFont = ("Helvetica", 14)
	welcomeLblStr = "Welcome to Peer Chat"
	welcomeLbl = tk.Label(pg1, text=welcomeLblStr, bg="black", 
						  fg="white", font=titleFont)
	welcomeLbl.pack()

	interftypeLblStr = "Interface type: " + str(interftype)
	interftypeLbl = tk.Label(pg1, text=interftypeLblStr, bg="black",
							 fg="white")
	interftypeLbl.pack()

	interfNmLblStr = "Interface address: " + str(interfaceName)
	interfNmLbl = tk.Label(pg1, text=interfNmLblStr, bg="black", 
						   fg="white")
	interfNmLbl.pack()

	dfltGatewayLblStr = "Default gateway: " + str(ipaddresses[0])
	dfltGatewayLbl = tk.Label(pg1, text=dfltGatewayLblStr, bg="black",
							  fg="white")
	dfltGatewayLbl.pack()

	onlineDevsLblStr = "Available Devices on subnet: "
	onlineDevsLbl = tk.Label(pg1, text=onlineDevsLblStr, bg="black",
							 fg="white")
	onlineDevsLbl.pack()

	onlineDevsLb = tk.Listbox(pg1, bg="black", fg="white")
	onlineDevsLb.pack(expand=True)
	refreshOnlineDevLb(onlineDevsLb, ipaddresses)

	modeLbl = tk.Label(pg1, text="Mode:", bg="black", fg="white")
	modeLbl.pack()

	joinIpLbl = tk.Label(pg1, text="Room IP: ", bg="black", fg="white")
	joinIpLbl.pack()

	joinIPEntry = tk.Entry(pg1, bg="black", fg="white")
	joinIPEntry.pack()

	clientBtn = tk.Button(pg1, text="Join Room", bg="black", 
						  fg="white", command=None)
	clientBtn.pack()
	serverBtn = tk.Button(pg1, text="Create A Room", bg="black",
						  fg="white", command=None)
	serverBtn.pack()

	pg1.mainloop()


def main():
	# Detect system's os.
	opSys = detectOS()
	print(opSys)

	# Retrieve ARP data.
	arpDat = arp(opSys)

	# Varibales retrieved from initial network scan.
	interfaceName = arpDat[0]
	ipaddresses = arpDat[1]

	interfaceName = interfaceName.split(" ")[1]

	# Determine type of interface given the interface name.
	interftype = getInterftype(opSys, interfaceName)

	print("\n")
	#print(interfaceName)
	print("Interface type: "+str(interftype))
	print("Interface address: "+str(interfaceName))
	print("Default gateway: "+str(ipaddresses[0]))
	print("Devices found on subnet:")
	for dev in range(1, len(ipaddresses)):
		print(ipaddresses[dev])

	page1(arpDat, opSys, interftype)


if __name__ == '__main__':
	main()
