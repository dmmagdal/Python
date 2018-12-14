# swarm.py
# author: Diego Magdaleno
# create a game instance of objects and a swarm to navigate between
# obstacles.
# game:
# Python 3.6
# Windows 10

import sys
import turtle
import random


# Obstacle Object class.
class Obstacle:
	# "Private" data.
	__shapeList = ["traingle", "rectangle", "ellipse", "polygon"]
	# "Public" internal data.
	shape = ""
	center = []
	cornerPoints = []

	def __init__(self, shape=None, center=None, cornerPoints=None):
		# Set shape.
		if shape == None:
			self.shape = random.choice(self.__shapeList)
			if shape == "traingle":
				corners = generateCorners(3, center)
				self.cornerPoints = corners 
			elif shape == "rectangle":
				corners = generateCorners(4, center)
				self.cornerPoints = corners
			elif shape == "polygon":
				numSides = random.randint(4,25)
				corners = generateCorners(numSides, center)
				self.cornerPoints = corners
		else:
			self.shape = shape
		# Set center.
		if center == None:
			randX = random.randint(50, 650)
			randY = random.randint(0, 750)
			self.center = [randX, randY]
		else:
			self.center = center
		# Set cornerpoints.
		if cornerPoints == None:
			if shape == "traingle":
				corners = generateCorners(3, center)
				self.cornerPoints = corners 
			elif shape == "rectangle":
				corners = generateCorners(4, center)
				self.cornerPoints = corners
			elif shape == "polygon":
				numSides = random.randint(4,25)
				corners = generateCorners(numSides, center)
				self.cornerPoints = corners
		else:
			self.cornerPoints = cornerPoints
		

	'''
	#------------------------------------------------------------------
	# constructors no longer needed.
	#------------------------------------------------------------------
	def __init__(self):
		self.shape = random.choice(self.__shapeList)
		randX = random.randint()
		randY = random.randint()
		self.center = [randX, randY]
		if shape == "traingle":
			corners = generateCorners(3, center)
			self.cornerPoints = corners 
		elif shape == "rectangle":
			corners = generateCorners(4, center)
			self.cornerPoints = corners
		elif shape == "polygon":
			numSides = random.randint(4,25)
			corners = generateCorners(numSides, center)
			self.cornerPoints = corners


	def __init__(self, shape, center):
		self.shape = shape
		self.center = center
		if shape == "traingle":
			corners = generateCorners(3, center)
			self.cornerPoints = corners 
		elif shape == "rectangle":
			corners = generateCorners(4, center)
			self.cornerPoints = corners
		elif shape == "polygon":
			numSides = random.randint(4,25)
			corners = generateCorners(numSides, center)
			self.cornerPoints = corners


	def __init__(self, center, cornerPoints):
		self.cornerPoints = cornerPoints
		self.center = center
		numPoints = len(cornerPoints)
		if numPoints == 3:
			self.shape = "traingle"
		elif numPoints == 4:
			self.shape = "rectangle"
		elif numPoints > 4:
			self.shape = "polygon"


	def __init__(self, shape, center, cornerPoints):
		self.shape = shape
		self.center = center
		self.cornerPoints = cornerPoints
	'''


	# For randomly generated obstacles, this will used the number of
	# sides (>= 3) and it's center and generates a list of coordinates
	# for the corners of the obstacle.
	def generateCorners(numSides, center):
		# Store the x and y coordinates of the object's center.
		xcoord = center[0]
		ycoord = center[1]
		# List to store corners (list of [x,y] ints for the corner
		# coordinates).
		cornersList = []
		# If the number of sides are exactly 3.
		if numSides == 3:
			for i in range(numSides):
				if i == 0:
					xcorner = xcoord + random.randint(25)
					ycorner = ycoord + random.randint(25)
					cornersList.append([xcorner, ycorner])
				elif i == 1:
					xcorner = xcoord - random.randint(25)
					ycorner = ycoord + random.randint(25)
					cornersList.append([xcorner, ycorner])
				elif i == 2:
					xcorner = xcoord - random.randint(25)
					ycorner = ycoord - random.randint(25)
					cornersList.append([xcorner, ycorner])
		# If the number of sides are more than 3.
		else:
			for i in range(numSides):
				if i < numSides//4:
					xcorner = xcoord + random.randint(25)
					ycorner = ycoord + random.randint(25)
					cornersList.append([xcorner, ycorner])
				elif i > numSides//4 and i < numSides//2:
					xcorner = xcoord - random.randint(25)
					ycorner = ycoord + random.randint(25)
					cornersList.append([xcorner, ycorner])
				elif i > numSides//2 and i < numSides * 3//4:
					xcorner = xcoord - random.randint(25)
					ycorner = ycoord - random.randint(25)
					cornersList.append([xcorner, ycorner])
				else:
					xcorner = xcoord + random.randint(25)
					ycorner = ycoord - random.randint(25)
					cornersList.append([xcorner, ycorner])
		# Return corners list.
		return cornersList


	# Draw the obstacle with a turtle.
	def draw():
		# Create turtle object to draw the obstacle.
		objTur = turtle.Turtle()
		objTur.color("white")
		objTur.pensize(1)

		# Send turtle to obstacle's center.
		objTur.goto(self.center[0], self.center[1])

		# Start drawing shape.
		objTur.pendown()
		objTur.begin_fill()
		for coord in self.cornerPoints:
			objTur.goto(coord[0], coord[1])
		objTur.goto(self.cornerPoints[0][0], self.cornerPoints[0][1])
		objTur.end_fill()



