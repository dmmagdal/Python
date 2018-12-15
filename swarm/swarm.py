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
import math


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
		if cornerPoints == None and shape == "traingle":
			corners = self.generateCorners(3, self.center)
			self.cornerPoints = corners 
		elif cornerPoints == None and shape == "rectangle":
			corners = self.generateCorners(4, self.center)
			self.cornerPoints = corners
		elif cornerPoints == None and shape == "polygon":
			numSides = random.randint(4,25)
			corners = self.generateCorners(numSides, self.center)
			self.cornerPoints = corners
		elif cornerPoints == None and shape == "ellipse":
			circumfPoints = self.genEllipseCircPts(self.center)
			self.cornerPoints = circumfPoints
		else:
			self.cornerPoints = cornerPoints
		print(self.cornerPoints)


	# For randomly generated obstacles, this will used the number of
	# sides (>= 3) and it's center and generates a list of coordinates
	# for the corners of the obstacle.
	def generateCorners(self, numSides, center):
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
					xcorner = xcoord + random.randint(5, 25)
					ycorner = ycoord + random.randint(5, 25)
					cornersList.append([xcorner, ycorner])
				elif i == 1:
					xcorner = xcoord - random.randint(5, 25)
					ycorner = ycoord + random.randint(5, 25)
					cornersList.append([xcorner, ycorner])
				elif i == 2:
					xcorner = xcoord - random.randint(5, 25)
					ycorner = ycoord - random.randint(5, 25)
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


	# For randomly generated ellipse obstacles, this will generate a
	# list of points that will represent the corners of the ellipse.
	def genEllipseCircPts(self, center):
		# Store the x and y coordinates of the object's center.
		xcoord = center[0]
		ycoord = center[1]
		# Randomly generate a height and width for the ellipse.
		a = random.randint(5, 25)
		b = random.randint(5, 25)
		# List to store corners (list of [x,y] ints for the corner
		# coordinates).
		cornersList = []
		# If a = b, then treat a as the radius of a circle.
		if a == b:
			circumference = 2 * math.pi + a
			n = circumference*64
			for i in range(int(n)):
				xpoint = xcoord + int(math.cos(2*math.pi/n*i)*a)
				ypoint = ycoord + int(math.sin(2*math.pi/n*i)*a)
				cornersList.append([xpoint,ypoint])
		# Otherwise, treat the obstacle as an ellipse.
		else:
			numerator = math.pow(a-b, 2)
			denominator = math.pow(a+b, 2)
			h = numerator/denominator
			mult = 1 + ((3 * h)/(10 + math.sqrt(4 - (3 * h))))
			circumference = math.pi * (a + b) * mult
			n = circumference*64
			for i in range(int(n)):
				xpoint = xcoord + int(math.cos(2*math.pi/n*i)*a)
				ypoint = ycoord + int(math.sin(2*math.pi/n*i)*b)
				cornersList.append([xpoint,ypoint])
		# Return corners list.
		return cornersList


	# Draw the obstacle with a turtle.
	def draw(self):
		# Create turtle object to draw the obstacle.
		objTur = turtle.Turtle()
		objTur.color("white")
		objTur.pensize(1)
		objTur.penup()

		# Send turtle to obstacle's center.
		objTur.goto(self.center[0], self.center[1])

		# Start drawing shape.
		objTur.pendown()
		objTur.begin_fill()
		for coord in self.cornerPoints:
			objTur.goto(coord[0], coord[1])
		#objTur.goto(self.cornerPoints[0][0], self.cornerPoints[0][1])
		objTur.end_fill()



# Ship Object class.
class Ship:
	# "Public" internal data.
	xcoord = 0
	ycoord = 0
	shipNum = 0

	def __init__(self, center=None, shipN=None, size=None, numS=None):
		if center == None and size != None:
			self.xcoord = random.randint(5, size-5)
			self.ycoord = random.randint(5, size-5)
		elif center != None:
			self.xcoord = center[0]
			self.ycoord = center[1]
		if shipNum == None:
			self.shipNum = random.randint(1, numS)
		else:
			self.shipNum = shipN


	def draw():
		ship = turtle.Turtle()
		ship.color("red")
		ship.penup()


	# Move the ship until 
	def fly():
		pass


	# Return a boolean telling if the ship is about to collide with an
	# obstacle.
	def collision():
		return False



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

		# Check if intitializing obstacles works.
		obj0 = [Obstacle("traingle")]
		#print(obj0[0].center)
		#print(obj0[0].shape)
		#print(obj0[0].cornerPoints)

		# Check if the generateObjects() method works (ie, obstacles
		# can be initialized without any issues.)
		obj1 = generateObjects(numObj)
		# Check if the drawScreen() method works (ie, can objects be
		# drwan to the canvas without any issues.)
		#drawScreen(obj0)
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
	win.setworldcoordinates(0, 0, 750, 750)
	#win.delay(300)

	# Draw obstacles.
	for ob in obstacleList:
		ob.draw()
		print(ob.center)
		print(ob.shape)
		print(ob.cornerPoints)

	#win.exitonclick()
	win.mainloop()


if __name__ == '__main__':
	main()
