#!/usr/bin/env python

#import rospy
#import sys
#import os
#import random   
#from std_msgs.msg import String
from collections import defaultdict

board = defaultdict(list)
board["Boardwalk"] = [False, 0, "Blue", 270] #Owned, Owned by who, color set, price
#Just an example of the dictionary of properties. 

class MoneyExchange:
  def __init__(self):
    self.robotMoney = {500:2, 100:2, 50:2, 20:6, 10:5, 5:5, 1:5}
    self.robotMoneySum = 1500
    #Gives command to grab or count the correct amount of starting money. 
    self.opponentMoney = {500:2, 100:2, 50:2, 20:6, 10:5, 5:5, 1:5}
    self.opponentMoneySum = 1500
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
    self.ownedProperty = defaultdict(list)
    self.ownedProperty["Blue"] = [0]
  def checkPropertyOwnership(self, list): #Computer vision will pass in square 
    if list[0] == False:
      return True
    return False
  def PurchaseProperty(self, square):
    if self.checkPropertyOwnership(board[square]):
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

#class Jail:

#class Auction: (Potential, not necessary)
#class TurnLog:
#class opponentHandler: (Includes getting and paying rent, as well as keeping track of the opponents properties)
    
#def main():
  #call roll dice
  

#if __name__ =="__main__":
  #main()
