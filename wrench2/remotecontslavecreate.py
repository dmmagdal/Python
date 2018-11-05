# remotecontslavecreate.py
# author: Diego Magdaleno
# A program to remote control the Create2 bot from a laptop (Slave).
# Python 3.6
# Linux

from pycreate2 import Create2
import sys
import socket
import time

def main():
	bot = Create2()
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
