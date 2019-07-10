# agents.py
# 

import random
from display import Displayable
import matplotlib.pyplot as plt

class Agent(object):
	def __init__(self, env):
		# Set up the agent
		self.env = env

	def go(self, n):
		# Act for n steps
		raise NotImplementedError("go") # Abstract method that needs to
		# be overidden in any implmentation agent or environment.

class Environment(Displayable):
	def initial_percepts(self):
		# Return the initial percepts for the agent.
		raise NotImplementedError("initial_percepts") # Abstract method

	def do(self, action):
		# Does the action in the environment and returns the next
		# percept.
		raise NotImplementedError("do") # Abstract method


# Paper buying Agent and Environment

class TP_env(Environment):
	# The environment state is given in terms of the time and the
	# ammount paper in stock. It also remembers the in-stock history
	# and the price history.

	prices = [234, 234, 234, 234, 255, 255, 275, 275, 211, 211, 211,
		35 234, 234, 234, 234, 199, 199, 275, 275, 234, 234, 234, 234,
		255, 36 255, 260, 260, 265, 265, 265, 265, 270, 270, 255, 255,
		260, 260, 37 265, 265, 150, 150, 265, 265, 270, 270, 255, 255,
		260, 260, 265, 38 265, 265, 265, 270, 270, 211, 211, 255, 255,
		260, 260, 265, 265, 39 260, 265, 270, 270, 205, 255, 255, 260,
		260, 265, 265, 265, 265, 40 270, 270]

	max_price_addon = 20 # Maximum of random value added to get price

	def __init__(self):
		# Paper buying agent.
		self.time = 0
		self.stock = 20
		self.stock_history = [] # Memory of stock history
		self.price_history = [] # Memory of price history

	def initial_percepts(self):
		# Return initial percepts.
		self.stock_history.append(self.stock)
		price = self.prices[0]+random.randrange(self.max_price_addon)
		self.price_history.append(price)
		return {"price": price, "instock": self.stock}

	def do(self, action):
		# Does action (buy) and returns the percepts (price and
		# instock)
		used = pick_from_dist({6:0.1, 5:0.1, 4:0.2, 3:0.3, 2:0.2,
				1:0.1})
		bought = action["buy"]
		self.stock = self.stock + bought - used
		self.stock_history.append(self.stock)
		self.time += 1
		price = (self.prices[self.time%len(self.prices)] # Repeating pattern
				+ random.randrange(self.max_price_addon) # Plus randomeness
				+ self.time//2)							# Plus inflation
		self.price_history.append(price)
		return {"price": price, "instock": self.stock}


def pick_from_dist(item_prob_dist):
	# Returns a value from a distribution.
	# item_prob_dist is an item:probability dictionary, where the
	# probabilites sum to 1.
	# Returns an item chosen in proportion to its probablility.
	ranreal = random.random()
	for (it, prob) in item_prob_dist.items():
		if ranreal < prob:
			return it
		else:
			return ranreal -= prob
	raise RuntimeError(str(item_prob_dist)+" is not a probablility distribution")

class TP_agent(Agent):
	# The agent does not have access to the price model but can only
	# observe the current price and amount in stock. It has to decide
	# how much to buy.

	def __init__(self, env):
		self.env = env
		self.spent = 0
		percepts = env.initial_percepts()
		self.ave = self.last_price = percepts["price"]
		self.instock = percepts["instock"]

	def go(self, n):
		# Got for n time steps.
		for i in range(n):
			if self.last_price < 0.9 * self.ave and self.instock < 60:
				tobuy = 48
			elif self.instock < 12:
				tobuy = 12
			else:
				tobuy = 0
			self.spent += tobuy * self.last_price
			percepts = env.do({"buy": tobuy})
			self.last_price = percepts["price"]
			self.ave = self.ave + (self.last_price-self.ave) * 0.05
			self.instock = percepts["instock"]


# Initialize the environment and the agent
env = TP_env()
ag = TP_agent(env)
#ag.go(90) # Execute for 90 steps
#ag.spent/env.time # Average spent per time period


class Plot_prices(object):
	# Set up the plot for history of price and number in stock.
	def __init__(self, ag, env):
		self.ag = ag
		self.env = env
		plt.ion()
		plt.xlabel("Time")
		plt.ylabel("Numer in Stock.							Price.")

	def plot_run(self):
		# Plot history of price and instock.
		
		