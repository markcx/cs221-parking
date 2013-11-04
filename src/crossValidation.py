'''
Given large data, as a list, separate the data into training data and test data

'''

import random

def separateData(data, trainingPercent=.8):
	'''
	Given large data, as a list, separate the data into training data and test data
	trainingPercent is a number between 0 and 1 which indicate the percentage of the data to be marked as training

	'''
	numData = len(data)
	random.shuffle(data)	# randomly shuffles the data
	trainingSize = int(numData*trainingPercent)
	trainingData = data[:trainingSize]
	testData = data[trainingSize:]
	return (trainingData, testData)