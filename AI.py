import rules
from time import sleep
import random as rd
from std_msgs.msg import Int16
import rospy
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
    self.turnCounter = 50
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
        if self.currPos >= 40:
          self.currPos -= 40
          self.passGo()

    self.namingShortcut()

    if self.square == -2:
      if self.isPlayer == False:
        #Say what square it lands on.
        print("I landed on " + self.name)
      else:
        print("You've landed on " + self.name)
      """match self.name:
        case "CommunityChest":
          self.pullCard()
        case "Chance":
          self.pullCard()
        case "IncomeTax":
          if self.isPlayer == False:
            self.giveMoney(min(200, self.robotMoneySum * 0.1))
          else:
            self.giveMoney(min(200, self.playerMoneySum * 0.1))
        case "Go To Jail":
          self.currPos = 10
          self.inJail = True
        case "Luxury Tax":
          self.giveMoney(75)"""

      if self.name == "Community Chest":
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

def isDouble(self, d1, d2):
  return d1 == d2


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
    self.ownedSets, self.playerOwnedSets = set(), set()
    self.listOfCC = rd.sample(range(1, 17), 16)
    self.listOfChance = rd.sample(range(1, 17), 16)

  def gainMoney(self, amount):
    if self.isPlayer == False:
      self.robotMoneySum += amount
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
      self.playerMoneySum += amount
      while amount > 0:
        for i in self.playerMoney:
          if amount >= i:
            temp = amount // i
            self.playerMoney[i] += temp
            #Give command for the robot to grab the correct currency.
            amount -= (i * temp)
          if amount == 0:
            return

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
    
    if self.isPlayer == False:
      self.robotMoneySum -= amount
      while amount > 0:
        x = self.closest(amount)
        try:
          amount = self.payAmount(x, amount)
        except:
          print("Error!")
        if amount < 0:
          self.gainMoney(amount * -1)
          self.robotMoneySum += amount
          return
        elif amount == 0:
          return
          
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
          return
        elif amount == 0:
          return
    

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


