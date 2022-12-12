import rospy
import math
import sys
import os


class Monopoly():
	def __init__(self):
		self.board = Board()
		self.current_space = 'Go'
		self.turn = 'player'
		self.doubleStreak = 0
		self.gameover = False
		self.pass_Go = False
		self.in_Jail = False
		self.jail_remaining = 0 # Number of turns remaining in jail
		self.money_balance = 1500 # starting cash
		
	def changeTurn(self):
		if self.turn == 'player':
			self.turn == 'robot'
		else:
			self.turn == 'player'
			
	def gameOver(self):
		# TODO: gameover if: owes money but has none (balance is negative)
		pass

	def rollDice(self):
	# TODO: implement this via IK; how to roll dice? with a cup?
		pass

	def readDice(self):
	# TODO: implement this via computer vision
	# TODO: update self.doubleStreak
		pass
	
	def takeTurn(self):
		if self.turn = 'robot' and not in_Jail:
			# Roll dice
			self.rollDice()
			dieResult = self.readDice()
			next_space = self.current_space + dieResult

			# Move piece based on die results
			self.pick(board_spaces[self.current_space], rot) # TODO: migrate this from the demo .py
			if self.doubleStreak == 3:
				# triple doubles -> go to jail!
				self.place(board_spaces['jail'], rot) # TODO: modify with coords and/or name of jail space
				self.in_Jail = True
			else:
				self.place(board_spaces[next_space], rot)
				passGo(next_space)
				self.current_space = next_space
	
				# Take action based on space
				action = self.evaluateSpace(board_spaces[current_space])
				self.transactMoney(current_space, action)

			# End of turn
			self.turn = 'player'
		else:
			print("It is not my turn")
			
	def passGo(next_space):
		if passGo == False and self.current_space + nextSpace >= 'Go':
			# TODO: improve this check; board space should be >= Go space but not trigger prematurely
			#		perhaps a simple count of total travelled spaces?
				self.money_balance = self.money_balance + 200

	def getOutOfJail(self):
		if in_Jail and jail_remaining > 0:
			pass # TODO: look up rules for getting out of jail
		else:
			self.takeTurn()

	def evaluateSpace(space):
		if space == self.board.owned[space]:
			# This is a space the bot owns; do nothing
			return 0
		elif space == self.baord.unclaimed[space]:
			# Attempt to buy an available property
			#self.purchaseProperty(space)
			return 1
		elif space == self.board.claimed[space]:
			# Another player owns this space; buy rent to owner
			return 2
		elif space == 'Community Chest':
			# draw comm. chest card
			return 3
		elif space == 'Chance':
			# draw chance card
			return 4
		elif space == 'Tax':
			# Pay money to bank
			return 5
		else:
			# Go, Free Parking, Visiting Jail; do nothing
			return 0

	def transactMoney(current_space, action):
		if action == 0:
			return # do nothing

		elif action == 1:
			self.Board.buyProperty(current_space)

		elif action == 2:
			rent = self.Board.getRent(current_space)
			self.money_balance = self.money_balance - rent
			# TODO: Give money to player
		elif action == 5:
			tax = self.BoardgetTax(current_space)
			self.money_balance = self.money_balance - tax
			# TODO: give money to bank
		elif action == 9: # TODO: refactor this number
			# Player owes BoardBot money
			rent_owned = self.Board.getRent(current_space)
			self.money_balance = self.money_balance + tax


class Board():
	def__init__(self):
		board_spaces = [] # list of all spaces with coords, TODO: possibly rent or other values?
						  # Initialize all buyable property to 'unclaimed'
		owned = []	# spaces owned by BoardBot
		unclaimed = board_spaces # TODO: trim this to remove unbuyable spaces
		claimed = [] # spaces owned by other players
		
	def getRent(space):
		# TODO: change
		# note that this may be rent other players owe BoardBot
		rent = 0
		return rent
	
	def getTax(space):
		tax = 0 # TODO: change
		return tax
	
	
	
	
if __name__=="__main__":
    main()
