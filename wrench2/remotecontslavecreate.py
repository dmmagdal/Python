# remotecontslavecreate.py
# author: Diego Magdaleno
# A program to remote control the Create2 bot from a laptop (Slave).
# Python 3.6
# Linux

from pycreate2 import Create2
import sys
import socket
import time
import serial
import glob


connection = None


def setPort():
	ports = getSerialPorts()
	if len(ports) != 0:
		print("Available ports:\n" + '   '.join(ports))
		port = str(ports[0]) # Guess is that Roomba's port is 1st in list.
		return port
	else:
		print("No ports available.")


def onConnect():
	global connection

	if connection is not None:
		print("Oops, you're already connected!")
		return

	try:
		ports = getSerialPorts()
		print("Available ports:\n" + '   '.join(ports))
		if len(ports) != 0:
			port = str(ports[0]) # Guess is that Roomba's port is 1st in list.
	except EnvironmentError:
		port = raw_input("Port? Enter COM port to open.")

	if port is not None:
		print("Trying " + str(port) + "... ")
	try:
		connection = serial.Serial(str(ports[0]), baudrate=115200, timout=1)
		print("Connected!")
	except:
		print("Failed. Could not connect to " + str(port))


def getSerialPorts():
	if sys.platform.startswith('win'):
		print("Windows system detected.")
		ports = ['COM' + str(i + 1) for i in range(256)]
	elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
		print("Linux system detected.")
		ports = glob.glob('/dev/tty[A-Za-z]*')
	elif sys.platform.startswith('darwin'):
		print("MacOS system detected.")
		ports = glob.glob('/dev/tty.*')
	else:
		print("Unsupported platform. Exiting...")
		exit(1)

	results = []
	for port in ports:
		try:
			s = serial.Serial(port)
			s.close()
			results.append(port)
		except (OSError, serial.SerialException):
			pass

	return results


def main():
	port = setPort()
	bot = Create2(port)
	bot.full()


# method for driving mode.
def drive(bot, mode):
	# If the driving mode is tank mode
	if mode == "tank":
		# Set to use tank controls.
		pass
	# Otherwise, drive normally.
	pass


# Method for roaming mode.
def roam(bot):
	# Infinite loop.
	while True:
		# Load sensor data.
		sensors = bot.get_sensors()
		# While the bot doesn't sense a wall.
		while sensors.wall == False;
			# Drive straight.
			bot.drive_straight(100)
		# Otherwise (wall detected) turn the bot
		bot.turn(100, 0)


# Method for dance mode.
def dance(bot):
	bot.turn_angle(720, 400)
	bot.drive_straight(-100)
	bot.drive_straight(100)
	bot.turn_angle(45, 250)
	bot.turn_angle(-90, 250)
	bot.drive_turn(100, 0)
	bot.drive_turn(0, 100)
	bot.drive_turn(100, 0)
	bot.drive_turn(0, 100)
	bot.turn_angle(720, 250)
	bot.drive_straight(-100)


# Method for sentry mode (unimplemented).
def sentry(bot):
	pass


# Method to have robot find its charging dock.
def dock(bot):
	pass


if __name__ == '__main__':
	main()
