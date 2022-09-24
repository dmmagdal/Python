# __main__.py
# Runs an instance of the asteroids game (asteroids.py).
# Python 3.6
# Windows/MacOS/Linux


from asteroids import SpaceRocks


if __name__ == '__main__':
	asteroids_game = SpaceRocks()
	asteroids_game.main_loop()