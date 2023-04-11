#This is importing the rules made by Adam, which controls how the game is played
import rules
from time import sleep
#This is to generate a random order for the cards
import random as rd
#restructured the AI code to make it more readable
class board(rules.BoardSpaces, rules.TitleDeedCards):
  #Reorganized to start at 0, with 0 representing Go. -2 means unbuyable, 0 means unpurchased, 1 means owned by BoardBot, and -1 means owned by another player. 
  #[Ownership, Color Set, Name, # of properties in the set]
  
  Board = { 0: [-2, "Go"], 
            1: [0, "Brown", "Mediterrean Avenue", 2], 
            2: [-2, "CommunityChest"],
            3: [0, "Brown", "Baltic Avenue", 2],
            4: [-2, "IncomeTax"],
            5: [0, "Railroad", "Reading Railroad", 4], 
            6: [0, "LightBlue", "Oriental Avenue", 3],
            7: [-2, "Chance"],
            8: [0, "LightBlue", "Vermont Avenue", 3], 
            9: [0, "LightBlue", "Connecticut Avenue", 3], 
            10:[-2, "Jail"],
            11:[0, "Magenta", "St Charles Place", 3],
            12:[0, "Utilities", "Electric Company", 2],
            13:[0, "Magenta", "States Avenue", 3],
            14:[0, "Magenta", "Virginia Avenue", 3],
            15:[0, "Railroad", "Pennsylvania Railroad", 4],
            16:[0, "Orange", "St James Place", 3],
            17:[-2, "Community Chest"],
            18:[0, "Orange", "Tennessee Avenue", 3],
            19:[0, "Orange", "New York Avenue", 3],
            20:[-2, "Free Parking"],
            21:[0, "Red", "Kentucky Avenue", 3],
            22:[-2, "Chance"],
            23:[0, "Red", "Indiana Avenue", 3],
            24:[0, "Red", "Illinois Avenue", 3],
            25:[0, "Railroad", "B&O Railroad", 4],
            26:[0, "Yellow", "Atlantic Avenue", 3],
            27:[0, "Yellow", "Ventnor Avenue", 3],
            28:[0, "Utilities", "Water Works", 2],
            29:[0, "Yellow", "Marvin Gardens", 3],
            30:[-2, "Go To Jail"],
            31:[0, "Green", "Pacific Avenue", 3],
            32:[0, "Green", "North Carolina Avenue", 3],
            33:[-2, "Community Chest"],
            34:[0, "Green", "Pennsylvania Avenue", 3],
            35:[0, "Railroad", "Shortline", 4],
            36:[-2, "Chance"],
            37:[0, "DarkBlue", "Park Place", 2],
            38:[-2, "Luxury Tax"],
            39:[0, "DarkBlue", "Boardwalk", 2],
          }

#currPos tracks the current position of both the player and the robot. This is done with creating an object for both the player and the robot so they do not intefer with each other.   
  currPos = 0
#turnCounter is used to track the number of turns the AI has taken. We plan on having them play up to 50 rounds, and when that is up, the game will end. 
  turnCounter = 50
