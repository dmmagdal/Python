# Tamagotchi.py
# author: Diego Magdaleno
# This is a small python program that allows a user to "adopt" and
# "raise" their own tamagatchi pets on their desktop.
# Sources: https://runestone.academy/runestone/books/published/fopp/
# Classes/Tamagotchi.html
# Python 3.7
# Windows/MacOS/Linux


import os
import subprocess
import math
import random
from datetime import datetime


# Create the Pet class.
class Pet():
	def __init__(self, pet_name, health, is_alive, hunger, boredom):
		# Initialize all variables from constructor arguments.
		self.name = pet_name
		self.health = health
		self.is_alive = is_alive
		self.hunger = hunger
		self.boredom = boredom

		# Initalize all static variables.
		self.HUNGER_THRESHOLD = 20
		self.BOREDOM_THRESHOLD = 30
		self.HEALTH_THRESHOLD = 1

		# Calculate the hunger and boredem from last load (if
		# applicable) and subtract that from the respective meters.

		# Check the pet's hunger, boredom, and heath. Decrement the
		# respective variables if the values currently loaded are below
		# the set thresholds.
		if self.hunger < self.HUNGER_THRESHOLD:
			self.health -= random.randint(10)

		if self.boredom < self.BOREDOM_THRESHOLD:
			self.health -= random.randint(5)

		if self.health < self.HEALTH_THRESHOLD:
			self.is_alive = False

		if not self.is_alive:
			self.make_noise("dead")
		
		# Return nothing.
		return


	def play(self, game_name):
		# Initialize dictionary containing a mapping of all valid
		# games and their respective game functions.
		VALID_GAMES = {"walk": "walk_game_function",
						"fetch": "fetch_game_function",
						"pet": "pet_game_function"}

		# Play the game and retrieve the score.
		boredom_points = VALID_GAMES[game_name]

		# Restore boredom points based on the game score achieved.
		self.boredom += boredom_points

		# Return nothing.
		return


	def feed(self, food_name):
		# Initialize dictionary containing a mapping of all valid
		# foods and their respective point values.
		VALID_FOODS = {"chicken": 45,
						"bone": 15,
						"salmon": 40,
						"kibble": 35}

		# Restore hunger points based on the food chosen.
		self.hunger += VALID_FOODS[food_name]

		# Return nothing.
		return


	def make_noise(self, emotion_noise)
		# Initialize dictionary containing a mapping of all valid
		# emotions and the file paths to their sound files.
		VALID_NOISES = {"happy1": "file_path",
						"happy2": "file_path",
						"happy3": "file_path",
						"happy4": "file_path",
						"sad1": "file_path",
						"sad2": "file_path",
						"sad3": "file_path",
						"bored1": "file_path",
						"bored2": "file_path",
						"dead": "file_path"}

		# Isse the sound/notification to the desktop.

		# Return nothing.
		return


	def save(self, pet_name):
		
		pass


	def load(self, pet_name):
		pass



def main():
	# Prompt the user to either load in a tamagotchi or create a new
	# pet.

	# Have the pet available until the user decides to close the
	# program. Then save the pet.

	# Exit the program.
	exit(0)


if __name__ == '__main__':
	main()