"""
Author: Team 34
Project: BoardBot
Class: CS 425/426
Fall 2022/Spring 2023

This file is a collection of classes used to play the game on Monopoly.
"""

import rospy
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
        if doubles = True:
            doubleStreak = doubleStreak + 1
        else:
            doubleStreak = 0 # streak broken!
        pass
    
    def takeTurn(self):
        if self.turn == 'robot' and not in_Jail:
            # Roll dice
            self.rollDice()
            dieResult = self.readDice()
            next_space = self.current_space + dieResult

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
        board_spaces = [] # list of all spaces with coords, TODO: possibly rent or other values?
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


# This class represents property deeds that can be bought and sold
class deedCard():    
    def __init__self(name, cost, mortgage, build=yes, rentList)    
    


def main():
    # AI test: play through some turns with dummy inputs




    
if __name__=="__main__":
    main()
