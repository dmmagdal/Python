# knn.py
# Implement KNN algorithm for classification & regression.
# Source: https://www.tutorialspoint.com/machine_learning_with_python/
#	machine_learning_with_python_knn_algorithm_finding_nearest_
#	neighbors.htm
# Python 3.7
# Windows/MacOS/Linux


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import accuracy_score


def main():
	# Introduction
	# K-nearest neighbors (KNN) algorithm is a type of supervised ML 
	# algorithm which can be used for both classification as well as 
	# regression predictive problems. However, it is mainly used for 
	# classification predictive problems in industry. The following 
	# two properties would define KNN well:
	#	Lazy learning algorithm − KNN is a lazy learning algorithm 
	#		because it does not have a specialized training phase and 
	#		uses all the data for training while classification.
	#	Non-parametric learning algorithm − KNN is also a 
	#		non-parametric learning algorithm because it doesn’t 
	#		assume anything about the underlying data.

	# Working of KNN Algorithm
	# K-nearest neighbors (KNN) algorithm uses ‘feature similarity’ to 
	# predict the values of new datapoints which further means that the
	# new data point will be assigned a value based on how closely it 
	# matches the points in the training set. We can understand its 
	# working with the help of following steps:
	#	Step 1 − For implementing any algorithm, we need dataset. So 
	#		during the first step of KNN, we must load the training as 
	#		well as test data.
	#	Step 2 − Next, we need to choose the value of K i.e. the 
	#		nearest data points. K can be any integer.
	#	Step 3 − For each point in the test data do the following −
	#		3.1 − Calculate the distance between test data and each row
	#			of training data with the help of any of the method 
	#			namely: Euclidean, Manhattan or Hamming distance. The 
	#			most commonly used method to calculate distance is 
	#			Euclidean.
	#		3.2 − Now, based on the distance value, sort them in 
	#			ascending order.
	#		3.3 − Next, it will choose the top K rows from the sorted 
	#			array.
	#		3.4 − Now, it will assign a class to the test point based 
	#			on most frequent class of these rows.
	#	Step 4 − End

	# Implementation in Python
	# As we know K-nearest neighbors (KNN) algorithm can be used for 
	# both classification as well as regression. The following are the 
	# recipes in Python to use KNN as classifier as well as regressor.

	# KNN as classifier
	# Download the iris dataset from its weblink as follows:
	path = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"

	# Assign column names to the dataset as follows:
	headernames = [
		'sepal-length', 'sepal-width', 'petal-length', 'petal-width', 
		'Class'
	]

	# Read dataset to pandas dataframe as follows:
	dataset = pd.read_csv(path, names = headernames)
	dataset.head()

	# Data Preprocessing will be done with the help of following script
	# lines.
	X = dataset.iloc[:, :-1].values
	y = dataset.iloc[:, 4].values

	# divide the data into train and test split. Following code will 
	# split the dataset into 60% training data and 40% of testing data:
	X_train, X_test, y_train, y_test = train_test_split(
		X, y, test_size = 0.40
	)

	# Data scaling will be done as follows:
	scaler = StandardScaler()
	scaler.fit(X_train)
	X_train = scaler.transform(X_train)
	X_test = scaler.transform(X_test)

	# Train the model with the help of KNeighborsClassifier class of 
	# sklearn as follows:
	classifier = KNeighborsClassifier(n_neighbors = 8)
	classifier.fit(X_train, y_train)

	# At last we need to make prediction. It can be done with the help 
	# of following script:
	y_pred = classifier.predict(X_test)

	# Print the results as follows:
	result = confusion_matrix(y_test, y_pred)
	print("Confusion Matrix:")
	print(result)
	result1 = classification_report(y_test, y_pred)
	print("Classification Report:",)
	print (result1)
	result2 = accuracy_score(y_test,y_pred)
	print("Accuracy:",result2)

	# KNN as regressor
	# Reuse same dataset & column names from above.
	data = pd.read_csv(path, names = headernames)
	array = data.values
	X = array[:,:2]
	Y = array[:,2]
	print(data.shape)

	# Fit the model.
	knnr = KNeighborsRegressor(n_neighbors = 10)
	knnr.fit(X, Y)

	# Find the MSE as follows:
	print(
		"The MSE is: ",format(np.power(Y - knnr.predict(X), 2).mean())
	)

	# Pros and cons of KNN
	# Pros
	#	-> It is very simple algorithm to understand and interpret.
	#	-> It is very useful for nonlinear data because there is no 
	#		assumption about data in this algorithm.
	#	-> It is a versatile algorithm as we can use it for 
	#		classification as well as regression.
	#	-> It has relatively high accuracy but there are much better 
	#		supervised learning models than KNN.
	# Cons
	#	-> It is computationally a bit expensive algorithm because it 
	#		stores all the training data.
	#	-> High memory storage required as compared to other supervised
	#		learning algorithms.
	#	-> Prediction is slow in case of big N.
	#	-> It is very sensitive to the scale of data as well as 
	#		irrelevant features.

	# Applications of KNN
	# The following are some of the areas in which KNN can be applied 
	# successfully:
	# 	-> Banking System - KNN can be used in banking system to 
	#		predict weather an individual is fit for loan approval? 
	#		Does that individual have the characteristics similar to 
	#		the defaulters one?
	#	-> Calculating Credit Ratings - KNN algorithms can be used to 
	#		find an individual’s credit rating by comparing with the 
	#		persons having similar traits.
	#	-> Politics - With the help of KNN algorithms, we can classify 
	#		a potential voter into various classes like “Will Vote”, 
	#		“Will not Vote”, “Will Vote to Party ‘Congress’, “Will Vote
	#		to Party ‘BJP’.
	# Other areas in which KNN algorithm can be used are Speech 
	# Recognition, Handwriting Detection, Image Recognition and Video 
	# Recognition.

	# Exit the program.
	exit(0)


if __name__ == '__main__':
	main()