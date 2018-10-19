# kerasNeuNet1.py
# A first Neural network with Keras.
# author: Diego Magdaleno
# Python 3.6
# Windows 10

from keras.models import Sequential
from keras.layers import Dense
import numpy

# fix a seed with the random generator.
numpy.random.seed(7)

# use pima Indian onset of diabetes dataset.
# load file (dataset) directly.
dataset = numpy.loadtxt("pima-indians-diabetes.csv", delimiter=",")
# split into X (input) and Y (output) variables.
X = dataset[:,0:8]
Y = dataset[:,8]

# define the model.
# Using Keras Sequential model.

# Ensure the input layers have right number of input.
# Using fully connected network structure with 3 layers for this
# example. Fully connected layers defined with Dense() class.

# Dense class
#	specify number of neurons.
#	initialise method (init=).
#	specify activation function (activation=).

# first layer (input layer) is input_dim with 8 inputs and 12 neurons.
# last layer (output layer) is a signoid function and 1 neuron.
model = Sequential()
model.add(Dense(12, input_dim=8, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# rectifier 'relu' activation function.
# sigmoid 'sigmoid' activation function.

# compile model.
# specify additional properties required when training the network.
# looking at best set of weights for the problem.

# specify loss function to use to evaluate a set of weights.
model.compile(loss='binary_crossentropy', optimizer='adam',
			  metrics=['accuracy'])
# loss function is algorithmic loss which is the binary cross entropy
# for a binary classification problem.
# gradient decent algorithm used is called adam (very efficient)
# because it is an efficient default.

# fit model.
# execute the model on some data. Can train or fit model on loaded data
# by calling fit() on model.

# training process runs for fixed number of iterations through the
# dataset called epochs (specified through the nepochs argument). Can
# also set the number of instances that are evaluated before a weight
# update in the network performed (called batch size and set using
# batch_size argument).
model.fit(X, Y, epochs=150, batch_size=10)

# use 150 iterations and a small batch size of 10. Values chosen
# experimentally by trial and error.

# evaluate model.
# evaulate the model on the training dataset using the evaluate()
# function on the model and pass it the same input and output used to
# train the model.

scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# bonus: making predictions.
# this example can be used to generate predictions on the training
# dataset, pretending it is a new dataset we have not seen before.

# can make predictions with model.predict(). We're using a sigmoid
# activation function on the output layer, so the predictions will
# be in range 0 to 1. Can easily conver them to a binary prediction
# for classification task my rounding them.

# calculate predictions.
predictions = model.predict(X)
# round predictions.
rounded = [round(x[0]) for x in predictions]
print(rounded)
