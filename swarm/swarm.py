# swarm.py
# author: Diego Magdaleno
# create a game instance of objects and a swarm to navigate between
# obstacles.
# Python 3.6
# Windows 10

import sys
import turtle
import random


def main():
	debug = False

	# If there are 2 command line arguments.
	if (len(sys.argv) == 2):
		#Usage python swarm.py <Number of Drones>"
	# If there are 3 command line arguments.
	elif (len(sys.argv) == 3):
		#Usage python swarm.py <Number of Drones> <Number of Obstacles>"
		#Usage python swarm.py -d <Number of Drones>"
	# If there are 4 command line arguments.
	elif (len(sys.argv) == 4):
		#Usage python swarm.py -d <Number of Drones> <Number of Obstacles>"

	# Create a list of obstacles and store that.
	listOfObj = generateObjects()
	# So long as a solution with the current map does not exist,
	# generate a new set of obstacles.
	while !solutionExists(listOfObj):
		listOfObj = generateObjects()


# Generate a list of obstacles in the map.
def generateObjects():
	return []


# Check if a solution exists given the current map.
def solutionExists(objList):
	return True


if __name__ == '__main__':
	main()
