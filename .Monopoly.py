""" 
7 Mar 2023 Update:
This file is deprecated and its functionality has been split between AI.py and rules.py. 
It is no longer under development.

This file will be retained for reference for now.
"""





"""
Author: Team 34
Project: BoardBot
Class: CS 425/426
Fall 2022/Spring 2023

This file is a collection of classes used to play the game on Monopoly.
"""

#import rospy
import math
import sys
import os


# This class is the rule-enforcement/AI
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
        if money_balance <=0:
            # TODO: attempt to sell houses/hotels
            # TODO: attempt to mortgage properties

            # If both of these fail, BoardBot has lost!
            self.gameover = True

    def rollDice(self):
    # TODO: implement this via IK; how to roll dice? with a cup?
        pass

    def readDice(self):
    # TODO: implement this via computer vision
        doubles = False # set to True based on results: die_1 == die_2
        if doubles == True:
            doubleStreak = doubleStreak + 1
        else:
            doubleStreak = 0 # streak broken!
        pass
    
    def takeTurn(self, num1, num2):
        print("Beginning my turn")
        if self.turn == 'robot' and not in_Jail:
            # Roll dice
            if num1 and num2:
                # For testing/debug purposes
                dieResult = [num1, num2]
            else:
                self.rollDice()
                dieResult = self.readDice()
            next_space = self.current_space + dieResult[0] + dieResult[1]

            # Move piece based on die results
            self.pick(board_spaces[self.current_space], rot) # TODO: migrate this from the demo .py
            if self.doubleStreak == 3:
                # triple doubles -> go to jail!
                goToJail()
            else:
                self.place(board_spaces[next_space], rot)
                passGo(next_space)
                self.current_space = next_space
    
                # Take action based on space
                self.evaluateSpace(board_spaces[current_space])

            # End of turn
            self.turn = 'player'

        elif self.turn == 'robot':
            getOutOfJail()
            self.turn = 'player'

        else:
            print("It is not my turn")
            
    def passGo(next_space):
        if passGo == False and self.current_space + nextSpace >= 'Go':
            # TODO: improve this check; board space should be >= Go space but not trigger prematurely
            #       perhaps a simple count of total travelled spaces?
                self.money_balance = self.money_balance + 200

    def goToJail(self):
                self.place(board_spaces['jail'], rot) # TODO: modify with coords and/or name of jail space
                jail_remaining = 3 # spend a max of 3 turns in jail
                self.in_Jail = True


    def getOutOfJail(self):
        if in_Jail and jail_remaining > 0:
            # Option 1: Pay money
            if self.money_balance > 500:
                self.money_balance = self.money_balance - 50
                # TODO: move piece to "just visitng"
                in_jail = False
                jail_remaining = 0

            elif 'Get Out of Jail Free' in self.cards:
                in_jail = False
                jail_remaining = 0
                pass # Use card to get out of jail

            else:
                rollDice()
                dieResults = readDice()
                if dieResults[0] == dieResults[1]: # doubles!
                    in_jail = False
                    jail_remaining = 0
                else: # still in jail
                    jail_remaining = jail_remaining - 1
        else:
            self.takeTurn() # TODO: consider refactoring this line

    def evaluateSpace(self, space):
        if space == self.board.owned[space]:
            # This is a space the bot owns; do nothing
            return
        elif space == self.board.unclaimed[space]:
            # Attempt to buy an available property
            transactMoney(space, 1)
        elif space == self.board.claimed[space]:
            # Another player owns this space; buy rent to owner
            transactMoney(space, 2)
        elif space == 'Community Chest':
            # draw comm. chest card
            drawCard(2)
        elif space == 'Chance':
            # draw chance card
            drawCard(1)
        elif space == 'Tax':
            # Pay money to bank
            transactMoney(space, 5)
        elif space == 'Go To Jail':
            goToJail()
        else:
            # Go, Free Parking, Visiting Jail; do nothing
            return

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

    # Draw the top card of chance or community chest
    def drawCard(card):
        if card == 1:
            getChance()
        elif card == 2:
            getCommChest()


