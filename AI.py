#!/usr/bin/env python
#Main Author: Yee Hong Tham
import rules
import subprocess
import trump
from time import sleep
import random as rd
from std_msgs.msg import (Int16, String, Int16MultiArray)
import rospy
import roslibpy     # for web integration
from gtts import gTTS
import os
#Some commented out code is made using match/case, which is Python 3.10, which is too high of a version for Baxter. I kept it in here as it is code I have written. 

#new Board which is a dict that is [type of square, color/name, name, weight]. Weight is used for selling properties and is found using data online on which properties are the most valuable.
    
class board(rules.BoardSpaces, rules.TitleDeedCards):
  Board = {
    0: [-2, "Go"],
    1: [0, "Brown", "Mediterranean Avenue"],
    2: [-2, "Community Chest"],
    3: [0, "Brown", "Baltic Avenue"],
    4: [-2, "IncomeTax"],
    5: [0, "Railroad", "Reading Railroad"],
    6: [0, "LightBlue", "Oriental Avenue"],
    7: [-2, "Chance"],
    8: [0, "LightBlue", "Vermont Avenue"],
    9: [0, "LightBlue", "Connecticut Avenue"],
    10: [-2, "Jail"],
    11: [0, "Magenta", "St Charles Place"],
    12: [0, "Utilities", "Electric Company"],
    13: [0, "Magenta", "States Avenue"],
    14: [0, "Magenta", "Virginia Avenue"],
    15: [0, "Railroad", "Pennsylvania Railroad"],
    16: [0, "Orange", "St James Place"],
    17: [-2, "Community Chest"],
    18: [0, "Orange", "Tennessee Avenue"],
    19: [0, "Orange", "New York Avenue"],
    20: [-2, "Free Parking"],
    21: [0, "Red", "Kentucky Avenue"],
    22: [-2, "Chance"],
    23: [0, "Red", "Indiana Avenue"],
    24: [0, "Red", "Illinois Avenue"],
    25: [0, "Railroad", "B&O Railroad"],
    26: [0, "Yellow", "Atlantic Avenue"],
    27: [0, "Yellow", "Ventnor Avenue"],
    28: [0, "Utilities", "Water Works"],
    29: [0, "Yellow", "Marvin Gardens"],
    30: [-2, "Go To Jail"],
    31: [0, "Green", "Pacific Avenue"],
    32: [0, "Green", "North Carolina Avenue"],
    33: [-2, "Community Chest"],
    34: [0, "Green", "Pennsylvania Avenue"],
    35: [0, "Railroad", "Shortline"],
    36: [-2, "Chance"],
    37: [0, "DarkBlue", "Park Place"],
    38: [-2, "Luxury Tax"],
    39: [0, "DarkBlue", "Boardwalk"],
  }

  def __init__(self, player=False):
    self.isPlayer = player
    self.currPos = 0
    self.playerPos = 0
    self.turnCounter = 10 # TODO: Is this outdated? Seems like this should be removed
    #numPlayers = input("How many players are playing?: ")
    self.numPlayers = 1
    self.weights = {
      "Brown": 0.2,
      "Railroad": 0.8,
      "LightBlue": 0.3,
      "Magenta": 0.4,
      "Orange": 0.9,
      "Red": 1,
      "Yellow": 0.6,
      "Green": 0.5,
      "DarkBlue": 0.7
    }
  def namingShortcut(self):
    x = self.currPos
    if self.isPlayer == True:
      x = self.playerPos
    self.space = x
    self.square = self.Board[x][0]
    if self.square == -2:
      self.name = self.Board[x][1]
    else:
      self.color = self.Board[x][1]
      self.name = self.Board[x][2]
      self.price = self.board[x][3]

  def updatePosition(self, sum):
    movement = 0
    if(self.isPlayer == False):
        while movement != 2:
            movement = rospy.wait_for_message("moveState", Int16).data
    #global
    self.move = sum
    if self.isPlayer == True:
      if self.playerInJail == True:
        return
      else:
        self.playerPos += sum
        if self.playerPos >= 40:
          self.playerPos -= 40
          self.passGo()
    else:
      if self.robotInJail == True:
        return
      else:
        self.currPos += sum
        try:
          if not rospy.is_shutdown():
            print("debugging pub probs in updatePosition\n")
            #writePublisher(sum) # Publish diceroll to motion planner 
        except:
          print("Error! Could not publish 'updatePosition'")
        if self.currPos >= 40:
          self.currPos -= 40
          self.passGo()

    self.namingShortcut()

    if self.square == -2: # -2: this space cannot be bought (Go, Jail, etc.)
      if self.isPlayer == False:
        #Say what square it lands on.
        print("I landed on " + self.name)
      else:
        print("You've landed on " + self.name)

      if self.name == "Community Chest":
        print("Pulling card")
        self.pullCard(self.name)
      elif self.name == "Chance":
        self.pullCard(self.name)
      elif self.name == "IncomeTax":
        if self.isPlayer == False:
          self.giveMoney(min(200, self.robotMoneySum * 0.1))
        else:
          self.giveMoney(min(200, self.playerMoneySum * 0.1))
      elif self.name == "Go To Jail":
        self.goToJail()
      elif self.name == "Luxury Tax":
        self.giveMoney(75)

    else:
      if self.isPlayer == False:
        print("I landed on " + self.name)
        if self.square == -1:
          self.payRent()
      else:
        print("You've landed on " + self.name)
        if self.square == 1:
          self.payRent()

  def updateOwnership(self, change):
    self.namingShortcut()

    if change == "buy":
      self.Board[self.currPos][0] = 1

    elif change == "sell" or change == "oppSell":
      self.Board[self.currPos][0] = 0

    elif change == "oppBuy":
      self.Board[self.playerPos][0] = -1
    print("Board state updated.")

