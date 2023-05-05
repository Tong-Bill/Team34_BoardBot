import AI

game = AI.debug()
game.isPlayer = True
game.updatePosition(5)
game.buy()
game.endTurn()
game.updatePosition(5)
print(game.robotMoneySum)
print(game.playerMoneySum)



