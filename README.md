# blackjack_AI
A neural network created from my Simplex lbrary that can win and bet in Blackjack. 

Open up terminal and run example.py to watch the AI learn Blackjack and play 10 games! Afterwards, the file offers a user interface to allow you to play 10 games, and then your scores and banks are compared. ;)

It takes about a minute for the AI to learn and bet efficiently, incredibly faster than a human ever could. The AI learns until it reaches a 45% win rate and then levels off. It can usually make about $100.00 profit from a starting bank of $1000.00. 

The network has a 2-H-4 structure, where H is a hyperparameter. I recommend setting it to 20 nodes. The 2 input nodes repersent the current player hand score (e.g. 2 of Hearts, 3 of Spades, and King of Diamonds corresponds to a score of 15) and the current bank account divided by 1000.0 (to normalize it). The 4 output nodes represent whether the AI should hit, stay, double down, and what proportion of the player's bank it should bet.

At first the structure was 53-50-4, where the 53 input nodes were the current bank account and what cards in a 52 full deck the player had, but it took forever to learn and it oddly had a lower ceiling than the 2-20-4 network.