class Assets(board):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.robotMoney = {500: 2, 100: 2, 50: 2, 20: 6, 10: 5, 5: 5, 1: 5}
    self.playerMoney = {500: 2, 100: 2, 50: 2, 20: 6, 10: 5, 5: 5, 1: 5}
    self.robotMoneySum = 1500
    self.playerMoneySum = 1500

    self.ownedProperties = {
      "Brown": {
        "Mediterranean Avenue": [False, 0, False],
        "Baltic Avenue": [False, 0, False]
      },
      "LightBlue": {
        "Oriental Avenue": [False, 0, False],
        "Vermont Avenue": [False, 0, False],
        "Connecticut Avenue": [False, 0, False]
      },
      "Magenta": {
        "St Charles Place": [False, 0, False],
        "States Avenue": [False, 0, False],
        "Virginia Avenue": [False, 0, False]
      },
      "Orange": {
        "St James Place": [False, 0, False],
        "Tennessee Avenue": [False, 0, False],
        "New York Avenue": [False, 0, False]
      },
      "Red": {
        "Kentucky Avenue": [False, 0, False],
        "Indiana Avenue": [False, 0, False],
        "Illinois Avenue": [False, 0, False]
      },
      "Yellow": {
        "Atlantic Avenue": [False, 0, False],
        "Ventnor Avenue": [False, 0, False],
        "Marvin Gardens": [False, 0, False]
      },
      "Green": {
        "Pacific Avenue": [False, 0, False],
        "North Carolina Avenue": [False, 0, False],
        "Pennsylvania Avenue": [False, 0, False]
      },
      "DarkBlue": {
        "Park Place": [False, 0, False],
        "Boardwalk": [False, 0, False]
      },
      "Railroad": {
        "Reading Railroad": [False, 0, False],
        "Pennsylvania Railroad": [False, 0, False],
        "B&O Railroad": [False, 0, False],
        "Shortline": [False, 0, False]
      },
      "Utilities": {
        "Electric Company": [False, 0, False],
        "Water Works": [False, 0, False]
      },
    }

    self.playerOwnedProperties = {
      "Brown": {
        "Mediterranean Avenue": [False, 0, False],
        "Baltic Avenue": [False, 0, False]
      },
      "LightBlue": {
        "Oriental Avenue": [False, 0, False],
        "Vermont Avenue": [False, 0, False],
        "Connecticut Avenue": [False, 0, False]
      },
      "Magenta": {
        "St Charles Place": [False, 0, False],
        "States Avenue": [False, 0, False],
        "Virginia Avenue": [False, 0, False]
      },
      "Orange": {
        "St James Place": [False, 0, False],
        "Tennessee Avenue": [False, 0, False],
        "New York Avenue": [False, 0, False]
      },
      "Red": {
        "Kentucky Avenue": [False, 0, False],
        "Indiana Avenue": [False, 0, False],
        "Illinois Avenue": [False, 0, False]
      },
      "Yellow": {
        "Atlantic Avenue": [False, 0, False],
        "Ventnor Avenue": [False, 0, False],
        "Marvin Gardens": [False, 0, False]
      },
      "Green": {
        "Pacific Avenue": [False, 0, False],
        "North Carolina Avenue": [False, 0, False],
        "Pennsylvania Avenue": [False, 0, False]
      },
      "DarkBlue": {
        "Park Place": [False, 0, False],
        "Boardwalk": [False, 0, False]
      },
      "Railroad": {
        "Reading Railroad": [False, 0, False],
        "Pennsylvania Railroad": [False, 0, False],
        "B&O Railroad": [False, 0, False],
        "Shortline": [False, 0, False]
      },
      "Utilities": {
        "Electric Company": [False, 0, False],
        "Water Works": [False, 0, False]
      },
    }
    self.robotOwnedProperty, self.playerOwnedProperty = [], []
    self.robotNumProperties, self.playerNumProperties = 0, 0
    self.house, self.playerHouse, self.hotel, self.playerHotel = 0, 0, 0, 0
    self.playerAssets, self.robotAssets = 1500, 1500
    self.ownedSets, self.playerOwnedSets = set(), set()
    self.listOfCC = rd.sample(range(1, 17), 16)
    self.listOfChance = rd.sample(range(1, 17), 16)
    self.robotMortgaged, self.playerMortgaged = [], []

  def gainMoney(self, amount):
    global server
    global webRobotInfoPublisher
    global webPlayerInfoPublisher
    if self.isPlayer == False:
      self.robotMoneySum += amount
      moneyMsg = roslibpy.Message({'data': (self.robotMoneySum)}) # send info to web UI
      webRobotInfoPublisher.publish(moneyMsg)
      while amount > 0:
        for i in self.robotMoney:
          if amount >= i:
            temp = amount // i
            self.robotMoney[i] += temp
            #Give command for the robot to grab the correct currency.
            amount -= (i * temp)
          if amount == 0:
            return
    else:
      # TODO: If this is the player gaining money, then Web UI should reflect this
      self.playerMoneySum += amount
      moneyMsg = roslibpy.Message({'data': (self.playerMoneySum)}) # send info to web UI
      webPlayerInfoPublisher.publish(moneyMsg)
      while amount > 0:
        for i in self.playerMoney:
          if amount >= i:
            temp = amount // i
            self.playerMoney[i] += temp
            #Give command for the robot to grab the correct currency.
            amount -= (i * temp)
          if amount == 0:
            return
  """def webPublisher(self):
    client = roslibpy.Ros(host='134.197.95.215', port=9090)
    client.run()
    moneyTalker = roslibpy.Topic(client, '/Assets', 'std_smgs/String')
    #propTalker = roslibpy.Topic(server, '/Assets', 'std_smgs/String')
    if client.is_connected:
      print("True")
      moneyTalker.publish(roslibpy.Message({'data': str(self.robotMoneySum)}))
      #propTalker.publish(roslibpy.Message({'data': str(self.robotOwnedProperties)}))
    client.terminate()"""
  # Used to calcuate change for cash  
  def closest(self, value):
    cash = []
    if self.isPlayer == False:
      for k in self.robotMoney:
        if self.robotMoney[k] > 0:
          cash.append(k)
    else:
      for k in self.playerMoney:
        if self.playerMoney[k] > 0:
          cash.append(k)
    return cash[min(range(len(cash)), key = lambda i: abs(cash[i] - value))]
    
  def giveMoney(self, amount):
    global server
    global webRobotInfoPublisher
    global webPlayerInfoPublisher
    if self.isPlayer == False:
      self.robotMoneySum -= amount
      if self.robotMoneySum >= 0:
        while amount > 0:
          x = self.closest(amount)
          amount = self.payAmount(x, amount)
          if amount < 0:
            self.gainMoney(amount * -1)
            self.robotMoneySum += amount
            moneyMsg = roslibpy.Message({'data': (self.robotMoneySum)}) # send info to web UI
            webRobotInfoPublisher.publish(moneyMsg)
            return
          elif amount == 0:
            moneyMsg = roslibpy.Message({'data': (self.robotMoneySum)}) # send info to web UI
            webRobotInfoPublisher.publish(moneyMsg)
            return
      else:
        return -1
          
    else:
      self.playerMoneySum -= amount
      while amount > 0:
        x = self.closest(amount)
        try:
          amount = self.payAmount(x, amount)
        except:
          print("Error!")
        if amount < 0:
          self.gainMoney(amount * -1)
          self.playerMoneySum += amount
          moneyMsg = roslibpy.Message({'data': (self.playerMoneySum)}) # send info to web UI
          webPlayerInfoPublisher.publish(moneyMsg)
          return
        elif amount == 0:
          moneyMsg = roslibpy.Message({'data': (self.playerMoneySum)}) # send info to web UI
          webPlayerInfoPublisher.publish(moneyMsg)
          return
          
  def numHouses(self, color, name):
    if self.isPlayer == False:
      return self.ownedProperties[color][name][1]
    return self.playerOwnedProperties[color][name][1]
    

  def payAmount(self, value, amount):
    if self.isPlayer == False:
      if self.robotMoney[value] > 0:
        self.robotMoney[value] -= 1
        amount -= value
    else:
      if self.playerMoney[value] > 0:
        self.playerMoney[value] -= 1
        amount -= value
    return amount
    
  def isASet(self, color):
    if self.isPlayer == False:
      for name in self.ownedProperties[color]:
        if self.ownedProperties[color][name][0] == False:
          return False
      return True
    else:
      for name in self.playerOwnedProperties[color]:
        if self.playerOwnedProperties[color][name][0] == False:
          return False
      return True

  def hasMortgaged(self, color):
    if self.isPlayer == True:
      for name in self.playerOwnedProperties[color]:
        if self.playerOwnedProperties[color][name][2] == True:
          return True
    else:
      for name in self.ownedProperties[color]:
        if self.ownedProperties[color][name][2] == True:
          return True
    return False
    
  def propMortgaged(self, color, name):
    if self.isPlayer == True:
      if self.playerOwnedProperties[color][name][2] == True:
        return True
    else:
      if self.ownedProperties[color][name][2] == True:
        return True
    return False


