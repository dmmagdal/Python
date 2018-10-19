# hellocreate.py
# author: Diego Magdaleno
# A small program to run on the Create 2 robot. A sort of "hello world"
# program. Copied from pycreate2 documentation here, at
# https://pypi.org/project/pycreate2/ .
# Python 3.6
# Linux

from pycreate2 import Create2
import time

def main():
	# Create new bot object.
	bot = Create2()

	# Start the bot.
	bot.start()

	# Put bot into "safe" mode so it can be driven with some
	# protections.
	bot.safe()

	# Put bot into "full" mode. You are responsible for handling
	# issues, no protection/safety in this mode.
	bot.full()

	# Directly set motor speeds (easier if using a joystick).
	bot.drive_direct(100, 100)

	# Turn angle [degrees] at speed. 45 deg, 100 mm/sec.
	bot.turn_angle(45, 100)

	# Drive straight for a distance. 5m, reverse at 100 mm/sec.
	bot.drive_distance(5, -100)

	# Tell the bot to drive straight forward at 100 mm/sec.
	bot.drive_straight(-100)
	time.sleep(2)

	# Turn in place.
	bot.drive_turn(-100, 0)
	time.sleep(4)

	# Turn in place (again).
	bot.drive_turn(100, 0)
	time.sleep(2)

	# Use simpler drive_direct.
	bot.drive_direct(200, -200) # inputs are +/- 500 max.
	time.sleep(2)

	# Stop the bot.
	bot.drive_stop()

	# Query some sensors.
	sensors = bot.get_sensors() # returns all data
	print(sensors.light_bumper_left)

	# Close the connection to the bot.
	bot.close()


if __name__ == '__main__':
	main()
