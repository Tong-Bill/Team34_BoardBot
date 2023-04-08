import rules
from time import sleep
#restructured the AI code to make it more readable. 
class board(rules.boardSpaces, rules.TitleDeedCards):
  #Reorganized to start at 0, with 0 representing Go. -2 means unbuyable, 0 means unpurchased, 1 means owned by BoardBot, and -1 means owned by another player. 
  #[Ownership, Color Set, Name, # of properties in the set, weight]
  #The weight will be based off of data gathered here: https://bartwolff.com/Blog/2016/08/17/finding-the-most-valuable-monopoly-properties
  
  Board = { 0: [-2, "Go"], 
            1: [0, "Brown", "Mediterrean Avenue", 2, 0], 
            2: [-2, "CommunityChest"],
            3: [0, "Brown", "Baltic Avenue", 2, 0],
            4: [-2, "IncomeTax"],
            5: [0, "Railroad", "Reading Railroad", 4, 0], 
            6: [0, "LightBlue", "Oriental Avenue", 3, 0],
            7: [-2, "Chance"],
            8: [0, "LightBlue", "Vermont Avenue", 3, 0], 
            9: [0, "LightBlue", "Connecticut Avenue", 3, 0], 
            10:[-2, "Jail"],
            11:[0, "Magenta", "St Charles Place", 3, 0],
            12:[0, "Utilities", "Electric Company", 2, 0],
            13:[0, "Magenta", "States Avenue", 3, 0],
            14:[0, "Magenta", "Virginia Avenue", 3, 0],
            15:[0, "Railroad", "Pennsylvania Railroad", 4, 0],
            16:[0, "Orange", "St James Place", 3, 0],
            17:[-2, "Community Chest"],
            18:[0, "Orange", "Tennessee Avenue", 3, 0],
            19:[0, "Orange", "New York Avenue", 3, 0],
            20:[-2, "Free Parking"],
            21:[0, "Red", "Kentucky Avenue", 3, 0],
            22:[-2, "Chance"],
            23:[0, "Red", "Indiana Avenue", 3, 0],
            24:[0, "Red", "Illinois Avenue", 3, 0],
            25:[0, "Railroad", "B&O Railroad", 4, 0],
            26:[0, "Yellow", "Atlantic Avenue", 3, 0],
            27:[0, "Yellow", "Ventnor Avenue", 3, 0],
            28:[0, "Utilities", "Water Works", 2, 0],
            29:[0, "Yellow", "Marvin Gardens", 3, 0],
            30:[-2, "Go To Jail"],
            31:[0, "Green", "Pacific Avenue", 3, 0],
            32:[0, "Green", "North Carolina Avenue", 3, 0],
            33:[-2, "Community Chest"],
            34:[0, "Green", "Pennsylvania Avenue", 3, 0],
            35:[0, "Railroad", "Shortline", 4, 0],
            36:[-2, "Chance"],
            37:[0, "DarkBlue", "Park Place", 2, 0],
            38:[-2, "Luxury Tax"],
            39:[0, "DarkBlue", "Boardwalk", 2, 0],
          }
  #A tracker of the current position of BoardBot's piece and the number of times it has crossed Go. The goCounter is only useful for the first go around the board because the AI will buy every property on the first go around. 
  
  currPos = 0
  goCounter = 0
  turnCounter = 0

  #This is a function to make the code easier to read. Might make the runtime a bit longer, but it is O(1). 
  def namingShortcut(self):
    self.square = self.Board[self.currPos][0]
    if self.square == -2:
      self.name = self.Board[self.currPos][1]
    else:
      self.color = self.Board[self.currPos][1]
      self.name = self.Board[self.currPos][2]
      self.numInColor = self.Board[self.currPos][3]
      self.numHouses = self.Board[self.currPos][4]
      self.price = self.boardS[self.currPos][3]
      self.buildPrice = self.cards[self.currPos][1]

  #This is to update the position after a roll. If the current position is above 39, then it will reset to below 39 and the passGo function will be called. 
  def updatePosition(self, sum):
    self.currPos += sum
    if self.currPos > 39:
      self.currPos -= 39
      self.passGo()
    if self.Board[self.currPos][0] == -2:
      print ("I landed on " + self.Board[self.currPos][1])
    else:
      print("I landed on " + self.Board[self.currPos][2])

  #This is to update the board dictionary to reflect the current state of the board. Requires computer vision to work. 
  def updateOwnership(self, change):
    self.namingShortcut()
    if self.square != -2:
        if change == "buy":
          self.Board[self.currPos][0] = 1
        elif change == "sell" or change == "oppSell":
          self.Board[self.currPos][0] = 0
        elif change == "oppBuy":
          self.square = -1
    print("Board state updated.")
        
    
#This class is used to tally and organize all of the assets BoardBot has, including properties and money. Will add house and hotel trackers later. 
class Assets(board):
  def __init__(self):
    self.robotMoney = {500: 2, 100: 2, 50: 2, 20: 6, 10: 5, 5: 5, 1: 5}
    self.robotMoneySum = 1500
    self.ownedProperties = {"Brown": {"Mediterranean Avenue": [False, 0], "Baltic Avenue": [False, 0]},
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
    self.numProperties = 0
    self.ownedSets = []
    
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
    self.goCounter += 1
    self.gainMoney(200)

  def buy(self):
    self.namingShortcut()
    if self.square != -2:
      if self.robotMoneySum >= self.price and self.robotMoneySum-self.price >=350:
        self.updateOwnership("buy")
        self.giveMoney(self.price)
        self.ownedProperties[self.color][self.name][0] = True
        self.numProperties += 1
      
  def upgradeProperty(self):
    return
      
      
      

  def pullCard(self):
    if self.currPos in [2, 7, 17, 22, 33, 36]:
      return

  def bankruptcy(self):
    if self.robotMoneySum == 0 and self.numProperties == 0:
      print("I have lost. Good Game!\nWould you like to play again?")
      return True
    return False

  def endTurn(self):
    self.turnCounter += 1
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
  rules.gameSetup()
  while(d.turnCounter < 50):
    r = rules.rollDice()
    d.updatePosition(r[0]+r[1])
    d.buy()


if __name__ == "__main__":
  playTurn()
