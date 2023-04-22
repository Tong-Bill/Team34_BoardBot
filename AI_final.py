import rules
from time import sleep
import random as rd
#new Board which is a dict that is [type of square, color/name, name, weight]. Weight is used for selling properties and is found using data online on which properties are the most valuable. 
class board(rules.BoardSpaces, rules.TitleDeedCards):
  Board = { 0: [-2, "Go"], 
            1: [0, "Brown", "Mediterrean Avenue", 0.2], 
            2: [-2, "CommunityChest"],
            3: [0, "Brown", "Baltic Avenue", 0.2],
            4: [-2, "IncomeTax"],
            5: [0, "Railroad", "Reading Railroad", 0.8], 
            6: [0, "LightBlue", "Oriental Avenue", 0.3],
            7: [-2, "Chance"],
            8: [0, "LightBlue", "Vermont Avenue", 0.3], 
            9: [0, "LightBlue", "Connecticut Avenue", 0.3], 
            10:[-2, "Jail"],
            11:[0, "Magenta", "St Charles Place", 0.4],
            12:[0, "Utilities", "Electric Company", 0.1],
            13:[0, "Magenta", "States Avenue", 0.4],
            14:[0, "Magenta", "Virginia Avenue", 0.4],
            15:[0, "Railroad", "Pennsylvania Railroad", 0.8],
            16:[0, "Orange", "St James Place", 0.9],
            17:[-2, "Community Chest"],
            18:[0, "Orange", "Tennessee Avenue", 0.9],
            19:[0, "Orange", "New York Avenue", 0.9],
            20:[-2, "Free Parking"],
            21:[0, "Red", "Kentucky Avenue", 1],
            22:[-2, "Chance"],
            23:[0, "Red", "Indiana Avenue", 1],
            24:[0, "Red", "Illinois Avenue", 1],
            25:[0, "Railroad", "B&O Railroad", 0.8],
            26:[0, "Yellow", "Atlantic Avenue", 0.6],
            27:[0, "Yellow", "Ventnor Avenue", 0.6],
            28:[0, "Utilities", "Water Works", 0.1],
            29:[0, "Yellow", "Marvin Gardens", 0.6],
            30:[-2, "Go To Jail"],
            31:[0, "Green", "Pacific Avenue", 0.5],
            32:[0, "Green", "North Carolina Avenue", 0.5],
            33:[-2, "Community Chest"],
            34:[0, "Green", "Pennsylvania Avenue", 0.5],
            35:[0, "Railroad", "Shortline", 0.8],
            36:[-2, "Chance"],
            37:[0, "DarkBlue", "Park Place", 0.7],
            38:[-2, "Luxury Tax"],
            39:[0, "DarkBlue", "Boardwalk", 0.7],
  }

  def __init__(self, player=False):
    self.isPlayer = player
    self.currPos = 0
    self.playerPos = 0
    self.turnCounter = 50
    #numPlayers = input("How many players are playing?: ")
    self.numPlayers = 1
    self.weights = {"Brown": 0.2, "Railroad": 0.8, "LightBlue": 0.3, "Magenta": 0.4, "Orange": 0.9, "Red": 1, "Yellow": 0.6, "Green": 0.5, "DarkBlue": 0.7}

  def namingShortcut(self): 
    x = self.currPos
    if self.isPlayer == True:
      x = self.playerPos
    self.square = self.Board[x][0]
    if self.square == -2: 
      self.name = self.Board[x][1]
    else: 
      self.color = self.Board[x][1] 
      self.name = self.Board[x][2] 
      self.numInColor = self.Board[x][3]
      self.price = self.board[x][3]

  def updatePosition(self, sum):
    if self.isPlayer == True:
      self.playerPos += sum  
      if self.playerPos >= 40:
        self.playerPos -= 40
        self.passGo()
    else:
      self.currPos += sum
      if self.currPos >= 40:
        self.currPos -= 40
        self.passGo()
      
    self.namingShortcut()
    
    if self.square == -2:
      if self.isPlayer == False:
        print ("I landed on " + self.name)
      else:
        print("You've landed on " + self.name)
      match self.name:
        case "Community Chest":
          self.pullCard()
        case "Chance":
          self.pullCard()
        case "Income Tax":
          if self.isPlayer == False:
            self.giveMoney(min(200, self.robotMoneySum * 0.1))
          else:
            self.giveMoney(min(200, self.playerMoneySum * 0.1))
        case "Go To Jail":
          self.currPos = 10
          self.inJail = True
        case "Luxury Tax":
          self.giveMoney(75)

    else:
      if self.isPlayer == False:
        print("I landed on " + self.name)
      else:
        print("You've landed on " + self.name)

  def updateOwnership(self, change):
    self.namingShortcut()
 
    if change == "buy":
      self.Board[self.currPos][0] = 1

    elif change == "sell" or change == "oppSell":
      self.Board[self.currPos][0] = 0

    elif change == "oppBuy":
      self.square = -1
    print("Board state updated.")

