#!/usr/bin/env python
#import AI_No_Robot as AI
import AI
from time import sleep

def rentTest():
  """game = AI.debug()
  game.isPlayer = True #The player is playing
  game.updatePosition(37) #Buys Boardwalk
  game.buy()
  print("You have {} dollars.".format(game.playerMoneySum))
  game.updatePosition(2)
  game.buy()
  print("You have {} dollars.".format(game.playerMoneySum))
  game.endTurn()
  print("BoardBot has {} dollars".format(game.robotMoneySum))
  game.updatePosition(37)
  print("BoardBot has {} dollars".format(game.robotMoneySum))
  print("You have {} dollars.".format(game.playerMoneySum))"""

def houseTest2():
  game = AI.debug()
  game.isPlayer = True
  game.updatePosition(37)
  game.buy()
  game.updatePosition(2)
  game.buy()
  game.updatePosition(2)
  game.buy()
  game.updatePosition(2)
  game.buy()
  game.playerTurn()
  
def mortgageTest():
  game2 = AI.debug()
  game2.isPlayer = True
  game2.updatePosition(37)
  game2.buy()
  print("You have {} dollars.".format(game2.playerMoneySum))
  game2.mortgage()
  print("You have {} dollars.".format(game2.playerMoneySum))
  game2.endTurn()
  game2.updatePosition(37)
  print("BoardBot has {} dollars".format(game2.robotMoneySum))
  print("You have {} dollars.".format(game2.playerMoneySum))

def unmortgageTest():
  game3 = AI.debug()
  game3.isPlayer = False
  game3.updatePosition(37)
  game3.buy()
  print("BoardBot has {} dollars".format(game3.robotMoneySum))
  game3.mortgage()
  print("BoardBot has {} dollars".format(game3.robotMoneySum))
  game3.unmortgage()
  print("BoardBot has {} dollars".format(game3.robotMoneySum))
  
  
def houseTest():
  game4 = AI.debug()
  game4.isPlayer = True
  game4.updatePosition(37)
  game4.buy()
  game4.updatePosition(2)
  game4.buy()
  game4.buyHouse("DarkBlue")
  game4.buyHouse("DarkBlue")
  print("BoardBot has {} dollars".format(game4.playerMoneySum))
  print("The robot owns {} houses.".format(game4.playerHouse))
  

#rentTest()
houseTest2()
#mortgageTest()
#unmortgageTest()
#houseTest()
