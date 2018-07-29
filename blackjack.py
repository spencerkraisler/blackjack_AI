# blackjack.py
#
#
# Spencer Kraisler 2018
#
#
# This file contains the methods and objects to create an interface to play blackjack.
# Both human user and AI may play the game() method.
#
#

import math
import random as rand
import numpy as np 

# minimum bet
MIN_BET = 0.0

# this class is for a single Card
# a card object contains a rank (A,2,3,...), a suit (spades, clubs, etc.), and a score ('J' => 10, 'A' => 1, '2' => 2)
class Card:
	def __init__(self, card_str):
		allowed_ranks = 'A23456789TJQK'
		allowed_suits = 'scdh'
		if card_str[0] not in allowed_ranks or card_str[1] not in allowed_suits:
			print("Card does not exist.")
		else:
			self.rank = card_str[0]
			self.suit = card_str[1]
			self.score = -1
			if self.rank in 'TJQK': self.score = 10
			elif self.rank in '23456789':self.score = int(self.rank)
			# Although an ace is a 11 or 1 in blackjack, I set the score to always be 1 for the sake of simplicity
			elif self.rank == 'A': self.score = 1 


	def __str__(self):
		return str(self.rank) + str(self.suit)

# this method returns an array of strings that are the types of a full deck of cards ('As', '2s', ..., 'Qd', 'Kd')
def getFullDeckArr():
	full_deck = [0] * 52
	for i in range(52):
		if i % 13 == 0:
			full_deck[i] = 'A'
		elif i % 13 == 9:
			full_deck[i] = 'T'
		elif i % 13 == 10:
			full_deck[i] = 'J'
		elif i % 13 == 11:
			full_deck[i] = 'Q'
		elif i % 13 == 12:
			full_deck[i] = 'K'
		else:
			full_deck[i] = str((i + 1) % 13)
	for i in range(13):
		full_deck[i] += 's'
	for i in range(13):
		full_deck[13 + i] += 'h'
	for i in range(13):
		full_deck[2 * 13 + i] += 'c'
	for i in range(13):
		full_deck[3 * 13 + i] += 'd'
	return full_deck

# this class is for a deck of cards
# a deck object contains an array of card objects
class Deck:
	def __init__(self):
		self.deck = []

	# returns a string of the cards contained within deck
	# returns 'nil' if deck is empty
	def __str__(self):
		deck_str = 'nil'
		if len(self.deck) != 0:
			deck_str = ''
			for i in range(len(self.deck) - 1):
				card = self.deck[i]
				deck_str += str(card)
				deck_str += ', '
			final_card = self.deck[len(self.deck) - 1]
			deck_str += str(final_card)
		return deck_str

	# this method appends a card object to the deck array
	def append(self, card):
		self.deck.append(card)

	# appends a full deck of card objects to the deck object
	def addFullDeck(self):
		full_deck = getFullDeckArr()
		for i in range(52):
			self.deck.append(Card(full_deck[i]))

	# returns the score of the deck (e.g. 'As', '4c', '5h' => 10 points)
	def getScore(self):
		total_score = 0
		for i in range(len(self.deck)):
			total_score += self.deck[i].score
		return total_score

	# selects a random card in the deck object, deletes it, then returns it
	def deal(self):
		r = rand.randint(0, len(self.deck) - 1)
		card = self.deck.pop(r)
		return card