class Assets(board):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    self.robotMoney = {500: 2, 100: 2, 50: 2, 20: 6, 10: 5, 5: 5, 1: 5}
    self.playerMoney = {500: 2, 100: 2, 50: 2, 20: 6, 10: 5, 5: 5, 1: 5}
    self.robotMoneySum = 1500
    self.playerMoneySum = 1500
    
    self.ownedProperties = {"Brown": {"Mediterranean Avenue": [False, 0, False], "Baltic Avenue": [False, 0, False]},
                            "LightBlue":{"Oriental Avenue": [False, 0, False], "Vermont Avenue": [False, 0], "Connecticut Avenue": [False, 0, False]},
                            "Magenta":{"St Charles Place": [False, 0, False], "States Avenue": [False, 0, False], "Virginia Avenue":[False, 0, False]},
                            "Orange":{"St James Place": [False, 0, False], "Tennessee Avenue": [False, 0, False], "New York Avenue": [False, 0, False]},
                            "Red": {"Kentucky Avenue": [False, 0, False], "Indiana Avenue": [False, 0, False], "Illinois Avenue": [False, 0, False]},
                            "Yellow": {"Atlantic Avenue": [False, 0, False], "Ventnor Avenue": [False, 0, False], "Marvin Gardens": [False, 0, False]},
                            "Green":{"Pacific Avenue": [False, 0, False], "North Carolina Avenue": [False, 0, False], "Pennsylvania Avenue": [False, 0, False]},
                            "DarkBlue":{"Park Place": [False, 0, False], "Boardwalk": [False, 0, False]}, 
                            "Railroad":{"Reading Railroad": [False, 0, False], "Pennsylvania Railroad":[False, 0, False], "B&O Railroad":[False, 0, False], "Shortline":[False, 0, False]},
                            "Utilities":{"Electric Company:":[False, 0, False], "Water Works":[False, 0, False]}
    }
    
    self.playerOwnedProperties = {"Brown": {"Mediterranean Avenue": [False, 0, False], "Baltic Avenue": [False, 0, False]},
                            "LightBlue":{"Oriental Avenue": [False, 0, False], "Vermont Avenue": [False, 0], "Connecticut Avenue": [False, 0, False]},
                            "Magenta":{"St Charles Place": [False, 0, False], "States Avenue": [False, 0, False], "Virginia Avenue":[False, 0, False]},
                            "Orange":{"St James Place": [False, 0, False], "Tennessee Avenue": [False, 0, False], "New York Avenue": [False, 0, False]},
                            "Red": {"Kentucky Avenue": [False, 0, False], "Indiana Avenue": [False, 0, False], "Illinois Avenue": [False, 0, False]},
                            "Yellow": {"Atlantic Avenue": [False, 0, False], "Ventnor Avenue": [False, 0, False], "Marvin Gardens": [False, 0, False]},
                            "Green":{"Pacific Avenue": [False, 0, False], "North Carolina Avenue": [False, 0, False], "Pennsylvania Avenue": [False, 0, False]},
                            "DarkBlue":{"Park Place": [False, 0, False], "Boardwalk": [False, 0, False]}, 
                            "Railroad":{"Reading Railroad": [False, 0, False], "Pennsylvania Railroad":[False, 0, False], "B&O Railroad":[False, 0, False], "Shortline":[False, 0, False]},
                            "Utilities":{"Electric Company:":[False, 0, False], "Water Works":[False, 0, False]}
    }
    self.robotOwnedProperty, self.playerOwnedProperty = [], []
    self.robotNumProperties, self.playerNumProperties = 0, 0
    self.house, self.playerHouse, self.hotel, self.playerHotel = 0, 0, 0, 0
    self.ownedSets, self.playerOwnedSets = set(), set()
    #self.listOfCC = rd.sample(range(1, 17), 16)
    self.listOfCC = rd.sample(range(1, 7), 6)

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

  def giveMoney(self, amount):
    if self.isPlayer == False:
      self.robotMoneySum -= amount
      while amount > 0:
        for i in self.robotMoney:
          if amount >= i and self.robotMoney[i] > 0:
            temp = amount // i
            self.robotMoney[i] -= temp
            amount -= (i * temp)
          if amount == 0:
            return
    else:
      self.playerMoneySum -= amount
      while amount > 0:
        for i in self.playerMoney:
          if amount >= i and self.playerMoney[i] > 0:
            temp = amount // i
            self.playerMoney[i] -= temp
            amount -= (i * temp)
          if amount == 0:
            return

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
        self.leftoverMoney = self.robotMoneySum-self.price
        if self.leftoverMoney >=350:
          self.updateOwnership("buy")
          self.giveMoney(self.price)
          self.ownedProperties[self.color][self.name][0] = True
          self.robotOwnedProperty.append(self.name)
          self.robotNumProperties += 1
          if self.isASet(self.color) and (self.color != "Utilities" or self.color != "Railroads"):
            self.ownedSets.add(self.color)
            
      else:
        self.leftoverMoney = self.playerMoneySum-self.price
        if self.leftoverMoney >=350:
          self.updateOwnership("oppBuy")
          self.giveMoney(self.price)
          self.playerOwnedProperties[self.color][self.name][0] = True
          self.playerOwnedProperty.append(self.name)
          self.playerNumProperties += 1
          if self.isASet(self.color) and (self.color != "Utilities" or self.color != "Railroads"):
            self.ownedSets.add(self.color)

  def buyHouse(self, color):
    prop = dict()
    if self.isPlayer == False and self.isSet(color) and self.isMortgaged(color) == False:
      for name in self.ownedProperties[color]:
        prop[name] = self.ownedProperties[color][name][1]
      most_houses = max(prop.values())
      if all(value == most_houses for value in prop.values()):
        house = rd.choice([prop.keys()])
        self.addHouse(color, house)
      else:
        least_houses = min(prop.values())
        min_keys = [m for m in prop if prop[m] == least_houses]
        key = rd.choice(min_keys)
        self.addHouse(color, key)

    elif self.isPlayer == True and self.isSet(color) and not self.isMortgaged(color) == False:
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
    x = self.robotMoneySum - self.cards[choice][1]
    
    if x >= 350 and self.isPlayer == False:
      print("Adding a house to " + choice)
      self.giveMoney(self.getBuildCost(choice))
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
          choice2 = input("Are your sure? You will not be able to buy houses in this color set anymore [y/n]: ")
          match choice2:
            case "y":
              self.gainMoney(self.mortgageProperty(choice))
              self.playerOwnedProperties[color][choice][2] = True
              return
            case "n":
              return
        elif choice in prop[color]:
          self.gainMoney(self.mortgageProperty(choice))
          self.playerOwnedProperties[color][choice][2] = True
    else:
      return
          
  def readCardCC(self, cardNum):
    match cardNum:
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
        return False

  def pullCard(self):
    self.card = self.listOfCC.pop(0)
    self.readCardCC(self.card)
    self.listOfCC.append(self.card)
    if self.currPos in [2, 17, 33]:
      self.card = self.listOfCC.pop(0)
      self.readCardCC(self.card)
      self.listOfCC.append(self.card)
    elif self.currPos in [7, 22, 36]:
      return

  def endTurn(self):
    self.turnCounter -= 1
    if self.isPlayer == True:
      self.isPlayer = False
    else:
      self.isPlayer = True

  def checkBankruptcy(self):
    if self.isPlayer == True:
      if self.playerMoneySum == 0 and self.playerNumProperties == 0:
        return True
    else:
      if self.robotMoneySum == 0 and self.robotNumProperties == 0:
        return True
    return False
        