class Actions(Assets, rules.ChanceCommunityCards, rules.TitleDeedCards):

  def passGo(self):
    self.gainMoney(200)

  def buy(self):
    global webRobotPropertyPublisher
    global webPlayerPropertyPublisher
    self.namingShortcut()
    if self.square == 0:
      if self.isPlayer == False:
        self.leftoverMoney = self.robotMoneySum - self.price
        if self.leftoverMoney >= 350:
          self.updateOwnership("buy")
          self.giveMoney(self.price)
          self.ownedProperties[self.color][self.name][0] = True
          self.robotOwnedProperty.append(self.name)
          tempString = ', '.join(self.robotOwnedProperty) # Collapse list into string
          propMsg = roslibpy.Message({'data': tempString})
          webRobotPropertyPublisher.publish(propMsg) # Update web UI with property info
          self.robotNumProperties += 1
          # - BILL TONG
          #Social aspect here, saying that they bought xxx property.
          if self.isASet(self.color):
            self.ownedSets.add(self.color)

      else::
        self.leftoverMoney = self.playerMoneySum - self.price
        if self.leftoverMoney >= 350:
          self.updateOwnership("oppBuy")
          self.giveMoney(self.price)
          self.playerOwnedProperties[self.color][self.name][0] = True
          self.playerOwnedProperty.append(self.name)
          self.playerNumProperties += 1
          tempString = ', '.join(self.playerOwnedProperty) # Collapse list into string
          propMsg = roslibpy.Message({'data': tempString})
          webPlayerPropertyPublisher.publish(propMsg) # Update web UI with property info

          if self.isASet(self.color):
            self.playerOwnedSets.add(self.color)

  def buyHouse(self, color):
    prop = dict()
    if self.isPlayer == False and self.isASet(color) and self.hasMortgaged(
        color) == False:
      for name in self.ownedProperties[color]:
        prop[name] = self.ownedProperties[color][name][1]
      most_houses = max(prop.values())
      if all(value == most_houses for value in prop.values()):
        house = rd.choice(list(prop.keys()))
        self.addHouse(color, house)
        #Social Here, bragging about buying the house
      else:
        least_houses = min(prop.values())
        min_keys = [m for m in prop if prop[m] == least_houses]
        key = rd.choice(min_keys)
        self.addHouse(color, key)

    elif self.isPlayer and self.isASet(color) and not self.hasMortgaged(color):
      
      for name in self.playerOwnedProperties[color]:
        prop[name] = self.playerOwnedProperties[color][name][1]
      for key, value in prop.items():
        if value <= 4:
          print("There are " + str(value) + " houses on " + key)
        else:
          print("There is a hotel on " + key)
      choice = input("Choose Property: ")
      print("It will cost " + str(self.cards[choice][3]))
      if choice in prop.keys():
        most_houses = max(prop.values())
        if all(v == most_houses for v in prop.values()):
          self.addHouse(color, choice)
        else:
          least_houses = min(prop.values())
          if prop[choice] == least_houses:
            self.addHouse(color, choice)
          else:
            print("Please distribute the houses evenly!")
            return
            
  def addHouse(self, color, choice):
    price = self.robotMoneySum - self.getBuildCost(choice)

    if price >= 350 and self.isPlayer == False:
      print("Adding a house to " + choice)
      self.giveMoney(self.cards[choice][3])
      self.ownedProperties[color][choice][1] += 1
      self.house += 1

    elif self.isPlayer == True:
      print("Adding a house to " + choice)
      self.giveMoney(self.cards[choice][3])
      self.playerOwnedProperties[color][choice][1] += 1
      self.playerHouse += 1
      
  def sellHouse(self):
    prop = {}
    if not self.isPlayer:
      wgt = {k: v for k, v in sorted(self.weights.items(), key=lambda item: item[1])}
      for color in self.ownedSets: 
        prop[color] = {}
        
      for color in prop:
        for name in self.ownedProperties[color]:
          if self.ownedProperties[color][name][1] > 0:
            prop[color][name] = self.ownedProperties[color][name][1]
      worst = ""
      x = float("inf")
      for color in prop: 
        if wgt[color] < x:
          x = wgt[color]
          worst = color
      most_houses = max(prop[worst].values())
      if all(value == most_houses for value in prop[worst].values()):
        house = rd.choice(list(prop[worst].keys()))
        self.removeHouse(worst, house)
      else:
        most_keys = [m for m in prop if prop[worst][m] == most_houses]
        key = rd.choice(most_keys)
        self.removeHouse(worst, key)
    else:
      for color in self.playerOwnedSets: 
        prop[color] = {}
        
      for color in prop:
        for name in self.playerOwnedProperties[color]:
          if self.playerOwnedProperties[color][name][1] > 0:
            prop[color][name] = self.playerOwnedProperties[color][name][1]
      print(prop)
      choice = input("Which house would you like to sell?: ")
      for color in prop:
        if choice in prop[color]:
          most_house = prop[color].values()
          if prop[self.returnColor(choice)][choice] == most_house:
            self.removeHouse(self.returnColor(choice), choice)

      
  def removeHouse(self, color, choice):
    if self.isPlayer == False:
      print("Selling a house from " + str(choice))
      self.gainMoney(self.cards[choice][3])
      self.ownedProperties[color][choice][1] -= 1
      self.house -= 1

    elif self.isPlayer == True:
      print("Selling a house from " + str(choice))
      self.gainMoney(self.cards[choice][3])
      self.playerOwnedProperties[color][choice][1] -= 1
      self.playerHouse -= 1  
  def mortgage(self):
    # TODO: If player's choice, present this via Web UI
    prop = dict()
    if self.isPlayer == True:
      for color in self.playerOwnedProperties:
        if color not in prop:
          prop[color] = []
        if color in self.playerOwnedSets:
          for name in self.playerOwnedProperties[color]:
            if self.playerOwnedProperties[color][name][1] != 0:
              print("Please sell your houses first!")
              # - BILL TONG
              subprocess.call(['/home/team34/ros_ws/src/baxter_tools/scripts/emotions/confused.sh'], shell=True)
              trump.dialogue(3)
              return
            else:
              prop[color].append(name)
        else:
          for name in self.playerOwnedProperties[color]:
            if self.playerOwnedProperties[color][name][0] == True:
              prop[color].append(name)
      print(prop)
      # - BILL TONG
      subprocess.call(['/home/team34/ros_ws/src/baxter_tools/scripts/emotions/worried.sh'], shell=True)
      trump.dialogue(4)
      choice = input("Which property would you like to mortgage?: ")
      for color in prop:
        if color in self.playerOwnedSets and choice in prop[color]:
          choice2 = input(
            "Are your sure? You will not be able to buy houses in this color set anymore [y/n]: "
          )
          
          if choice2 == "y":
            self.gainMoney(self.cards[choice][1])
            self.playerOwnedProperties[color][choice][2] = True
            self.playerMortgaged.append(choice)
            return
          elif choice2 == "n":
            return
        elif choice in prop[color]:
          self.gainMoney(self.cards[choice][2])
          self.playerOwnedProperties[color][choice][2] = True
          self.playerMortgaged.append(choice)
          return
    else:
      notSet = []
      finSet = []
      p = ""
      y = 0
      for prop in self.robotOwnedProperty:
        for color in self.ownedProperties:
          if prop in self.ownedProperties[color] and self.isASet(color):
            if self.propMortgaged(color, prop) == False:
              finSet.append(prop)
          elif prop in self.ownedProperties[color] and self.isASet(color) == False:
            if self.propMortgaged(color, prop) == False:
              notSet.append(prop)
            
      if len(notSet) > 0 and self.house == 0:
        y = self.cards[notSet[0]][1]
        p = notSet[0]
        for propNum in range(1, len(notSet)):
          if self.cards[notSet[propNum]][1] > y:
            p = notSet[propNum]
            y = self.cards[prop][1]
      elif len(notSet) == 0 and self.house == 0:
        p = finSet[0]
        y = self.cards[finSet[0]][1]
        for prop in finSet:
          if self.cards[prop][1] > y:
            p = prop
            y = self.cards[prop][1]
      self.gainMoney(self.cards[p][2])
      self.robotMortgaged.append(p)
      for color in self.ownedProperties:
        if p in self.ownedProperties[color]:
          self.ownedProperties[color][p][2] = True
          break
          
  def listMortgaged(self):
    mortgaged = []
    if self.isPlayer == False:
      for color in self.ownedProperties:
        for name in self.ownedProperties[color]:
          if self.ownedProperties[color][name][2] == True:
            mortgaged.append(name)
    else:
      for color in self.playerOwnedProperties:
        for name in self.playerOwnedProperties[color]:
          if self.playerOwnedProperties[color][name][2] == True:
            mortgaged.append(name)
    return mortgaged
    
  def returnColor(self, name):
    for space in self.Board:
      if self.Board[space][0] == -2:
        continue
      else:
        if self.Board[space][2] == name:
          return self.Board[space][1]

  def unmortgage(self):
    if not self.isPlayer:
      mort = self.listMortgaged()
      setMort = []
      for prop in mort:
        if self.returnColor(prop) in self.ownedSets:
          setMort.append(prop)
          mort.pop(prop.index())
          
      m = ""
      y = 0
      k = ""
      wgt = {k: v for k, v in sorted(self.weights.items(), key=lambda item: item[1], reverse = True)}
      if len(setMort) > 0:
        for prop in setMort:
          if self.robotMoneySum > self.unmortgageProperty(prop):
            y = max(y, wgt[self.returnColor(prop)])
            if wgt[self.returnColor(prop)] == y:
              m = prop
      else:
        for prop in mort:
          if self.robotMoneySum > self.unmortgageProperty(prop):
            y = max(y, wgt[self.returnColor(prop)])
            if wgt[self.returnColor(prop)] == y:
              m = prop
      self.giveMoney(self.unmortgageProperty(m))
      self.ownedProperties[self.returnColor(m)][m][2] = False
      return
    else:
      mort = self.listMortgaged()
      print(mort)
      # - BILL TONG
      subprocess.call(['/home/team34/ros_ws/src/baxter_tools/scripts/emotions/worried.sh'], shell=True)
      trump.dialogue(5)
      prop = input("Which property would you like to unmortgage?: ")
      # TODO: Web UI input here
      if prop in mort and self.playerMoneySum - self.unmortgageProperty(prop) > 0:
        self.giveMoney(self.unmortgageProperty(prop))
        self.playerOwnedProperties[self.returnColor(prop)][prop][2] = True
      else:
        return
        

        
      
  def readCardCC(self, cardNum):
    # TODO: Possible feedback here
    print("I pulled No." + str(cardNum))
    self.namingShortcut()
    #social here, talking about the card pulled.
    if cardNum == 1:
      if self.isPlayer == False:
        self.giveMoney(self.house * 40 + self.hotel * 110)
      else:
        self.giveMoney(self.playerHouse * 40 + self.playerHotel * 110)
    elif cardNum == 2:
      self.updatePosition(40-self.space)
    elif cardNum == 3:
      self.gainMoney(10)
    elif cardNum == 4:
      self.gainMoney(50)
    elif cardNum == 5:
      self.gainMoney(100)
    elif cardNum == 6:
      self.gainMoney(10 * self.numPlayers)
    elif cardNum == 7:
      self.gainMoney(25)
    elif cardNum == 8:
      self.giveMoney(100)
    elif cardNum == 9:
      self.gainMoney(20)
    elif cardNum == 10:
      self.giveMoney(50)
    elif cardNum == 11:
      self.gainMoney(100)
    elif cardNum == 12:
      self.gainMoney(100)
    elif cardNum == 13:
      self.gainMoney(200)
    elif cardNum == 14:
      self.giveMoney(50)
    elif cardNum == 15:
      self.goToJail()
    elif cardNum == 16:
      self.getJailCard()

  def readCardChance(self, cardNum):
    # TODO: Possible feedback here
    print("I pulled No." + str(cardNum))
    if cardNum == 1:
      if self.isPlayer == False:
        self.giveMoney(self.house * 25 + self.hotel * 100)
      else:
        self.giveMoney(self.playerHouse * 25 + self.playerHotel * 100)
      return
    elif cardNum == 2:
      self.namingShortcut()
      self.updatePosition(40-self.space)
      return
    elif cardNum == 3 or cardNum == 8:
      rail = [15, 25, 35]
      t = 0
      if self.isPlayer == False:
        for pos in rail:
          if pos > self.currPos:
            self.updatePosition(pos-self.currPos)
            break
          elif self.currPos == 36:
            self.updatePosition(9)
            break
        self.namingShortcut()
        if self.square == 0:
          self.buy()
      else:
        for pos in rail:
          if pos > self.playerPos:
            self.updatePosition(pos - self.playerPos)
            break
          elif self.playerPos == 36:
            self.updatePosition(9)
            break
        self.namingShortcut()
        if self.square == 0:
          # - BILL TONG
          subprocess.call(['/home/team34/ros_ws/src/baxter_tools/scripts/emotions/worried.sh'], shell=True)
          trump.dialogue(0)
          choice = input("Would you like to buy the railroad? [y/n]")
          if choice == "y":
            self.buy()
          else:
            return
    elif cardNum == 4:
      self.namingShortcut()
      if self.space > 24:
        self.updatePosition(64-self.space)
      else:
        self.updatePosition(24-self.space)
      return
    elif cardNum == 5:
      self.namingShortcut()
      self.updatePosition(39-self.space)
      return
    elif cardNum == 6:
      self.namingShortcut()
      self.updatePosition(45-self.space)
      return
    elif cardNum == 7:
      util = [12, 28]
      if self.isPlayer == False:
        for pos in util:
          if pos > self.currPos:
            self.updatePosition(pos-self.currPos)
            break
          elif self.currPos == 36:
            self.updatePosition(16)
            break
        self.namingShortcut()
        if self.square == 0:
          self.buy()
      else:
        for pos in util:
          if pos > self.playerPos:
            self.updatePosition(pos - self.playerPos)
            break
          elif self.playerPos == 36:
            self.updatePosition(16)
            break
        self.namingShortcut()
        if self.square == 0:
          # - BILL TONG
          subprocess.call(['/home/team34/ros_ws/src/baxter_tools/scripts/emotions/worried.sh'], shell=True)
          trump.dialogue(1)
          choice = input("Would you like to buy the Utility? [y/n]")
          if choice == "y":
            self.buy()
          else:
            return
    elif cardNum == 9:
      self.namingShortcut()
      if self.space > 11:
        self.updatePosition(51-self.space)
      else:
        self.updatePosition(11-self.space)
      return
    elif cardNum == 10:
      self.updatePosition(-3)
      return
    elif cardNum == 11:
      self.gainMoney(150)
    elif cardNum == 12:
      self.gainMoney(50)
    elif cardNum == 13:
      self.giveMoney(15)
    elif cardNum == 14:
      if self.isPlayer == False:
        self.giveMoney(50)
        self.isPlayer = True
        self.gainMoney(50)
        self.isPlayer = False
        return
      else:
        self.giveMoney(50)
        self.isPlayer = False
        self.gainMoney(50)
        self.isPlayer = True
        return
    elif cardNum == 15:
      self.goToJail()
      return
    elif cardNum == 16:
      self.getJailCard()
    
        
        
    
  def pullCard(self, cardType):
    # TODO: Voice or Web UI feedback for this
    if cardType == "Community Chest":
        rules.pullCard()
        card = rospy.wait_for_message('mpCards', Int16).data
        self.readCardCC(card)
        self.listOfCC.append(card)
    elif cardType == "Chance":
        rules.pullCard()
        card = rospy.wait_for_message('mpCards', Int16).data
      #  self.card = self.listOfChance.pop(0)
        self.readCardChance(card)
    if card != 16:
        self.listOfChance.append(card)
    else:
        return
  def receiveRent(self, value):
    if self.isPlayer == False:
      self.isPlayer = True
      self.gainMoney(value)
      self.isPlayer = False
    else:
      self.isPlayer = False
      self.gainMoney(value)
      self.isPlayer = True

  def oppSet(self, color):
    if not self.isPlayer:
      x = False
      self.isPlayer = True
      if self.isASet(color):
        x = True
      self.isPlayer = False
      return x
    else:
      x = False
      self.isPlayer = False
      if self.isASet(color):
        x = True
      self.isPlayer = False
      return x
    return False
    
  def oppMort(self, color, name):
    if not self.isPlayer:
      x = False
      self.isPlayer = True
      if self.propMortgaged(color, name):
        x = True
      return x
    else:
      x = False
      self.isPlayer = False
      if self.propMortgaged(color, name):
        x = True
      return x
    return False
     
  def payRent(self):
    # TODO: This information should be communicated to player, either through Voice or UI
    self.namingShortcut()
    if self.isPlayer == False: # Robot owes player money
      if self.oppMort(self.color, self.name):
        print("No rent! This property has been mortgaged!")
      elif self.square == -1 and self.oppSet(self.color):
        if self.color == "Utilities":
          # Have the robot announce the rent
          rent = self.move * 10
          audio = "I owe you" + self.rent + "dollars."
          language = "en" 
          audioTalk = gTTS(text=audio, lang=language, slow=False)
          audioTalk.save("audio.mp3")
          os.system("mpg321 audio.mp3")
          self.giveMoney(rent)
          self.receiveRent(rent)
        else:
          house = self.numHouses(self.color, self.name)
          if house > 4:
            rent = self.rentLookup(self.name, True, 0, 1)
            audio = "I owe you" + self.rent + "dollars."
            language = "en" 
            audioTalk = gTTS(text=audio, lang=language, slow=False)
            audioTalk.save("audio.mp3")
            os.system("mpg321 audio.mp3")
            self.giveMoney(rent)
            self.receiveRent(rent)
          elif house > 0:
            rent = self.rentLookup(self.name, True, house)
            audio = "I owe you" + self.rent + "dollars."
            language = "en"
            audioTalk = gTTS(text=audio, lang=language, slow=False)
            audioTalk.save("audio.mp3")
            os.system("mpg321 audio.mp3")
            self.giveMoney(rent)
            self.receiveRent(rent)

          else:
            rent = self.rentLookup(self.name, True)
            audio = "I owe you" + self.rent + "dollars."
            language = "en" 
            audioTalk = gTTS(text=audio, lang=language, slow=False)
            audioTalk.save("audio.mp3")
            os.system("mpg321 audio.mp3")
            self.giveMoney(rent)
            self.receiveRent(rent)

      elif self.square == -1:
        if self.color == "Utilities":
          rent = self.move * 4
          audio = "I owe you" + self.rent + "dollars."
          language = "en"
          audioTalk = gTTS(text=audio, lang=language, slow=False)
          audioTalk.save("audio.mp3")
          os.system("mpg321 audio.mp3")
          self.giveMoney(rent)
          self.receiveRent(rent)
        else:
          rent = self.rentLookup(self.name)
          audio = "I owe you" + self.rent + "dollars."
          language = "en" 
          audioTalk = gTTS(text=audio, lang=language, slow=False)
          audioTalk.save("audio.mp3")
          os.system("mpg321 audio.mp3")
          self.giveMoney(rent)
          self.receiveRent(rent)

      #social here, anger.

    else:
      if self.oppMort(self.color, self.name):
        print("No rent! This property has been mortgaged!")
      elif self.square == 1 and self.color in self.ownedSets:
        if self.color == "Utilities":
          rent = self.move * 10
          audio = "You owe me" + self.rent + "dollars."
          language = "en"
          audioTalk = gTTS(text=audio, lang=language, slow=False)
          audioTalk.save("audio.mp3")
          os.system("mpg321 audio.mp3")
          self.giveMoney(rent)
          self.receiveRent(rent)
        else:
          house = self.ownedProperties[self.color][self.name][1]
          if house > 4:
            rent = self.rentLookup(self.name, True, False, True)
            audio = "You owe me" + self.rent + "dollars."
            language = "en"
            audioTalk = gTTS(text=audio, lang=language, slow=False)
            audioTalk.save("audio.mp3")
            os.system("mpg321 audio.mp3")
            self.giveMoney(rent)
            self.receiveRent(rent)

          elif house > 0:
            rent = self.rentLookup(self.name, True, house)
            audio = "You owe me" + self.rent + "dollars."
            language = "en"
            audioTalk = gTTS(text=audio, lang=language, slow=False)
            audioTalk.save("audio.mp3")
            os.system("mpg321 audio.mp3")
            self.giveMoney(rent)
            self.receiveRent(rent)

          else:
            rent = self.rentLookup(self.name, True)
            audio = "You owe me" + self.rent + "dollars."
            language = "en"
            audioTalk = gTTS(text=audio, lang=language, slow=False)
            audioTalk.save("audio.mp3")
            os.system("mpg321 audio.mp3")
            self.giveMoney(rent)
            self.receiveRent(rent)

      elif self.square == 1 and self.color not in self.ownedSets:
        if self.color == "Utilities":
          rent = self.move * 4
          audio = "You owe me" + self.rent + "dollars."
          language = "en"
          audioTalk = gTTS(text=audio, lang=language, slow=False)
          audioTalk.save("audio.mp3")
          os.system("mpg321 audio.mp3")
          self.giveMoney(rent)
          self.receiveRent(rent)

        else:
          rent = self.rentLookup(self.name)
          audio = "You owe me" + self.rent + "dollars."
          language = "en"
          audioTalk = gTTS(text=audio, lang=language, slow=False)
          audioTalk.save("audio.mp3")
          os.system("mpg321 audio.mp3")
          self.giveMoney(rent)
          self.receiveRent(rent)


  def endTurn(self):
    self.turnCounter -= 1
    if self.isPlayer == True:
      self.isPlayer = False
    else:
      self.isPlayer = True
    #Taunting here. Social

  def checkBankruptcy(self):
    if self.isPlayer == True:
      if self.playerMoneySum == 0:
        for prop in self.playerOwnedProperty:
          if prop not in self.playerMortgaged:
            break
        else:
          return False
        return True
        #Trump voice, demand recount.
    else:
      if self.robotMoneySum == 0:
        for prop in self.robotOwnedProperty:
          if prop not in self.robotMortgaged:
            break
        else:
          return False
        return True
    return False
    
  def countAssets(self):
    robotTotal, playerTotal = self.robotMoneySum, self.playerMoneySum
    for color in self.ownedProperties:
      for prop in self.ownedProperties[color]:
        if color in self.ownedSets:
          robotTotal += self.ownedProperties[color][prop][1] * self.getBuildCost(prop)
        if self.ownedProperties[color][prop][0] == True:
          robotTotal += self.board[self.cards[prop][0]][3]
    for color in self.playerOwnedProperties:
      for prop in self.playerOwnedProperties[color]:
        if color in self.playerOwnedSets:
          playerTotal += self.playerOwnedProperties[color][prop][1] * self.getBuildCost(prop)
        if self.playerOwnedProperties[color][prop][0] == True:
          playerTotal += self.board[self.cards[prop][0]][3]
    if robotTotal > playerTotal:
      # TODO: WebUI for this?
      print("You lose! The robot has {} dollars of total assets while you have {} dollars of total assets".format(robotTotal, playerTotal))
      return True
    elif playerTotal > robotTotal:
      print("You win! You have {} dollars of total assets while BoardBot has {} dollars of total assets.".format(playerTotal, robotTotal))
      return False
    else:
      print("Tie!")
         
          
  def endGame(self):
    if self.checkBankruptcy == True:
      if self.isPlayer == True:
        # TODO: Web UI for this
        print("Game Over! You have gone bankrupt!")
      else:
        print("You win! I have gon bankrupt!")
    else:
      if self.countAssets():
        # - BILL TONG
        subprocess.call(['/home/team34/ros_ws/src/baxter_tools/scripts/emotions/sassy.sh'], shell=True)
        trump.robotWin()
      else:
        # - BILL TONG
        subprocess.call(['/home/team34/ros_ws/src/baxter_tools/scripts/emotions/angry.sh'], shell=True)
        trump.playerWin()
    quit()
      
          
