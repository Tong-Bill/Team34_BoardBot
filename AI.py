#!/usr/bin/env python

#import rospy
#import sys
#import os
#import random
#from std_msgs.msg import String
import unittest
import random
class boardState:
  board = {1: [0, "Brown", "Mediterrean Avenue"], 
           2: [-2, "CommunityChest"],
           3: [0, "Brown", "Baltic Avenue"],
           4: [-2, "IncomeTax"],
           5: [0, "Railroad", "Reading Railroad"], 
           6: [0, "LightBlue", "Oriental Avenue"],
           7: [-2, "Chance"],
           8: [0, "LightBlue", "Vermont Avenue"], 
           9: [0, "LightBlue", "Connecticut Avenue"], 
           10:[-2, "Jail"],
           11:[0, "Magenta", "St Charles Place"],
           12:[0, "Utilities", "Electric Company"],
           13:[0, "Magenta", "States Avenue"],
           14:[0, "Magenta", "Virginia Avenue"],
           15:[0, "Railroad", "Pennsylvania Railroad"],
           16:[0, "Orange", "St James Place"],
           17:[-2, "Community Chest"],
           18:[0, "Orange", "Tennessee Avenue"],
           19:[0, "Orange", "New York Avenue"],
           20:[-2, "Free Parking"],
           21:[0, "Red", "Kentucky Avenue"],
           22:[-2, "Chance"],
           23:[0, "Red", "Indiana Avenue"],
           24:[0, "Red", "Illinois Avenue"],
           25:[0, "Railroad", "B&O Railroad"],
           26:[0, "Yellow", "Atlantic Avenue"],
           27:[0, "Yellow", "Ventnor Avenue"],
           28:[0, "Utilities", "Water Works"],
           29:[0, "Yellow", "Marvin Gardens"],
           30:[-2, "Go To Jail"],
           31:[0, "Green", "Pacific Avenue"],
           32:[0, "Green", "North Carolina Avenue"],
           33:[-2, "Community Chest"],
           34:[0, "Green", "Pennsylvania Avenue"],
           35:[0, "Railroad", "Shortline"],
           36:[-2, "Chance"],
           37:[0, "DarkBlue", "Park Place"],
           38:[-2, "Luxury Tax"],
           39:[0, "DarkBlue", "Boardwalk"],
           40:[-2, "Go"]
          }
  def __init__(self):
    self.robotMoney = {500: 2, 100: 2, 50: 2, 20: 6, 10: 5, 5: 5, 1: 5}
    self.robotMoneySum = 1500
    self.goCounter = 0
    self.ownedProperties = {"Brown":[0],
                            "LightBlue":[0],
                            "Magenta":[0],
                            "Orange":[0],
                            "Red":[0],
                            "Yellow":[0],
                            "Green":[0],
                            "DarkBlue":[0],
                            "Railroad":[0],
                            "Utilities":[0]
                           }
  

class MoneyExchange(boardState):

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
          return self.robotMoney
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
          return self.robotMoney
        #Give command for sadness or angriness in social aspects


class Properties(MoneyExchange):

  #def __init__(self):
  
  def checkPropertyOwnership(self, list):  #Computer vision will pass in square
    if list[0] == 0:
      return True
    return False

  def updateBoard(self, num, action):
    if action == "buy":
      self.board[num][0] = 1
    elif action == "sell":
      if self.board[num][0] == 1:
        self.board[num][0] = 0
  
  def PurchaseProperty(self, num):
    if self.goCounter == 0:
      if self.checkPropertyOwnership(self.board[num]):
        self.updateBoard(num, "buy")
        self.loseMoney(100)
        self.ownedProperties[self.board[num][1]][0] += 1
        self.ownedProperties[self.board[num][1]].append(self.board[num][2])
        print("I have bought " + self.board[num][2] + ".")
      #The robot will always buy on the first round of the board. 
        #Need to implement more intelligence later. 

  #def setsComplete(self):
  #def buildHouseHotel(self):


class Jail:

  def __init__(self):
    self.card = False
    self.inJail = False
    self.bail = 50
    self.otherJail = False
    self.visiting = False

  def getOutofJail(
    self, card
  ):  #card here is a bool of whether the robot has the get out of jail free card.
    if self.inJail and self.card:
      self.card = False
      self.inJail = False
      #TakeTurn Function is called
    else:
      #Intelligent way of determining whether to pay the fine or roll. Rolling means you don't get another turn.
      print(
        "Hello World"
      )  #This is just standing in for other code. I am building the blueprint of the code.


#class Auction: (Potential, not necessary)
#class TurnLog:  #Creates a log of their turn in a txt file. (Potential but not necessary)

  #def __init__(self):
    #f = open("monopolyLog.txt", "w")


class opponentHandler(
    Properties
):  #(Includes getting and paying rent, as well as keeping track of the opponents properties)

  def __init__(self):
    self.opponentMoney = {500: 2, 100: 2, 50: 2, 20: 6, 10: 5, 5: 5, 1: 5}
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
      print(
        "Looks like I'm out of money. You win! Would you like to play again?")
      #Sadness in social aspects
      exit(-1)
    #Find a way for the robot to know that the opponent lost.
    elif self.turnCount == self.turnLimit:
      print("Hello World")
      #Compare the net worths of both players and determines who wins

def rollDice():
    values = []
    values.append(random.randrange(1,6))   
    values.append(random.randrange(1,6))   
    return tuple(values)

def gameSetup():
    print("\n\nBegin setup:")
    print("Choose a banker. A human is preferred.")
    print("Each player starts with $1500.")
    # gainMoney (1500)
    print("Please shuffle the Community Chest and Chance cards, and place them facedown in their designated areas.")
    print("Choose a token. I will use my special token for easier gripping.")
    print("Roll the dice. High roll goes first.\n")
    result = rollDice()
    print("I rolled {0}\n".format(result))
  
def playerTurn():
  gameSetup()
  print("I will go first.")
  p = Properties()
  r = rollDice()
  t = r[0] + r[1]
  print("I rolled a " + str(r[0] + r[1]) + ".")
  p.PurchaseProperty(t)
  print(p.ownedProperties)
  
  
  

""""class TestMoney(unittest.TestCase):

  def testGainMoney(self):
    p = Properties()
    self.assertEqual(p.money.gainMoney(200), {
      500: 2,
      100: 4,
      50: 2,
      20: 6,
      10: 5,
      5: 5,
      1: 5
    })"""


if __name__ =="__main__":
  playerTurn()
