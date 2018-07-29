# genetic_algorithm.py
#
#
# Spencer Kraisler 2018
#
#
# This file contains methods for the genetic algorithm which optimizes the AI to play blackjack. 
#
#

from blackjack import Player
from blackjack import game
from simplex import Network
import random as rand
import numpy as np


# this method creates a matrix of random values whose shape is a parameter tuple (e.g. (2,4))
def getRandMatrix(shape, limit):
	R = np.zeros(shape)
	for i in range(shape[0]):
		for j in range(shape[1]):
			R[i][j] = rand.uniform(-limit,limit)
	return R

# this method creates a matrix of random 1's and 0's the same shape as X
# the probability of a one appearing is given by the one_rate parameter
def getRandBinaryMatrix(shape, one_rate):
	B = np.zeros(shape)
	for i in range(shape[0]):
		for j in range(shape[1]):
			r = rand.random()
			if r < one_rate: B[i][j] = 1
			else: B[i][j] = 0
	return B

# takes a matrix and changes values to random ones based on the mutation rate parameter
def mutate(X, mutation_rate):
	B = getRandBinaryMatrix(X.shape, mutation_rate)
	R = getRandMatrix(X.shape, 1)
	return X + R * B

# accepts an array of SNNs (and their structure) and uses the cost function to return the best performing network 
def getMaxNetwork(network_array):
	max_network = network_array[0]
	max_network_cost = cost_blackjack(max_network)
	for i in range(len(network_array)):
		if cost_blackjack(network_array[i]) > max_network_cost:
			max_network = network_array[i]
			max_network_cost = cost_blackjack(max_network)
	return max_network

# accepts a network and randomly adds values to some weight elements in the weight matrices based on a mutation rate
def mutateNetwork(network, mutation_rate):
	mutant_network = Network(network.layers[0].dim,network.layers[1].dim,network.layers[2].dim)
	mutant_network.layers[1].weight_matrix = mutate(network.layers[1].weight_matrix, mutation_rate)
	mutant_network.layers[2].weight_matrix = mutate(network.layers[2].weight_matrix, mutation_rate)
	return mutant_network

# accepts a network and returns a metric that measures the network's performance in blackjack
def cost_blackjack(network):
	AI = Player('AI', network=network)
	stats = AI.getPlayerPerformance(10, False)
	win_rate = stats[0]
	ave_bank = stats[1]
	ave_reward = stats[2]
	cost = win_rate + ave_bank / 1000.0 + 1.1 * ave_reward
	return cost

# creates a generation of networks
# gen_size is the number of networks in generation, and h_l_s is the hidden layer size (recommended 20)
def createGeneration(gen_size, hidden_layer_size):	
	models = []
	for i in range(gen_size):
		models.append(Network(2, hidden_layer_size, 4))
	return models

# accepts a generation of networks and trains them based on a mutation rate (recommended 0.05)
# epoch is the number of training iterations for a single generation (recommeded 200)
# print_info is boolean: should it print data every 10 epochs or not 
def trainGeneration(models, epoch, mutation_rate, print_info):
	for i in range(epoch):
		max_network = getMaxNetwork(models)
		AI = Player('AI', network = max_network)
		stats = AI.getPlayerPerformance(10, False)
		win_rate = stats[0]
		ave_bank = stats[1]
		if print_info == True and i % 10 == 0: print("Epoch: " + str(i) + " - Win rate: " + str(round(win_rate * 100.0, 1)) + "% - Ave. bank (5 plays): $" + str(round(ave_bank, 2)))
		for i in range(len(models)):
			models[i] = mutateNetwork(max_network, mutation_rate * (0.70 - win_rate) / 0.70)