#numPlayers is the number of other players in the game, currently we are only creating a 1-on-1 experience. 
  #numPlayers = input("How many players are playing?: ")
  numPlayers = 1

  #This is to make the code easier to read as well as to code. The time complexity should be O(1).
  def namingShortcut(self):
    #This is the type of square as described above. It stores either -2, -1, 0, or 1. 
    self.square = self.Board[self.currPos][0]
    if self.square == -2:
      #After check if it is an unbuyable square, which it is, this stores the name of the square. 
      self.name = self.Board[self.currPos][1]
    else:
      #This stores the type or color the property is. For example, it could store yellow or railroad. 
      self.color = self.Board[self.currPos][1]
      #This stores the name of the property. 
      self.name = self.Board[self.currPos][2]
      #This stores the number of properties in the set. This is for AI to prioritize finishing sets. 
      self.numInColor = self.Board[self.currPos][3]
      #This stores the price of the property. 
      self.price = self.board[self.currPos][3]
      #This stores the price that it costs to build houses and hotels on the property. 
      self.buildPrice = self.cards[self.currPos][1]

  #This is to update the position after a roll. If the current position is above 39, then it will reset to below 39 and the passGo function will be called. 
  def updatePosition(self, sum):
    #This will add the dice roll to the current position variable.
    self.currPos += sum
    #This checks if the value stored in currPos is over or equal to 40, which is Go. If it is pass Go and collect $200 by calling passGo().  
    if self.currPos >= 40:
      self.currPos -= 40
      self.passGo()
    self.namingShortcut()
    if self.square == -2:
      #This prints the square that the robot/player lands on if it is a special square, and depending on the special square, does different things. 
      print ("I landed on " + self.name)
      match self.name:
        case "Community Chest":
          self.pullCard()
        case "Chance":
          self.pullCard()
        case "Income Tax":
          self.giveMoney(min(200, self.robotMoneySum * 0.1))
        case "Go To Jail":
          self.currPos = 10
          self.inJail = True
        case "Luxury Tax":
          self.giveMoney(75)
          #Else, it will just print what property it landed on. This is probably where we will call the movement of the robot. 
    else:
      print("I landed on " + self.name)

  #This is to update the board dictionary to reflect the current state of the board. Requires computer vision to work. 
  def updateOwnership(self, change):
    self.namingShortcut()
    #This is if the robot will buy the property. 
    if change == "buy":
      self.Board[self.currPos][0] = 1
    #This is if the robot or player will sell the property. 
    elif change == "sell" or change == "oppSell":
      self.Board[self.currPos][0] = 0
    #And this is if the player will buy the property. I use opp as it is an opponent to the robot. 
    elif change == "oppBuy":
      self.square = -1
    print("Board state updated.")
        
    
#This class is used to tally and organize all of the assets BoardBot has, including properties and money. Will add house and hotel trackers later. 
class Assets(board):
  def __init__(self):
    self.robotMoney = {500: 2, 100: 2, 50: 2, 20: 6, 10: 5, 5: 5, 1: 5}
    self.robotMoneySum = 1500
    self.ownedProperties = {"Brown": {"Mediterranean Avenue": [False, 0], "Baltic Avenue": [False, 0]},
                            "LightBlue":{"Oriental Avenue": [False, 0], "Vermont Avenue": [False, 0], "Connecticut Avenue": [False, 0]},
                            "Magenta":{"St Charles Place": [False, 0], "States Avenue": [False, 0], "Virginia Avenue":[False, 0]},
                            "Orange":{"St James Place": [False, 0], "Tennessee Avenue": [False, 0], "New York Avenue": [False, 0]},
                            "Red": {"Kentucky Avenue": [False, 0], "Indiana Avenue": [False, 0], "Illinois Avenue": [False, 0]},
                            "Yellow": {"Atlantic Avenue": [False, 0], "Ventnor Avenue": [False, 0], "Marvin Gardens": [False, 0]},
                            "Green":{"Pacific Avenue": [False, 0], "North Carolina Avenue": [False, 0], "Pennsylvania Avenue": [False, 0]},
                            "DarkBlue":{"Park Place": [False, 0], "Boardwalk": [False, 0]},
                            "Railroad":[0],
                            "Utilities":[0]
                           }
    self.numProperties = 0
    self.ownedSets = []
    #self.listOfCC = rd.sample(range(1, 17), 16)
    self.listOfCC = rd.sample(range(1, 7), 6)
    
  #This is called when BoardBot gains money, and will both alter the total money it has and what bills it has as well. 
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
          return
#The opposite of gainMoney, works the same way. 
  def giveMoney(self, amount):
    self.robotMoneySum -= amount
    while amount > 0:
      for i in self.robotMoney:
        if amount >= i and self.robotMoney[i] > 0:
          temp = amount // i
          self.robotMoney[i] -= temp
          amount -= (i * temp)
        if amount == 0:
          return
          
