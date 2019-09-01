# turtleInvaders.py
# author: Diego Magdaleno
# This is a small game using native python modules to
# 	create a space invadors like game with turtles. Is
#	2 player as well.
# Python 3.6
# Windows 10

import sys
import turtle
import random
import math
import time

class Ship:
	# xcoord = 0
	# ycoord = 0
	# shipTurtle = None
	# hitbox = [] 

	def __init__(self, center, color, shipType=None):
		self.xcoord = center[0]
		self.ycoord = center[1]
		self.shipTurtle = turtle.Turtle()
		self.shipTurtle.setx(self.xcoord)
		self.shipTurtle.sety(self.ycoord)
		self.shipTurtle.color(color)
		self.shipTurtle.penup()
		self.shipTurtle.showturtle()
		if shipType == None:
			self.shipTurtle.speed(1)
			#self.shipTurtle.rotate(90)
			self.shipTurtle.setheading(90)
		else:
			self.shipTurtle.speed(0.75)
			#self.shipTurtle.rotate(-90)
			self.shipTurtle.setheading(270)
		self.updateHitBox(self.xcoord, self.ycoord)


	def move(self, xmove, ymove):
		self.xcoord += xmove
		self.ycoord += ymove
		if self.xcoord > 725 or self.xcoord < 25:
			self.xcoord -= xmove
		if self.ycoord < 200:
			self.ycoord -= ymove
		self.shipTurtle.goto(self.xcoord, self.ycoord)
		self.updateHitBox(self.xcoord, self.ycoord)


	def updateHitBox(self, xcenter, ycenter):
		corner1 = (xcenter+3, ycenter+6)
		corner2 = (xcenter-3, ycenter+6)
		corner3 = (xcenter-3, ycenter-6)
		corner4 = (xcenter+3, ycenter-6)
		self.hitbox = [corner1, corner2, corner3, corner4]


	def fire(self, color):
		return Blaster([xcoord, ycoord], color)



class Blaster:
	# xcoord = 0
	# ycoord = 0
	# blastTurtle = None

	def __init__(self, center, color):
		self.xcoord = center[0]
		self.ycoord = center[1]
		self.blastTurtle = turtle.Turtle()
		self.blastTurtle.setx(xcoord)
		self.blastTurtle.sety(ycoord)
		self.blastTurtle.color(color)
		self.blastTurtle.penup()
		self.blastTurtle.shape("square")
		self.blastTurtle.showturtle()


	def move(self):
		self.ycoord += 3
		self.blastTurtle.goto(self.xcoord, self.ycoord)



def main():
	# Initialize player variables.
	numPlayers = 1
	score = [0]
	ships = []

	# Check number of sys args.
	if len(sys.argv) != 2:
		print("Usage: python turtleInvaders.py <NumberOfPlayers>")
		exit(1)
	else:
		# Check that last sys arg is correct.
		if int(sys.argv[1]) != 2 and int(sys.argv[1]) != 1:
			str1 = "Error: Please enter either "
			str2 = "1 or 2 for the number of players"
			print(str1 + str2)
			exit(1)
		else: 
			numPlayers = int(sys.argv[1])

	# Set player variables based on sys args.
	if numPlayers == 2:
		score.append(0)

	# Create screen object.
	win = turtle.Screen()
	win.title("Turtle Invaders")
	win.setup(width=750, height=750, startx=25, starty=25)
	win.bgcolor("black")
	win.setworldcoordinates(0, 0, 750, 750)

	for sh in range(len(score)):
		color = "white"
		if sh // 1 == 1:
			color = "green"
		if sh == 0 and len(score) == 2:
			ships.append(Ship([300, 50], color))
		elif sh == 1 and len(score) == 2:
			ships.append(Ship([400, 50], color))
		else:
			# sh == 0 and len(score) == 1.
			ships.append(Ship([350, 50], color))

	if numPlayers == 2:
		win.onkeypress(lambda: ships[0].move(-1, 0), "Left")
		win.onkeypress(lambda: ships[0].move(1, 0), "Right")
		win.onkeypress(lambda: ships[1].move(-1, 0), "a")
		win.onkeypress(lambda: ships[1].move(1, 0), "d")
	else:
		win.onkeypress(lambda: ships[0].move(-5, 0), "a")
		win.onkeypress(lambda: ships[0].move(5, 0), "d")

	win.listen()
	win.mainloop()


if __name__ == '__main__':
	main()