class Actions(Assets, rules.ChanceCommunityCards):

  def passGo(self):
    self.gainMoney(200)

  def buy(self):
    self.namingShortcut()
    if self.square == 0:
      if self.isPlayer == False:
        self.leftoverMoney = self.robotMoneySum - self.price
        if self.leftoverMoney >= 350:
          self.updateOwnership("buy")
          self.giveMoney(self.price)
          self.ownedProperties[self.color][self.name][0] = True
          self.robotOwnedProperty.append(self.name)
          self.robotNumProperties += 1
          #Social aspect here, saying that they bought xxx property.
          if self.isASet(self.color):
            self.ownedSets.add(self.color)

      else:
        self.leftoverMoney = self.playerMoneySum - self.price
        if self.leftoverMoney >= 350:
          self.updateOwnership("oppBuy")
          self.giveMoney(self.price)
          self.playerOwnedProperties[self.color][self.name][0] = True
          self.playerOwnedProperty.append(self.name)
          self.playerNumProperties += 1
          if self.isASet(self.color):
            self.ownedSets.add(self.color)

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

    elif self.isPlayer == True and self.isSet(
        color) and not self.isMortgaged(color) == False:
      for name in self.playerOwnedProperties[color]:
        prop[name] = self.playerOwnedProperties[color][name][1]
      for key, value in prop.items():
        if value <= 4:
          print("There are " + str(value) + " houses on " + key)
        else:
          print("There is a hotel on " + key)
      choice = input("Choose Property: ")
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
      self.giveMoney(self.cards[choice][1])
      if self.isPlayer == True:
        self.playerOwnedProperties[color][choice][1] += 1
      else:
        self.ownedProperties[color][choice][1] += 1

    elif self.isPlayer == True:
      print("Adding a house to " + choice)
      self.giveMoney(self.cards[choice][1])
      if self.isPlayer == True:
        self.playerOwnedProperties[color][choice][1] += 1
      else:
        self.ownedProperties[color][choice][1] += 1

  def mortgage(self):
    prop = dict()
    if self.isPlayer == True:
      for color in self.playerOwnedProperties:
        if color not in prop:
          prop[color] = []
        if color in self.playerOwnedSets:
          for name in self.playerOwnedProperties[color]:
            if self.playerOwnedProperties[color][name][1] != 0:
              print("Please sell your houses first!")
              return
            else:
              prop[color].append(name)
        else:
          for name in self.playerOwnedProperties[color]:
            if self.playerOwnedProperties[color][name][0] == True:
              prop[color].append(name)
      print(prop)
      choice = input("Which property would you like to mortgage?: ")
      for color in prop:
        if color in self.playerOwnedSets and choice in prop[color]:
          choice2 = input(
            "Are your sure? You will not be able to buy houses in this color set anymore [y/n]: "
          )
          """match choice2:
            case "y":
              self.gainMoney(self.cards[choice][2])
              self.playerOwnedProperties[color][choice][2] = True
              return
            case "n":
              return"""
          if choice2 == "y":
            self.gainMoney(self.cards[choice][2])
            self.playerOwnedProperties[color][choice][2] = True
            return
          elif choice2 == "n":
            return
        elif choice in prop[color]:
          self.gainMoney(self.cards[choice][2])
          self.playerOwnedProperties[color][choice][2] = True
    else:
      notSet = []
      finSet = []
      p = ""
      y = 0
      for prop in self.robotOwnedProperty:
        for color in self.ownedProperties:
          if prop in self.ownedProperties[color] and self.isASet(color):
            finSet.append(prop)
          elif prop in self.ownedProperties[color] and self.isASet(color) == False:
            notSet.append(prop)
      
      if len(notSet) > 0 and self.house == 0:
        y = self.cards[notSet[0]][1]
        for prop in notSet:
          if self.cards[prop][1] > y:
            p = prop
            y = self.cards[prop][1]
      elif len(notSet) == 0 and self.house == 0:
        y = self.cards[finSet[0]][1]
        for prop in finSet:
          if self.cards[prop][1] > y:
            p = prop
            y = self.cards[prop][1]
      self.gainMoney(self.cards[p][1])
      for color in self.ownedProperties:
        if p in self.ownedProperties[color]:
          self.ownedProperties[color][p][2] = True
          break
  
  def readCardCC(self, cardNum):
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
      
    """match cardNum:
      case 1:
        if self.isPlayer == False:
          self.giveMoney(self.house * 40 + self.hotel * 110)
        else:
          self.giveMoney(self.playerHouse * 40 + self.playerHotel * 110)
      case 2:
        self.currPos = 0
        self.passGo()
      case 3:
        self.gainMoney(10)
      case 4:
        self.gainMoney(50)
      case 5:
        self.gainMoney(100)
      case 6:
        self.gainMoney(10 * self.numPlayers)
      case 6:
        return False"""

  def readCardChance(self, cardNum):
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
    if cardType == "Community Chest":
      self.card = self.listOfCC.pop(0)
      self.readCardCC(self.card)
      self.listOfCC.append(self.card)
    elif cardType == "Chance":
      self.card = self.listOfChance.pop(0)
      self.readCardChance(self.card)
      if self.card != 16:
        self.listOfChance.append(self.card)
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

  def payRent(self):
    self.namingShortcut()
    if self.isPlayer == False:
      if self.playerOwnedProperties[self.color][self.name][2] == True:
        print("This property is mortgaged.")
      elif self.square == -1 and self.color in self.playerOwnedSets:
        if self.color == "Utilities":
           self.giveMoney(self.move * 10)
           self.receiveRent(self.move * 10)
        else:
          house = self.playerOwnedProperties[self.color][self.name][1]
          if house > 4:
            self.giveMoney(self.rentLookup(self.name, True, False, True))
            self.receiveRent(self.rentLookup(self.name, True, False, True))
          else:
            self.giveMoney(self.rentLookup(self.name, True, house))
            self.receiveRent(self.rentLookup(self.name, True, house))
      elif self.square == -1 and self.color not in self.playerOwnedSets:
        if self.color == "Utilities":
          self.giveMoney(self.move * 4)
          self.receiveRent(self.move * 4)
        else:
          self.giveMoney(self.rentLookup(self.name))
          print(self.robotMoneySum)
          self.receiveRent(self.rentLookup(self.name))
          print(self.playerMoneySum)

      #social here, anger.

    else:
      if self.ownedProperties[self.color][self.name][2] == True:
        print("This property is mortgaged.")
      elif self.square == 1 and self.color in self.ownedSets:
        house = self.ownedProperties[self.color][self.name][1]
        if house > 4:
          self.giveMoney(self.rentLookup(self.name, True, False, True))
          self.receiveRent(self.rentLookup(self.name, True, False, True))
        else:
          self.giveMoney(self.rentLookup(self.name, True, house))
          self.receiveRent(self.rentLookup(self.name, True, house))
      elif self.square == 1 and self.color not in self.ownedSets:
        self.giveMoney(self.rentLookup(self.name))
        self.receiveRent(self.rentLookup(self.name))


  def endTurn(self):
    self.turnCounter -= 1
    if self.isPlayer == True:
      self.isPlayer = False
    else:
      self.isPlayer = True
    #Taunting here. Social

  def checkBankruptcy(self):
    if self.isPlayer == True:
      if self.playerMoneySum == 0 and self.playerNumProperties == 0:
        return True
        #Trump voice, demand recount.
    else:
      if self.robotMoneySum == 0 and self.robotNumProperties == 0:
        return True
    return False