class Jail(Actions):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.robotInJail = False
    self.playerInJail = False
    self.robotJailFree = False
    self.playerJailFree = False
    
  def goToJail(self):
    # TODO: Communicate this to player somehow: Maybe with a "jail" emoji or web UI feedback
    self.namingShortcut()
    #Trump voice
    if self.isPlayer == False:
      self.currPos = 10
      self.robotInJail = True
      self.endTurn()
    else:
      self.playerPos = 10
      self.playerInJail = True
      self.endTurn()

  def getJailCard(self):
    if self.isPlayer == True:
      self.playerJailFree = True
    else:
      self.robotJailFree = True

  def useCard(self):
    if self.isPlayer == False and self.robotJailFree == True:
      self.robotInJail = False
      self.robotJailFree = False
    elif self.isPlayer == True and self.playerJailFree == True:
      self.playerInJail = False
      self.playerJailFree = False
    if len(self.listOfCC) != 16:
      self.listOfCC.append(16)
    elif len(self.listOfChance) != 16:
      self.listOfChance.append(16)

  def payFine(self):
    #Trump voice
    self.giveMoney(50)
    if self.isPlayer == False:
      self.robotInJail = False
    else:
      self.playerInJail = False

  def rollOut(self):
    if self.isPlayer == False:
      temp = rules.rollDice()
      if temp[0] == temp[1]:
        #Bragging
        self.robotInJail = False   
    else:
      self.playerInJail = False


