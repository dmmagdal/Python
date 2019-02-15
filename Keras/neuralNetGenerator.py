# neuralNetGenerator.py
# author: Diego Magdaleno
# Uses genetic algorithm to generate and test neural networks from
# keras. Hope is that this serves as a framework for creating original
# and optimal Neural Networks for ML/AI problems.
# Python 3.6
# Linux

#import keras
import numpy
import random
from keras import *
from keras.layers import *


def main():
	inputData = None
	outputData = None
	numFeatures = None

	# Initialize variables for generating a model.
	modelType = None
	availableLayers = []
	modelLayers = []
	numInputNodes = 1
	model = createModel(modelType, modelLayers, numInputNodes)
	model.compile()
	model.fit()
	scores = model.evaluate(inputData, outputData)

	# Create models until there's a most optimal model.
	generation = 1
	while scores <= 93.00:
		if generation == 1:
			# Create 8 randomly generated models
			for i in range(8):


		else:
			# Cross bread the top two models from the previous
			# generation

# Creates and returns a model.
def createModel(modelType, modelLayers):
	return None


if __name__ == '__main__':
	main()