class Jail(Actions):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.robotInJail = False
    self.playerInJail = False
    self.robotJailFree = False
    self.playerJailFree = False
    
  def goToJail(self):
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
    temp = rules.rollDice()
    if temp[0] == temp[1]:
      #Bragging
      if self.isPlayer == False:
        self.robotInJail = False
        
      else:
        self.playerInJail = False
    else:
      return


class Decisions(Jail):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.doubleCounter = 0

  def playerDecisions(self):
    c = self.playerStartTurn()
    endTurn = False
    while endTurn == False:
      if c == 1 or c == 2:
        if c == 1:
          self.doubleCounter = 0
        choice = int(
          input(
            "(1) Buy\n(2) Sell Houses\n(3)Mortgage Properties\n(4) Check Balance\n(5) Declare Bankruptcy\n(6) End Turn: "
          ))
      else:
        choice = int(
          input(
            "(1) Buy\n(2) Sell\n(3)Mortgage\n(4) Check Balance\n(5) Declare Bankruptcy\n(6) Skip Turn\n(7) Roll Dice: "
          ))
      if choice == 1:
        choice2 = int(input("(1) Buy Property\n(2) Buy Upgrade: "))
        if choice2 == 1:
          self.buy()
        elif choice2 == 2:
          if len(self.playerOwnedSets) != 0:
            print("Your current completed sets are " +
                  str(self.playerOwnedSets))
            i = input("What color set would you like to build on?: ")
            self.buyHouse(i)
          else:
            print("You don't have any completed sets!")
      elif choice == 3:
        self.mortgage()
      elif choice == 4:
        print(self.playerMoneySum)
        print("A more detailed breakdown: " + str(self.playerMoney))
        if len(self.playerOwnedProperty) != 0:
          print(self.playerOwnedProperty)
        else:
          print("You own no properties!")

      elif choice == 5:
        self.checkBankruptcy()

      elif choice == 6:
        break
      elif choice == 7:
        r = rules.rollDice()
        print("You rolled (" + str(r[0]) + "," + str(r[1]) + ").")
        self.updatePosition(r[0] + r[1])
        c = 1
    if c == 2:
      self.doubleCounter += 1
      if self.doubleCounter == 4:
        self.goToJail()
      else:
        self.playerDecisions()
      
    return
    """match int(choice):
        case 1:
          choice2 = input("(1) Buy Properties\n(2) Improve Property: ")
          match int(choice2):
            case 1:
              self.buy()
            case 2:
              if len(self.playerOwnedSets) != 0:
                print("Your current completed sets are " + str(self.playerOwnedSets))
                i = input("What color set would you like to build on?: ")
                self.buyHouse(i)
              else:
                print("You don't have any completed sets!")
        case 2:
          return
        case 3:
          self.mortgage()
        case 4:
          print(self.playerMoneySum)
          print("A more detailed breakdown: " + str(self.playerMoney))
          if len(self.playerOwnedProperty) != 0:
            print(self.playerOwnedProperty)
          else:
            print("You own no properties!")
            
          
        case 5:
          self.checkBankruptcy()
        case 6:
          endTurn = True
        case 7:
          r = rules.rollDice()
          self.updatePosition(r[0] + r[1])
          c = 1"""

  def playerStartTurn(self):
    print("It is your turn! Would you like to roll the dice?")
    playerIn = input("[y/n]: ")
    if playerIn == "y":
      r = rules.rollDice()
      print("You rolled (" + str(r[0]) + "," + str(r[1]) + ").")
      self.updatePosition(r[0] + r[1])
      if r[0] == r[1]:
        return 2
      else:
        return 1
    return 0
    """match playerIn:
      case "y":
        r = rules.rollDice()
        self.updatePosition(r[0] + r[1])
        return 1
      case "n":
        return 0"""
    
  def robotDecision(self):
    ownedWeights = {}
    self.namingShortcut()
    print(self.Board[self.space])
    print(self.square)
    if self.square == 0:
      self.buy()
    if self.robotMoneySum <= 300:
      self.mortgage()
    if len(self.ownedSets) > 0:
      for color in self.ownedSets:
        ownedWeights[color] = self.weights[color]
      max_key = max(ownedWeights, key=ownedWeights.get)
      self.buyHouse(max_key)


