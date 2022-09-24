# asteroids.py
# This is an Asteroids clone written in python with pygame.
# Source: https://realpython.com/asteroids-game-python/#project-overview
# Python 3.6
# Windows/MacOS/Linux


import pygame


class SpaceRocks:
	def __init__(self):
		# Initialize pygame and set the display.
		self._init_pygame()
		self.screen = pygame.display.set_mode((800, 600))


	def main_loop(self):
		# Initialize game loop. Handle user input first, then process
		# the game logic, then draw.
		while True:
			self._handle_input()
			self._process_game_logic()
			self._draw()


	def _init_pygame(self):
		pygame.init()
		pygame.display.set_caption("Space Rocks")


	def _handle_input(self):
		for event in pygame.event.get():
			# Close the game on a quit event (click "Close", Alt + F4,
			# or Cmd + W) or when the ESC key is pressed.
			if event.type == pygame.QUIT or \
			(event.type = pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				quit()


	def _process_game_logic(self):
		pass


	def _draw(self):
		# Set the screen color and update its contents.
		self.screen.fill((0, 0, 255))
		pygame.display.flip()