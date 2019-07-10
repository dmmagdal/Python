# agentMiddle.py
# Acts like a controller (for the environment layer) and an environment
# for the upper layer. It has to tell the environment how to steer (by
# calling env.do()) and is also told the position to go to and the
# timeout. 

from agents import Environment
import math


class Rob_middle_layer(Environment):
	def __init__(self, env):
		self.env = env
		self.percepts = env.initial_percepts()
		self.straight_angle = 11 # angle that is close enough to straight ahead
		self.close_threshold = 2 # distance that is close enough to arrived
		self.close_threshold_squared = self.close_threshold**2 # just compute it once

	def initial_percepts(self):
		return {}

	def do(self, action):
		# Action is {'go_to': target_pos, 'timeout':timeout}
		# target_pos is a (x,y) pair
		# timeout is the number of steps to try
		# returns {'arrived': True} when arrived is true or
		#	{'arrived': False} if it reached the timeout
		if 'timeout' in action:
			remaining = action['timeout']
		else:
			remaining = -1 # will never reach 0
		target_pos = action['go_to']
		arrived = self.close_enough(target_pos)
		while not arrived and remaining != 0:
			self.percepts = self.env.do({'steer': self.steer(target_pos)})
			remaining -= 1
			arrived = self.close_enough(target_pos)
		return {'arrived': arrived}

	def steer(self, target_pos):
		# Determines how to steer depending on whether the goal is to
		# the right or to the left of where the robot is facing.
		if self.percepts['whisker']:
			self.display(3, 'whisker on', self.percepts)
			return 'left'
		else:
			gx, gy = target_pos