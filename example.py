# example.py
#
#
# Spencer Kraisler 2018
#
#
# A simple example on how to train a network to play blackjack and then play against it yourself.
# This must be run from terminal to work. Takes about one minute to train.
#
#

from genetic_algorithm import createGeneration
from genetic_algorithm import trainGeneration
from genetic_algorithm import getMaxNetwork
from blackjack import Player
from blackjack import game

# constants
GEN_SIZE = 20
HIDDEN_LAYER_SIZE = 20
MUTATION_RATE = 0.05

# create and train generation
models = createGeneration(GEN_SIZE, HIDDEN_LAYER_SIZE)
trainGeneration(models, 200, MUTATION_RATE, True)

# creating user and AI 
gambling_addict = Player('AI', network=getMaxNetwork(models))
kayli = Player('Kayli')

# AI plays 10 games
for i in range(10):
	game(gambling_addict, 4, True)
print(1.0 * gambling_addict.wins / gambling_addict.games, gambling_addict.bank)

# user plays 10 games
for i in range(10):
	game(kayli, 4, True)
print(1.0 * kayli.wins / kayli.games, kayli.bank)