# This class tracks board state, such as who owns which properties
class Board():
    def __init__(self):
        # Consider storing board space info in a DB
                                #       Name            cost  card_set      rent_list           build_cost
        board_spaces = [deedCard('Mediterranean Avenue', 60, 'Brown', [2, 4, 10, 30, 90, 160, 250], 50),
                        ['Baltic Avenue', 60, 'Brown', [4, 8, 20, 60, 180, 320, 450], 50],
                        ['Reading RailRoad', 200,'RR', [25, 50, 100, 200], 0, False],
                        ['Oriental Avenue', 100, 'Light Blue', [6, 12, 30, 90, 270, 400, 550], 50],
                        ['Vermont Avenue', 100, 'Light Blue', [6, 12, 30, 90, 270, 400, 550], 50],
                        ['Connecticut Avenue', 120, 'Light Blue', [8, 16, 40, 100, 300, 450, 600], 50]] 
                        # list of all spaces with coords, TODO: possibly rent or other values?
                        # Initialize all buyable property to 'unclaimed'
        owned = []  # spaces owned by BoardBot
        unclaimed = board_spaces # TODO: trim this to remove unbuyable spaces
        claimed = [] # spaces owned by other players
        
    def getRent(space):
        # TODO: change
        
        rent = 0
        return rent
    
    def getTax(space):
        tax = 0 # TODO: change
        return tax

    def buySpace(space):
        if space not in unclaimed:
            print("Error: land %s cannot be bought" % space)
        else:
            # TODO: deduct cost from balance
            unclaimed.remove(space)
            owned.append(space)
            print("Bought %s" % space)


# This class represents property deeds that can be bought and sold
class deedCard():    
    def __init__(self, name, cost, card_set, rent_list, build_cost, buildable = True, is_mortgaged = False, mortgage = cost * 0.5, num_houses = 0, hotel = 0, in_set = False): 
        self.name = name
        self.cost = cost
        self.mortgage = mortgage
        self.is_mortgaged = is_mortgaged
        self.card_set = card_set
        self.buildable = buildable
        self.rent_list = rent_list
        # RentList: [base], [set], [1 House] ... [4 house], [hotel]
        self.build_cost = build_cost
        self.num_houses = 0
        self.hotel = 0
        self.in_set = False

    def rent(self, in_set = False):
        if is_mortgaged:
            return 0

        if not in_set:
            return rent_list[0]
        elif in_set and num_houses == 0 and hotel == 0:
            return rent_list[1]
        elif in_set and num_houses == 1:
            return rent_list[2]
        elif in_set and num_houses == 2:
            return rent_list[3]
        elif in_set and num_houses == 3:
            return rent_list[4]
        elif in_set and num_houses == 4:
            return rent_list[5]
        elif in_set and hotel == 1:
            return rent_list[6]
        else:
            print("Error: invalid rent of %s" % name)
            return 0

    def buildHouse(self):
        if not in_set:
            print("Error: Cannot build a house on %s because it is not in a set" % name)
            return
        elif 1 == 1 and num_houses < 4:
        # TODO: need a mechanism to check balance BEFORE committing to a buy- probably just call a method in Monopoly class
        # TODO: add a check to ensure that sufficent houses remain in supply BEFORE committing to a buy
            num_houses = num_houses + 1
        else:
            print("Error: Cannot build a house on %s because it already has the maximum amount of houses." % name)
            
    def buildHotel(self):
        if not in_set:
            print("Error: Cannot build a hotel on %s because it is not in a set" % name)
            return
        elif 1 == 1 and num_houses == 4:
        # TODO: need a mechanism to check balance BEFORE committing to a buy- probably just call a method in Monopoly class
        # TODO: add a check to ensure that sufficent hotels remain in supply BEFORE committing to a buy
            hotel = 1
        elif 1==1 and num_houses < 4:
            print("Error: Cannot build a hotel on %s because it does not have 4 houses." % name)

        else:
            print("Error: Cannot build a hotel on %s" % name)

    def mortgageProperty(self):
        is_mortgaged = True

    def getCost(self):
        return cost
     


# This class represents chance or community chest cards
class randomCard():
    def __init__(self, cardType, name, text, possess=False):
        self.cardType = cardType
        self.name = name
        self.text = text
        self.possess = possess

    def readCard(self):
        return self.text



def main():
    # AI test: play through some turns with dummy inputs
    # TODO: will likely pass messages between classes pub/sub-style
    AI = Monopoly()
    AI.takeTurn(1, 2)



    
if __name__=="__main__":
    main()