class Decisions(Jail):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.doubleCounter = 0
 

  def playerDecisions(self):
    global webPlayerInfoPublisher
    global webAnnouncePublisher
    c = self.playerStartTurn() # Get dice roll
    endTurn = False
    while endTurn == False:
      message = roslibpy.Message({'data': "It is your turn. Choose an action, or end your turn."})
      webAnnouncePublisher.publish(message)
      choice = rospy.wait_for_message("playerinput", Int16).data
      if c == 1 or c == 2: # 1: dice do not match. 2: dice match (rolled doubles)
        #choice = rospy.wait_for_message("playerinput", Int16).data
        if c == 1:
          self.doubleCounter = 0
        #choice = int(
        #  input(
        #    "(1) Buy\n(2) Sell Houses\n(3)Mortgage Properties\n(4) Check Balance\n(5) Declare Bankruptcy\n(6) End Turn\n(0) End Game: "
        #  ))
      else:
        pass
        #choice = int(
        #  input(
        #    "(1) Buy\n(2) Sell\n(3)Mortgage\n(4) Check Balance\n(5) Declare Bankruptcy\n(6) Skip Turn\n(7) Roll Dice\n(0) End Game: "
        #  ))
      if choice == 1:
        self.buy() # buy property
#        if choice2 == 1:
#          self.buy()
#        elif choice2 == 2:
#          if len(self.playerOwnedSets) != 0:
#            print("Your current completed sets are " +
#                  str(self.playerOwnedSets))
#            i = input("What color set would you like to build on?: ")
#            self.buyHouse(i)
#          else:
#            # - BILL TONG
#            subprocess.call(['./surprise.sh'], shell=True)
#            trump.dialogue(6)
#            print("You don't have any completed sets!")
      elif choice == 2:
         print(self.playerOwnedProperty)
         if len(self.playerOwnedSets) != 0:
            print("The colors you can build on are " + str(self.playerOwnedSets))
            i = input("What color set would you like to build on?: ")
            self.buyHouse(i)
      elif choice == 3:
        #choice2 = input("(1) Mortgage\n(2) Unmortgage")
        #if int(choice2) == 1:
        self.mortgage()
        #else:
          #self.unmortgage()
      elif choice == 4:
        self.unmortgage()
        #print(self.playerMoneySum)
        #moneyMsg = roslibpy.Message({'data': self.playerMoneySum})
        #webPlayerInfoPublisher.publish(moneyMsg)
        #print("A more detailed breakdown: " + str(self.playerMoney))
        #if len(self.playerOwnedProperty) != 0:
        #  print(self.playerOwnedProperty)
        #  tempString = ', '.join(self.playerOwnedProperty) # Collapse list into string
        #  tempString = tempString + ' Marvin Gardens,' + ' Boardwalk' # TODO: Testing for web ui; delete this
        #  propMsg = roslibpy.Message({'data': tempString})
        #  webPlayerPropertyPublisher.publish(propMsg)
        #else:
          # - BILL TONG
        #  subprocess.call(['./surprise.sh'], shell=True)
        #  trump.dialogue(7)
        #  print("You own no properties!")

      elif choice == 5:
        self.checkBankruptcy()

      elif choice == 6:
        #TODO: Endturn
        break
      elif choice == 7:
        #r = rules.rollDice()
        #print("You rolled (" + str(r[0]) + "," + str(r[1]) + ").")
        #self.updatePosition(r[0] + r[1])
        c = 1
      elif choice == 0:
        self.endGame()
    # End while loop

    # Update Web UI with player information    
    moneyMsg = roslibpy.Message({'data': self.playerMoneySum})
    webPlayerInfoPublisher.publish(moneyMsg)

    if c == 2:
      self.doubleCounter += 1
      if self.doubleCounter == 4:
        self.goToJail()
      else:
        self.playerDecisions()

    return
    # End of playerDecisions
  def playerStartTurn(self):
    # TODO: If this is used, then this functionality should shift to web UI
    global server # for Web UI
    global webPlayerInfoPublisher # For webUI topic
    global webPlayerPropertyPublisher
    #r = []
    print("It is the player's turn! Roll the dice.\n")
    global webAnnouncePublisher
    message = roslibpy.Message({'data': "It is your turn! Roll the dice."})
    webAnnouncePublisher.publish(message)

    #playerIn = input("[y/n]: ")
    #if playerIn == "y":
    dice = rospy.wait_for_message("diceinput", Int16).data # Get the dice total as: dice1dice2
    dice1 = int(dice//10) # Extract first digit (a single die value)
    dice2 = int(dice%10) # Extract second digit (the other die value)
    choice = [dice1, dice2]
    print("Dice rolled:")
    print(dice1, " ", dice2)
    #print("\n")
    #choice = input("What did you roll? (Format it as X X)")
    #for c in choice:
    #if c.isalnum():
        #r.append(int(c))
    diceTotal = dice1 + dice2
    self.updatePosition(diceTotal)
    #webInfoPublisher.publish(roslibpy.Message({'data': diceTotal}))  TODO: Change the topic for this
    if dice1 == dice2:
        return 2 # doubles!
    else:
        return 1 # not doubles
    
  def robotDecision(self):
    ownedWeights = {}
    self.namingShortcut()
    print(self.Board[self.space])
    if not self.checkBankruptcy():
      if self.square == 0:
        self.buy()
        subprocess.call(['/home/team34/ros_ws/src/baxter_tools/scripts/emotions/happy.sh'], shell=True)
        trump.happy()
      if self.robotMoneySum <= 200:
        self.mortgage()
      if len(self.robotMortgaged) > 0:
        self.unmortgage()
      if len(self.ownedSets) > 0:
        for color in self.ownedSets:
          ownedWeights[color] = self.weights[color]
        max_key = max(ownedWeights, key=ownedWeights.get)
        self.buyHouse(max_key)
    else:
      if self.checkBankruptcy():
        # TODO: Web UI output here, maybe
        print("You win! I have gone bankrupt.")
        quit()
      else:
        self.mortgage()
    


class PlayGame(Decisions):
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
  def startGame(self):
    robotRoll = rules.gameSetup()
    # Display initial cash for player and robot
    global webPlayerInfoPublisher
    moneyMsg1 = roslibpy.Message({'data': (self.playerMoneySum)})
    webPlayerInfoPublisher.publish(moneyMsg1)

    global webRobotInfoPublisher
    moneyMsg2 = roslibpy.Message({'data': (self.robotMoneySum)})
    webRobotInfoPublisher.publish(moneyMsg2)

    # TODO: Replace with real dice roll
    #robotSum = robotRoll[0] + robotRoll[1]
    robotSum = 1 #Testing
    #r = rules.rollDice()
    #playerRoll = input("What did you roll? Input as (X X): ") 
    #playerSum = int(playerRoll[0]) + int(playerRoll[2]) #Testing
    playerSum = 0
    #print("I rolled ({}, {})".format(r[0], r[1]))
    if robotSum > playerSum:
      # - BILL TONG
      subprocess.call(['/home/team34/ros_ws/src/baxter_tools/scripts/emotions/neutral.sh'], shell=True)
      trump.robotStart()
      print("I will be going first!")
    else:
      # - BILL TONG
      subprocess.call(['/home/team34/ros_ws/src/baxter_tools/scripts/neutral.sh'], shell=True)
      trump.playerStart()
      print("You will be going first!")
      self.isPlayer = True

  def robotTurn(self):
    # TODO: info from here should be pushed (published) to Web UI
    #diceMovePub = rospy.Publisher('diceRoll', Int16, queue_size=10)
    #rospy.sleep(2.0)
    print("It is the robot's turn!.\n")
    global webAnnouncePublisher
    message = roslibpy.Message({'data': "It is BoardBot's turn."})
    webAnnouncePublisher.publish(message)

    if self.robotInJail == True:
      if self.robotJailFree == True:
        print("I will use my card!")
        self.useCard()
        self.robotTurn()
      elif len(self.playerOwnedProperty) > 7 and self.robotMoneySum < 500:
        print("I will attempt to roll out!")
        self.rollOut()
        self.robotTurn()
      else:
        print("I will pay the fine!")
        self.payFine()
        self.endTurn()
    else:
      # Standard turn: Roll dice, move piece, do action
      rules.rollDice() # Rolling Dice
      #diceMovePublisher = rospy.Publisher('diceRoll', Int16, queue_size=10)
      #diceMovePublisher.publish(0) # "0" means to roll the dice
      print("\nin AI: robot should have rolled dice")
      #rospy.sleep(2.0)

      
      #rospy.spin() # wait here
      
      # Waits for computer vision to pass dice vals then passes them to movement
      rollVal = rospy.wait_for_message('diceVals', Int16MultiArray).data
      
      diceVal = int(rollVal[0]) + int(rollVal[1])
      rules.publishDice(diceVal)
      
      #r = rules.rollDice() # Randomly generate dice for testing
      print("I rolled (" + str(rollVal[0]) + ", " + str(rollVal[1]) + ")")
      
      # TODO
      # Needs to be reintegrated somewhere else
      self.updatePosition(rollVal[0] + rollVal[1])
      self.robotDecision()
      rospy.sleep(2)
      if rollVal[0] == rollVal[1]:
        self.doubleCounter += 1
        if self.doubleCounter == 4:
          self.goToJail()
          self.doubleCounter = 0
        else:
                #client = roslibpy.Ros(host='134.197.95.215', port=9090)
                #self.webPublisher() 
          self.robotTurn()
      else:
        self.doubleCounter = 0
            #self.webPublisher()
        self.endTurn()
        print("\n")

  def playerTurn(self):
    # TODO: Web UI will do a lot of I/O here, probably
    if self.playerInJail == False:
      self.playerDecisions()
      self.endTurn()
      print("\n")
    else:
      # - BILL TONG
      subprocess.call(['/home/team34/ros_ws/src/baxter_tools/scripts/emotions/sad.sh'], shell=True)
      trump.jail()
      print("You are in Jail!")
      choice = ""
      if self.playerJailFree == False:
        choice = input("Would you like to: \n(1) Roll\n(2) Pay\n")
      else:
        choice = input("Would you like to: \n(1) Roll\n(2) Pay\n(3) Use Get Out of Jail Card")
      if int(choice) == 1:
        self.rollOut()
      elif int(choice) == 2:
        self.payFine()
      elif int(choice) == 3:
        self.useCard()
        
  # Core gameplay loop: after a player initiates the game via Web UI, players take alternating turns
  def playGame(self, server):
  #def playGame(self):
    global begin 
    begin = False
    self.listener = roslibpy.Topic(server, '/begin', 'std_msgs/String') # Set up a topic 'begin' via the server

    #while not begin:
    #  self.listener.subscribe(beginCallback)
    begin = True
    if begin == True: # Wait until the player sends the signal to begin the game
      self.startGame()
      self.isPlayer = True # TODO: forcing player to go first
      while self.turnCounter > 0:
        if self.isPlayer == True:
            # TODO: web UI gets input from player to begin turn
          self.playerTurn()     # Human player takes a turn
        else:
          self.robotTurn()      # BoardBot takes a turn
        sleep(1)
        if self.turnCounter == 0:
            # TODO: Web UI should display victory/defeat
          self.endGame() # Check endgame conditions


class debug(PlayGame):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setDebug = False
    #inp = input("Would you like to enter debug mode? [y/n]: ")
    inp = "n" # Disabling debug mode for now
    if inp.lower() == "y":
      print("Entering debug mode!")
      self.setDebug = True
    elif inp.lower() == "n":
      return

  def debugMode(self):
    if self.setDebug == True:
      print("(1) Add Money\n(2) Add Property\n(3) Add House/Hotel")
      i = input()
      print(i)

#def subscribeFrontend()
#   used to check for a "start-the-game" message from web frontend
def beginCallback(data):
    temp = data
    global begin
    if(temp['data'] == "6"):
        begin = True
        print("\n\nStart the game already!\n\n")
    else:
        print("\nNot yet")


def playTurn():
    try:
      while True:
        rospy.init_node('AI') # Start a ROS node for pub-sub
        global server # Create global var to connect pubsub to rosbridge (web UI)
        global webPlayerInfoPublisher       # Create global var for sending money info to web UI
        global webPlayerPropertyPublisher   # Create global var for sending property info to web UI
        global webRobotInfoPublisher        # Create global var for sending money info to web UI
        global webRobotPropertyPublisher    # Create global var for sending property into to web UI
        global webAnnouncePublisher         # Create global var for sending messages and prompts to the web UI
        server = roslibpy.Ros(host='134.197.95.215', port=9090) # Assign connection info
        webPlayerInfoPublisher = roslibpy.Topic(server, '/playerinfo', 'std_msgs/Int16')
        webPlayerPropertyPublisher = roslibpy.Topic(server, '/playerassets', 'std_msgs/String')
        webRobotInfoPublisher = roslibpy.Topic(server, '/robotinfo', 'std_msgs/Int16')
        webRobotPropertyPublisher = roslibpy.Topic(server, '/robotassets', 'std_msgs/String')
        webAnnouncePublisher = roslibpy.Topic(server, '/announcements', 'std_msgs/String')
        #server.connect()
        server.run()       # Launch server
        d = debug()
        d.playGame(server)       # This is the main gameplay function
        server.terminate()  
    except KeyboardInterrupt:
      server.terminate()  # Ensure that server properly closes if program is closed
    """rospy.init_node('AI') # Start a ROS node for pub-sub
    d = debug()
    d.playGame()     # This .py file must be associated with a ROS node
    rospy.sleep(100.0)"""
        
if __name__ == "__main__":
  playTurn()