# this class is for a Player of blackjack. A player has a name (string), a deck of cards, a bank to bet money
# along with total wins and total games player
# the player can be human or neural network (using my Simplex library)
class Player:
	def __init__(self, name, bank=1000, wins=0, games=0, network=None):
		self.initial_amount = bank
		self.name = name
		self.hand = Deck()
		self.bank = bank
		self.wins = wins
		self.games = games
		self.network = network
		
	def __str__(self):
		return self.name

	# takes 1 random card from the deck parameter and appends it to the player object's deck
	def hit(self, deck):
		self.hand.append(deck.deal())

	# prints the hand and score of the player object
	def printScore(self):
		print(str(self) + ' has ' + str(self.hand) + ' for a total of ' + str(self.hand.getScore()))

	# returns how much the player object will bet
	def getBet(self, print_text=True):
		if self.name == 'AI':
			if print_text == True: print(str(self) + " has $" + str(self.bank) + " in their bank.")
			input_vector = np.array([[0.0],[self.bank / 1000.0]])
			output_vector = self.network.forward(input_vector)
			bet = output_vector[3][0] * 1000
			if bet < MIN_BET:
				bet = MIN_BET
			if bet > self.bank: bet = self.bank
			if print_text == True: print("AI has bet $" + str(bet))
			return bet
		else:
			if print_text == True: print(str(self) + " has $" + str(self.bank) + " in their bank.")
			# to make while loop work
			if print_text == True: bet = raw_input("How much would " + str(self) + " like to bet? ").lower()
			else: bet = raw_input('').lower()
			bet = int(bet)
			if bet < MIN_BET:
				bet = MIN_BET
			if bet > self.bank: bet = self.bank
			if print_text == True: print(str(self) + " has bet $" + str(bet))
			return bet

	# returns whether the player object wants to hit, stay, or double down in the form of a single character
	def getChoice(self, print_text=True):
		if self.name == 'AI':
			input_vector = np.array([[self.hand.getScore() / 21.0], [self.bank / 1000.0]])
			output_vector = self.network.forward(input_vector)
			if output_vector[0][0] > output_vector[1][0] and output_vector[0][0] > output_vector[2][0]: return 'h'
			elif output_vector[1][0] > output_vector[0][0] and output_vector[1][0] > output_vector[2][0]: return 's'
			elif output_vector[2][0] > output_vector[0][0] and output_vector[2][0] > output_vector[1][0]: return 'd'
		else:
			if print_text == True: return raw_input("Does " + str(self) + " want to [H]it, [S]tay, or [D]ouble down? ").lower()
			else: return raw_input('').lower()

	def getPlayerPerformance(self, rounds, print_info):
		win_rate = 0
		ave_bank = 0
		ave_reward = 0
		for rounds in range(rounds):
			self.wins = 0
			self.games = 0
			self.bank = 1000.0
			for games in range(5):
				ave_reward += game(self, 4, False)
			win_rate += 1.0 * self.wins / self.games
			ave_bank += self.bank
		win_rate /= rounds 
		ave_bank /= rounds
		ave_reward /= (rounds * 5)
		if print_info == True: print("Win rate: " + str(win_rate * 100.0) +"% - Bank: $" + str(round((ave_bank), 2) + " - Ave. reward: " + str(ave_reward)))
		return win_rate, ave_bank, ave_reward

	def getPlayerStatus(self):
		if str(self) != 'Dealer':
			if self.hand.getScore() == 21: return 'BLACKJACK'
			elif self.hand.getScore() > 21: return 'BUST'
			else: return 'ALIVE'
		else:
			if self.hand.getScore() >= 17 and self.hand.getScore() < 21 : return 'STOP_DEALER'
			elif self.hand.getScore() == 21: return 'BLACKJACK'
			elif self.hand.getScore() > 21: return 'BUST'
			else: return 'ALIVE'

# this method is a bit incomplete
# prints the end game results (e.g. 'dealer hit blackjack', 'player busts', etc.)
def printGameResults(player, dealer):
	if player.getPlayerStatus() == 'BLACKJACK':
		print(str(player) + " got blackjack! " + str(player) + " wins!")
	elif dealer.getPlayerStatus() == 'BLACKJACK':
		print("Dealer got blackjack. " + str(player) + " loses.")
	elif player.getPlayerStatus() == 'BUST':
		print(str(player) + " busted. " + str(player) + " loses.")

	elif dealer.getPlayerStatus() == 'BUST':
		print("Dealer busted! " + str(player) + " wins!")
	elif player.hand.getScore() > dealer.hand.getScore():
		print(str(player) + " got a higher score than the dealer! " + str(player) + " wins!")
	elif player.hand.getScore() < dealer.hand.getScore():
		print("Dealer got a higher score than " + str(player) + ". " + str(player) + " loses.")
	elif player.hand.getScore() == dealer.hand.getScore():
		print("Draw.")
	print(str(player) + " now has $" + str(player.bank))

