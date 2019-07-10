# display.py
# A simple way to trace the intermediate steps of algorithms.

class Displayable(object):
	# The amount of detail is controlled by max_display_level.

	max_display_level = 1 # Can be overidden in subclasses

	def display(self, level, *args, **nargs):
		# Print the arguments if the level is less than or equal to the
		# current max_display_level.
		# Level is an integer.
		# The other arguments are whatever arguments print can take.
		if level <= max_display_level:
			print(*args, **nargs) # If you get an error, you're using
			# python 2, not python 3.

def visualize(func):
	# A decorator for algorithms that do interactive visualization.
	# Ignored here.
	return func