"""def isASet(self):
    for key in self.ownedProperties:
      if key == "Railroad" or key == "Utilities":
        continue
      elif all(value == True for value in self.ownedProperties[key].values())
        self.ownedSets.append(key)"""
      
#These are the types of actions that the robot can take. Will include buying property, etc.   
class Actions(Assets, rules.ChanceCommunityCards):
  def passGo(self):
    self.gainMoney(200)

  def buy(self):
    self.namingShortcut()
    if self.square != -2:
      self.leftoverMoney = self.robotMoneySum-self.price
      if self.square != -1:
        if self.leftoverMoney >=350:
          self.updateOwnership("buy")
          self.giveMoney(self.price)
          if self.color == "Railroad" or self.color == "Utilities":
            self.ownedProperties[self.color].append(self.name)
          else:
            self.ownedProperties[self.color][self.name][0] = True
          self.numProperties += 1
      
  def upgradeProperty(self):
    return
      
      
  def readCardCC(self, cardNum):
    match cardNum:
      case 1:
        return True
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

  def bankruptcy(self):
    if self.robotMoneySum == 0 and self.numProperties == 0:
      print("I have lost. Good Game!\nWould you like to play again?")
      return True
    return False

  

  def endTurn(self):
    self.turnCounter -= 1
    return;
    
      


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



class Opponent(Jail):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.playerMoney = {500: 2, 100: 2, 50: 2, 20: 6, 10: 5, 5: 5, 1: 5}
    self.playerMoneySum = 1500
    self.playerOwnedProperties = {"Brown": {"Mediterranean Avenue": [False, 0], "Baltic Avenue": [False, 0]},
                            "LightBlue":{"Oriental Avenue": [False, 0], "Vermont Avenue": [False, 0], "Conneticut Avenue": [False, 0]},
                            "Magenta":{"St Charles Place": [False, 0], "States Avenue": [False, 0], "Virginia Avenue":[False, 0]},
                            "Orange":{"St James Place": [False, 0], "Tennessee Avenue": [False, 0], "New York Avenue": [False, 0]},
                            "Red": {"Kentucky Avenue": [False, 0], "Indiana Avenue": [False, 0], "Illinois Avenue": [False, 0]},
                            "Yellow": {"Atlantic Avenue": [False, 0], "Ventnor Avenue": [False, 0], "Marvin Gardens": [False, 0]},
                            "Green":{"Pacific Avenue": [False, 0], "North Carolina Avenue": [False, 0], "Pennsylvania Avenue": [False, 0]},
                            "DarkBlue":{"Park Place": [False, 0], "Boardwalk": [False, 0]},
                            "Railroad":[0],
                            "Utilities":[0]
                           }
  def gainMoney(self, amount):
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
    self.playerMoneySum -= amount
    while amount > 0:
      for i in self.playerMoney:
        if amount >= i and self.robotMoney[i] > 0:
          temp = amount // i
          self.playerMoney[i] -= temp
          amount -= (i * temp)
        if amount == 0:
          return
  
  def buy(self):
    self.namingShortcut()
    self.leftoverMoney = self.playerMoneySum-self.price
    if self.square != -2 and self.square != 1:
      if self.leftoverMoney >=350:
        self.updateOwnership("oppBuy")
        self.giveMoney(self.price)
        if self.color == "Railroad" or self.color == "Utilities":
          self.playerOwnedProperties[self.color].append(self.name)
        else:
          self.playerOwnedProperties[self.color][self.name][0] = True
        self.numProperties += 1
    
class debug(Jail):
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
  
#This is where most of the code will run. 
def playTurn():
  d = debug()
  o = Opponent()
  
  rules.gameSetup()
  while(d.turnCounter != 0):
    r = rules.rollDice()
    d.updatePosition(r[0]+r[1])
    if d.currPos in [2, 17, 33] and d.card == 6:
      o.giveMoney(10)
    d.buy()
    d.endTurn()
    print("\n\n\n")
    sleep(5)
    
    


if __name__ == "__main__":
  playTurn()