class Jail(Actions):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.inJail = False

  def goToJail(self):
    if self.currPos == 30:
      self.inJail = True
    elif self.currPos in [2, 7, 17, 22, 33, 36]:
      if self.pullCard() == 15:
        self.inJail = True

  def payFine(self):
    self.giveMoney(50)

  def rollOut(self):
    temp = rules.rollDice()
    if temp[0] == temp[1]:
      return True
    return False

class Decisions(Jail):
  
  def playerDecisions(self):
    c = self.playerStartTurn()
    endTurn = False
    while endTurn == False:
      if c == 1:
        choice = input("(1) Buy\n(2) Sell Houses\n(3)Mortgage Properties\n(4) Check Balance\n(5) Declare Bankruptcy\n(6) End Turn: ")
      else:
        choice = input("(1) Buy\n(2) Sell\n(3)Mortgage\n(4) Check Balance\n(5) Declare Bankruptcy\n(6) Skip Turn\n(7) Roll Dice: ")
      match int(choice):
        case 1:
          choice2 = input("(1) Buy Properties\n(2) Improve Property: ")
          match int(choice2):
            case 1:
              self.buy()
            case 2:
              if len(self.playerOwnedSets) > 0:
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
          c = 1
          
  
  def playerStartTurn(self):
    print("It is your turn! Would you like to roll the dice?")
    playerIn = input("[y/n]: ")
    match playerIn:
      case "y":
        r = rules.rollDice()
        self.updatePosition(r[0] + r[1])
        return 1
      case "n":
        return 0

  def robotDecision(self):
    ownedWeights = {}
    if len(self.ownedSets) > 0:
      for color in self.ownedSets:
        ownedWeights[color] = self.weights[color]
      max_key = max(ownedWeights, key=ownedWeights.get)
      self.buyHouse(max_key)

    self.buy()
    
        

