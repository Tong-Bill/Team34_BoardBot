#!/usr/bin/env python

#import rospy
#import sys
#import os
#import random   
#from std_msgs.msg import String
from collections import defaultdict

board = {}
board["Boardwalk"] = [False, 0, "Blue", 270] #Owned, Owned by who, color set, price
#Just an example of the dictionary of properties. 

class MoneyExchange:
  def __init__(self):
    self.robotMoney = {500:2, 100:2, 50:2, 20:6, 10:5, 5:5, 1:5}
    self.robotMoneySum = 1500
    #Gives command to grab or count the correct amount of starting money. 
  def gainMoney(self, amount):
    self.robotMoneySum += amount
    while amount > 0:
      for i in self.robotMoney:
        if amount >= i:
          temp = amount // i
          self.robotMoney[i] += temp
            #Give command for the robot to grab the correct currency. 
          amount -= (i * temp)
        if amount == 0:
          break
    #Give command for happiness or swagger in social aspects

  def loseMoney(self, amount):
    self.robotMoneySum -= amount
    while amount < 0:
      for i in self.robotMoney:
        if amount >= i:
          temp = amount // i
          self.robotMoney[i] -= temp
            #Give command for the robot to grab the correct currency. 
          amount += (i * temp)
        if amount == 0:
          break
        #Give command for sadness or angriness in social aspects
          
class Properties(MoneyExchange):
  def __init__(self):
    self.ownedProperty = {}
    self.ownedProperty["Blue"] = [0]
  def checkPropertyOwnership(self, list): #Computer vision will pass in square 
    if list[0] == False:
      return True
    return False
  def PurchaseProperty(self, square):
    if self.checkPropertyOwnership(board[square]):
      print("Hello World")
      #Implement intellegent way to determine whether to buy the property
      #if going to buy:
        #self.loseMoney(board[square][3]) Lose the amount in the price
        #Call motion to pick up the card
        #board[square][0] = True The property is now owned
        #board[square][1] = 1 You are the owner of the property
        #self.ownedProperty[board[square][2]].append(square)
        #self.ownedProperty[board[square][2]][0] += 1
        #update the board and owned properties function
    
  #def setsComplete(self):
  #def buildHouseHotel(self):

class Jail:
  def __init__(self):
    self.card = False
    self.inJail = False
    self.bail = 50
    self.otherJail = False
    self.visiting = False

  def getOutofJail(self, card): #card here is a bool of whether the robot has the get out of jail free card.
    if self.inJail and self.card:
      self.card = False
      self.inJail = False
      #TakeTurn Function is called
    else:
      #Intelligent way of determining whether to pay the fine or roll. Rolling means you don't get another turn. 
      print("Hello World") #This is just standing in for other code. I am building the blueprint of the code.
    
#class Auction: (Potential, not necessary)
class TurnLog: #Creates a log of their turn in a txt file. (Potential but not necessary)
  def __init__(self):
    f = open("monopolyLog.txt", "w")
    
class opponentHandler(Properties): #(Includes getting and paying rent, as well as keeping track of the opponents properties)
  def __init__(self):
    self.opponentMoney = {500:2, 100:2, 50:2, 20:6, 10:5, 5:5, 1:5}
    self.opponentMoneySum = 1500
    self.opponentProperties = {}

  #def giveMoney(self):

  #def getMoney(self):

  #def cards(self):
    
  #def buyProperties(self):

  #def sellProperties(self):

  #def completeSets(self):

  #def landInJail(self):


class GameOver(Properties):
  def __init__(self):
    self.turnCount = 0
    self.turnLimit = 50
    self.bankrupt = False

  def outOfMoney(self):
    for i in self.robotMoney:
      if self.robotMoney[i] != 0:
        return False
    for i in self.ownedProperty:
      if self.ownedProperty[i][0] != 0:
        return False
    return True

  def endGame(self):
    if self.outOfMoney():
      print("Looks like I'm out of money. You win! Would you like to play again?")
      #Sadness in social aspects
      exit(-1)
    #Find a way for the robot to know that the opponent lost. 
    elif self.turnCount == self.turnLimit:
      #Compare the net worths of both players and determines who wins

#def main():
  #call roll dice
  

#if __name__ =="__main__":
  #main()