class PlayGame(Decisions):

  def startGame(self):
    robotRoll = rules.gameSetup()
    robotSum = robotRoll[0] + robotRoll[1]
    r = rules.rollDice()
    playerSum = r[0] + r[1]
    print("You rolled ({}, {})".format(r[0], r[1]))
    if robotSum > playerSum:
      print("I will be going first!")
    else:
      print("You will be going first!")
      self.isPlayer = True

  def robotTurn(self):
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
      r = rules.rollDice()
      print("I rolled (" + str(r[0]) + ", " + str(r[1]) + ")")
      self.updatePosition(r[0] + r[1])
      self.robotDecision()
      if r[0] == r[1]:
        self.doubleCounter += 1
        if self.doubleCounter == 4:
          self.goToJail()
          self.doubleCounter = 0
        else:    
          self.robotTurn()
      else:
        self.doubleCounter = 0
        self.endTurn()
      print(self.robotMoneySum)
      print(self.robotMoney)
      print(self.robotOwnedProperty)
      print("\n")

  def playerTurn(self):
    if self.playerInJail == False:
      self.playerDecisions()
      self.endTurn()
      print("\n")
    else:
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
        
  def playGame(self):
    self.startGame()
    while self.turnCounter > 0:
      if self.isPlayer == True:
        self.playerTurn()
      else:
        self.robotTurn()
      sleep(1)


class debug(PlayGame):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setDebug = False
    inp = input("Would you like to enter debug mode? [y/n]: ")
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
      
def writePublisher():
    pub = rospy.Publisher('spaceInfo', Int16, queue_size = 10) # Message "object": Topic name, message type, number of messages to queue up
    rate = rospy.Rate(1)   # send at 1 Hz intervals
    variable = 5 # fake dice roll of value 5
    while not rospy.is_shutdown():
        testMessage = str(variable)
        pub.publish(testMessage)


def playTurn():
  d = debug()
  d.playGame()
  rospy.init_node('AI')       # This .py file must be associated with a ROS node
  while not rospy.is_shutdown():
    writePublisher()


if __name__ == "__main__":
  playTurn()