# Ship Object class.
class Ship:
	# "Public" internal data.
	xcoord = 0
	ycoord = 0
	shipNum = 0

	def __init__(self, screensize):
		self.xcoord = random.randint(5, screensize-5)
		self.ycoord = random.randint(5, screensize-5)
		self.shipNum = random.randint()


	def __init__(self, center, shipNum):
		self.xcoord = center[0]
		self.ycoord = center[1]
		self.shipNum = shipNum


	def fly():
		pass


	# Return a boolean telling if the ship is about to collide with an
	# obstacle.
	def collision():
		pass



def main():
	# Argument variables.
	debug = False
	numDrones = 1
	numObj = random.randint(1, 25)

	# If there are 2 command line arguments.
	if len(sys.argv) == 2:
		#Usage python swarm.py <Number of Drones>"
		numDrones = int(sys.argv[1])
	# If there are 3 command line arguments.
	elif len(sys.argv) == 3:
		#Usage python swarm.py <Number of Drones> <Number of Obstacles>"
		#Usage python swarm.py -d <Number of Drones>"
		if sys.argv[1] == "-d":
			debug = not debug
			numDrones = int(sys.argv[2])
		else:
			numDrones = int(sys.argv[1])
			numObj = int(sys.argv[2])
	# If there are 4 command line arguments.
	elif len(sys.argv) == 4:
		#Usage python swarm.py -d <Number of Drones> <Number of Obstacles>"
		debug = not debug
		numDrones = int(sys.argv[2])
		numObj = int(sys.argv[3])
	# Otherwise, there are insufficient command line arguments.
	else:
		#Usage python swarm.py -h.
		print("Error: Improper command line arguments.")
		print("For help, enter \"python swarm.py -h.\"")
		exit(1)

	if debug:
		# Check if the appropriate values have been set for the number
		# of drones/ships as well as obstacle objects.
		print("There are "+str(numDrones)+" number of ships.")
		print("There are "+str(numObj)+" number of obstacles.")

		# Check if the generateObjects() method works (ie, obstacles
		# can be initialized without any issues.)
		obj1 = generateObjects(numObj)
		# Check if the drawScreen() method works (ie, can objects be
		# drwan to the canvas without any issues.)
		drawScreen(obj1)

	'''
	# Create a list of obstacles and store that.
	listOfObj = generateObjects(numObj)
	# So long as a solution with the current map does not exist,
	# generate a new set of obstacles.
	while not solutionExists(listOfObj):
		listOfObj = generateObjects()
	'''


# Generate a list of obstacles in the map.
def generateObjects(numObjs):
	# Initialize an empty objects list.
	objectsList = []
	# Append the appropriate number of obstacle objects to the list.
	for i in range(numObjs):
		objectsList.append(Obstacle())
	# Return the objects list.
	return objectsList


# Check if a solution exists given the current map.
def solutionExists(objList):
	return True


# Draw the current screen.
def drawScreen(obstacleList,):
	win = turtle.Screen()
	win.title("Swarm Game")
	win.setup(width=750, height=750, startx=25, starty=25)
	win.bgcolor("black")

	# Draw obstacles.
	for ob in obstacleList:
		ob.draw()

	#win.exitonclick()
	win.mainloop()


if __name__ == '__main__':
	main()