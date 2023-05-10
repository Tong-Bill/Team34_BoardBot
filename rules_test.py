# Tests for Monopoly rules script
# Jacob Boe

import unittest
import sys
from math import ceil

sys.path.insert(0, '/home/team34/ros_ws/src/baxter_tools/scripts')

import rules

class TestMain(unittest.TestCase):
    def test_gameSetup(self):
        self.assertEqual(len(rules.gameSetup()), 2)
        

    def test_evaluateDice(self):
        diceRoll1 = [3, 3]
        diceRoll2 = [4]
        diceRoll3 = 1
        diceRoll4 = [7, 9]
        
        self.assertTrue(rules.evaluateDice(diceRoll1))
        self.assertFalse(rules.evaluateDice(diceRoll2))
        self.assertFalse(rules.evaluateDice(diceRoll3))
        self.assertFalse(rules.evaluateDice(diceRoll4))
      
#    def test_parseSpace(self):
#        boardSpaces = rules.BoardSpaces()
#        space1 = 1
#        space2 = 2
#        space3 = 41

#        self.assertEqual(boardSpaces.parseSpace(space1), "Options: own, buy, auction, pay rent")
#        self.assertEqual(boardSpaces.parseSpace(space2), "Draw card: community chest")
#        self.assertEqual(boardSpaces.parseSpace(space3), "Error: invalid board space!")
        
    def test_actionRules(self):
        boardSpaces = rules.BoardSpaces()
        space1 = 40
        space2 = 2
        space3 = 7
        space4 = 10
        space5 = 4
        space6 = 38
        space7 = 30
        space8 = 41
        
        self.assertEqual(boardSpaces.actionRules(space1), "Gain 200")
        self.assertEqual(boardSpaces.actionRules(space2), "Draw card: community chest")
        self.assertEqual(boardSpaces.actionRules(space3), "Draw card: chance")
        self.assertEqual(boardSpaces.actionRules(space4), "Do nothing")
        self.assertEqual(boardSpaces.actionRules(space5), "Pay 200")
        self.assertEqual(boardSpaces.actionRules(space6), "Pay 100")
        self.assertEqual(boardSpaces.actionRules(space7), "go to Jail")
        self.assertEqual(boardSpaces.actionRules(space8), "Error: undefined action in rules.py/actionRules")
        
    def test_rentLookup(self):    
        deedCards = rules.TitleDeedCards()
        p1Houses = 1
        p2Houses = 0
        p1Hotel = 1
        p2Hotel = 0
        p1Set = True
        p2Set = False
        p1Mortgage = True
        p2Mortgage = False
        space1 = "Mediterranean Avenue"
        space2 = "Invalid"
        
        self.assertEqual(deedCards.rentLookup(space1, p1Set, p1Houses, p1Hotel, p1Mortgage), 4)
        self.assertEqual(deedCards.rentLookup(space2, p1Set, p1Houses, p1Hotel, p1Mortgage), -1)
        self.assertEqual(deedCards.rentLookup(space1, p2Set, p1Houses, p1Hotel, p1Mortgage), 10)
        self.assertEqual(deedCards.rentLookup(space1, p2Set, p2Houses, p1Hotel, p1Mortgage), 250)
        self.assertEqual(deedCards.rentLookup(space1, p2Set, p2Houses, p2Hotel, p1Mortgage), 0)
        self.assertEqual(deedCards.rentLookup(space1, p2Set, p2Houses, p2Hotel, p2Mortgage), 2)
        
    def test_getBuildCost(self):
        deedCards = rules.TitleDeedCards()
        space1 = "Mediterranean Avenue"

        self.assertEqual(deedCards.getBuildCost(space1), 50)
        
    def test_mortgageProperty(self):
        deedCards = rules.TitleDeedCards()
        space1 = "Mediterranean Avenue"

        self.assertEqual(deedCards.mortgageProperty(space1), 30)
        
    def test_getSquare(self):
        deedCards = rules.TitleDeedCards()
        space1 = "Mediterranean Avenue"

        self.assertEqual(deedCards.getSquare(space1), 1)
        
    def test_buildHouse(self):
        buildings = rules.Buildings()
        mortgage1 = True
        mortgage2 = False
        houses1 = 5
        houses2 = 3
        houses3 = 0
        lowSet1 = 1
        lowSet2 = 5
        
        self.assertEqual(buildings.buildHouse(houses1, lowSet1, mortgage1), "error: mortgaged properties in set")
        self.assertEqual(buildings.buildHouse(houses1, lowSet1, mortgage2), "error: numHouses > 4")
        self.assertEqual(buildings.buildHouse(houses2, lowSet1, mortgage2), "error: numHouses not equal")
        self.assertEqual(buildings.buildHouse(houses3, lowSet2, mortgage2), "error: houseCount = 0")
        self.assertEqual(buildings.buildHouse(houses2, lowSet2, mortgage2), "house")
        
    def test_buildHotel(self):
        buildings = rules.Buildings()
        houses1 = 4
        houses2 = 3
        hotels1 = 0
        hotels2 = 1
        mortgage1 = True
        mortgage2 = False
        
        self.assertEqual(buildings.buildHotel(houses1, hotels2, mortgage1), "error: mortgaged properties in set")
        self.assertEqual(buildings.buildHotel(houses2, hotels2, mortgage2), "error: numHouses < 4")
        self.assertEqual(buildings.buildHotel(houses1, hotels1, mortgage2), "error: hotelCount = 0")
        self.assertEqual(buildings.buildHotel(houses1, hotels2, mortgage2), "hotel; houses -4")
    
    def test_evaluateDice(self):
        dice1 = [3, 3]
        dice2 = [4]
        dice3 = 1
        dice4 = ['7', '9']
        dice5 = [7, 9]
        
        self.assertFalse(rules.evaluateDice(dice2))
        self.assertFalse(rules.evaluateDice(dice3))
        self.assertFalse(rules.evaluateDice(dice4))
        self.assertTrue(rules.evaluateDice(dice1))
        self.assertFalse(rules.evaluateDice(dice5))
        
    def test_autoRollDice(self):
        self.assertEqual(len(rules.autoRollDice()), 2)
  
  # Integration test of rolling dice, checking roll is legit, adding dice, and recieving the correct space      
    def test_rollDiceParseSpace(self):
        diceRoll = rules.autoRollDice()
        diceBool = rules.evaluateDice(diceRoll)
        if diceBool is True:
            diceTotal = int(rules.diceTotal(diceRoll))
            boardSpaces = rules.BoardSpaces()
            
            if diceTotal == 2:
                self.assertEqual(boardSpaces.parseSpace(diceTotal), "Draw card: community chest")
            elif diceTotal == 4:
                self.assertEqual(boardSpaces.parseSpace(diceTotal), "Pay 200")
            elif diceTotal == 7:
                self.assertEqual(boardSpaces.parseSpace(diceTotal), "Draw card: chance")
            elif diceTotal == 10:
                self.assertEqual(boardSpaces.parseSpace(diceTotal), "Do nothing")
            elif diceTotal == 1 or 3 or 5 or 6 or 8 or 9 or 11 or 12:
                self.assertEqual(boardSpaces.parseSpace(diceTotal), "Options: own, buy, auction, pay rent")
        else:
            raise ValueError("Illegal dice roll")
    
    # Integration test of rolling dice, checking roll is legit, adding dice, and checking rent value if it is a property space
    def test_rollDiceRentLookup(self):
        diceRoll = rules.autoRollDice()
        diceBool = rules.evaluateDice(diceRoll)
        if diceBool is True:
            diceTotal = int(rules.diceTotal(diceRoll))
            propertySpaces = rules.TitleDeedCards()
            boardSpaces = rules.BoardSpaces()
            try:
                space = boardSpaces.board[diceTotal][2]
            except:
                space = "Not a property"  
            print(space)
            if space == "Mediterranean Avenue":
                self.assertEqual(propertySpaces.rentLookup(space), 2)
            elif space == "Baltic Avenue":
                self.assertEqual(propertySpaces.rentLookup(space), 4)
            elif space == "Reading Railroad":
                self.assertEqual(propertySpaces.rentLookup(space), 25)
            elif space == "Oriental Avenue":
                self.assertEqual(propertySpaces.rentLookup(space), 6)
            elif space == "Vermont Avenue":
                self.assertEqual(propertySpaces.rentLookup(space), 6)
            elif space == "Connecticut Avenue":
                self.assertEqual(propertySpaces.rentLookup(space), 8)
            elif space == "St Charles Place":
                self.assertEqual(propertySpaces.rentLookup(space), 10)
            elif space == "Electric Company":
                self.assertEqual(propertySpaces.rentLookup(space), 4)
            else:
                self.assertEqual(propertySpaces.rentLookup(space), -1)
        else:
            raise ValueError("Illegal space")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