# returns the reward of a game played
# this method is for the genetic algorithm
# essentailly, the closer the player was to 21, the higher its score
def getReward(player_score, dealer_score, choice):
	if choice == 'h':
		if player_score == 21:
			return 1.0
		else:
			return 0.7
	elif choice == 's':
		if player_score == 21:
			return 1.0
		elif player_score >= dealer_score and dealer_score < 21:
			return 1.0
		elif dealer_score > 21:
			return (player_score) / 21.0
		elif dealer_score > player_score:
			return (player_score) / 21.0
	elif choice == 'd':
		if player_score == 21:
			return 1.0
		elif player_score > 21:
			return 0.7
		elif player_score >= dealer_score and dealer_score < 21:
			return 1.0
		elif dealer_score > player_score:
			return (player_score) / 21.0

# this method prints a UI for playing blackjack
# returns the reward of the player
def game(player, deck_count, print_text=True):
	dealer = Player('Dealer')

	# shoe will have two full decks
	shoe = Deck()
	for i in range(deck_count):
		shoe.addFullDeck()

	if print_text==True: print("\nWELCOME TO BLACKJACK!")

	# get inital bet
	bet = player.getBet(print_text)
	player.bank -= bet
	dealer.hit(shoe)
	player.hit(shoe)
	dealer.hit(shoe)
	player.hit(shoe)

	if print_text == True: player.printScore()

	gameEnded = False
	while gameEnded == False:
		choice = player.getChoice(print_text)

		if choice == 'h':
			player.hit(shoe)
			if print_text == True:
				print(str(player) + " chose to hit.")
				player.printScore()
			player_status = player.getPlayerStatus()

			if player_status != 'ALIVE':
				if print_text == True: printGameResults(player, dealer)
				if player_status == 'BLACKJACK':
					player.bank += 1.5 * bet # player wins and gets 1.5 times its bet back
					player.wins += 1
				elif player.hand.getScore() == dealer.hand.getScore():
					player.bank += bet # player tied, so it only gets its bet back
				gameEnded = True
		elif choice == 'd':
			if print_text == True: print(str(player) + " chose to double down.")
			if player.bank < bet:
				bet += player.bank
				player.bank = 0
			else:
				player.bank -= bet
				bet *= 2 # doubled down
			if print_text == True: print(str(player) + " now has $" + str(player.bank) + " in their bank.")
			player.hit(shoe)
			if print_text == True: player.printScore()
			if player.hand.getScore() > 21:
				if print_text == True: 
					print(str(player) + " doubled down and busted. " + str(player) + " loses.")
					print(str(player) + " now has $" + str(player.bank) + " in their bank.")
			else:
				dealer_status = dealer.getPlayerStatus()
				while dealer_status == 'ALIVE':
					dealer.hit(shoe)
					dealer_status = dealer.getPlayerStatus()
				if print_text == True: dealer.printScore()
				if (player.hand.getScore() > dealer.hand.getScore() and dealer.hand.getScore() < 21) or dealer_status == 'BUST':
					player.bank += 1.5 * bet
					player.wins += 1
				elif dealer_status == 'BUST':
					player.bank += 1.5 * bet
					player.wins += 1
				elif dealer.hand.getScore() > player.hand.getScore():
					if print_text == True: print(str(player) + " got less than the dealer. " + str(player) + " loses.")
				else:
					if print_text == True: print("Draw.")
					player.bank += bet
			if print_text == True: print(str(player) + " now has $" + str(player.bank) + " in their bank.")
			gameEnded = True

		elif choice == 's':
			if print_text == True: print(str(player) + " chose to stay.")
			dealer_status = dealer.getPlayerStatus()
			while dealer_status == 'ALIVE':
				dealer.hit(shoe)
				dealer_status = dealer.getPlayerStatus()
			if print_text == True: dealer.printScore()
			if dealer_status == 'BUST' or dealer.hand.getScore() < player.hand.getScore():
				player.bank += 1.5 * bet
				player.wins += 1
			elif dealer.hand.getScore() == player.hand.getScore():
				player.bank += bet # a draw results in player receiving his bet back (profit = $0)
			if print_text == True: printGameResults(player, dealer)
			gameEnded = True
		elif print_text == True: print("Please enter valid command.")
	if print_text == True: print('******')
	reward = getReward(player.hand.getScore(), dealer.hand.getScore(), choice)
	player.hand = Deck()	
	player.games += 1
	return reward