class PlayGame(Decisions):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.d = Decisions()
    
  def startGame(self):
    robotRoll = rules.gameSetup()
    robotSum = robotRoll[0] + robotRoll[1]
    r = rules.rollDice()
    playerSum = r[0] + r[1]
    if robotSum > playerSum:
      print("I will be going first!")
    else:
      print("You will be going first!")
      self.d.isPlayer = True

  def robotTurn(self):
    r = rules.rollDice()
    self.d.updatePosition(r[0] + r[1])
    self.d.robotDecision()
    self.d.endTurn()
    print(self.d.turnCounter)
    
  def playerTurn(self):
    self.d.playerDecisions()
    self.d.endTurn()
    
  def playGame(self):
    self.startGame()
    while self.turnCounter > 0:
      if self.d.isPlayer == True:
        self.playerTurn()
      else:
        self.robotTurn()
      sleep(3)
    
    
class debug(PlayGame):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setDebug = False
    inp = input("Would you like to enter debug mode? [y/n]: ")
    if inp.lower() == "y":
      print("Entering debug mode!")
      self.setDebug = True
    elif inp.lower() == "n":
      return;

  def debugMode(self):
    if self.setDebug == True:
      print("(1) Add Money\n(2) Add Property\n(3) Add House/Hotel")
      i = input()
      print (i)


def playTurn():
  d = debug()
  d.playGame()
    
    
  

if __name__ == "__main__":
  playTurn()
