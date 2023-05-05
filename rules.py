#!/usr/bin/env python

import rospy
from std_msgs.msg import (Int16, String, Int16MultiArray)

import rospy
import sys
import os
import random           # for random dice values
from math import ceil   # for rounding
from std_msgs.msg import String

def gameSetup():
    print("\n\nBegin setup:")
    print("Choose a banker. A human is preferred.")
    print("Each player starts with $1500.")
    # gainMoney (1500)
    print("Please shuffle the Community Chest and Chance cards, and place them facedown in their designated areas.")
    print("Choose a token. I will use my special token for easier gripping.")
    print("Roll the dice. High roll goes first.\n")
    result = autoRollDice()
    print("I rolled {0}\n".format(result))
    return result
# end gameSetup



# Contains rules for board spaces
# Note: This class does not contain state information such as owner.
# That information is stored in AI.py
class BoardSpaces(object):
    
            # Board space schema:
            # {spaceNumber: [Space type, <color set>, Property name, <cost>]}
            # Note that color set, cost, and rent only apply to "property" types
    board = {1: ["Property", "Brown", "Mediterrean Avenue", 60], 
           2: ["Action", "CommunityChest"],
           3: ["Property", "Brown", "Baltic Avenue", 60],
           4: ["Action", "IncomeTax"],
           5: ["Property", "Railroad", "Reading Railroad", 200], 
           6: ["Property", "LightBlue", "Oriental Avenue", 100],
           7: ["Action", "Chance"],
           8: ["Property", "LightBlue", "Vermont Avenue", 100], 
           9: ["Property", "LightBlue", "Connecticut Avenue", 120], 
           10:["Action", "Jail"],
           11:["Property", "Magenta", "St Charles Place", 140],
           12:["Property", "Utilities", "Electric Company", 150],
           13:["Property", "Magenta", "States Avenue", 140],
           14:["Property", "Magenta", "Virginia Avenue", 160],
           15:["Property", "Railroad", "Pennsylvania Railroad", 200],
           16:["Property", "Orange", "St James Place", 180],
           17:["Action", "Community Chest"],
           18:["Property", "Orange", "Tennessee Avenue", 180],
           19:["Property", "Orange", "New York Avenue", 200],
           20:["Action", "Free Parking"],
           21:["Property", "Red", "Kentucky Avenue", 220],
           22:["Action", "Chance"],
           23:["Property", "Red", "Indiana Avenue", 220],
           24:["Property", "Red", "Illinois Avenue", 240],
           25:["Property", "Railroad", "B&O Railroad", 200],
           26:["Property", "Yellow", "Atlantic Avenue", 260],
           27:["Property", "Yellow", "Ventnor Avenue", 260],
           28:["Property", "Utilities", "Water Works", 150],
           29:["Property", "Yellow", "Marvin Gardens", 280],
           30:["Action", "Go To Jail"],
           31:["Property", "Green", "Pacific Avenue", 300],
           32:["Property", "Green", "North Carolina Avenue", 300],
           33:["Action", "Community Chest"],
           34:["Property", "Green", "Pennsylvania Avenue", 320],
           35:["Property", "Railroad", "Shortline", 200],
           36:["Action", "Chance"],
           37:["Property", "DarkBlue", "Park Place", 350],
           38:["Action", "Luxury Tax"],
           39:["Property", "DarkBlue", "Boardwalk", 400],
           40:["Action", "Go"]
          }

    # Given a space ID Number, determine if a space is a property or an action space
    def parseSpace(self, spaceNumber):
        try:
            space = self.board[spaceNumber][0]
            if space == "Property":
                messageString = "Options: own, buy, auction, pay rent"
            elif space == "Action":
                messageString = self.actionRules(spaceNumber)
        except:
#        else:
            messageString = "Error: invalid board space!"
        return messageString

    # Given a space ID number, return a string of the action(s) to be performed
    def actionRules(self, spaceNumber):
        if spaceNumber == 40:
            actionString = "Gain 200"   # "Go"
        elif spaceNumber == 2 or spaceNumber == 17 or spaceNumber == 33:
            actionString = "Draw card: community chest"
        elif spaceNumber == 7 or spaceNumber == 22 or spaceNumber == 36:
            actionString = "Draw card: chance"
        elif spaceNumber == 10 or spaceNumber == 20:
            actionString = "Do nothing" # Visit Jail/Free parking
        elif spaceNumber == 4:
            actionString = "Pay 200"    # Income Tax
        elif spaceNumber == 38:
            actionString = "Pay 100"    # Luxury Tax
        elif spaceNumber == 30:
            actionString = "go to Jail" # Jail
        else:
            actionString = "Error: undefined action in rules.py/actionRules"

        return actionString

class TitleDeedCards(object):
        # Title Deed schema:
        #   {spaceName: [[base rent, set rent, 1 house rent... hotel rent], mortgage cost, build cost]
        #   Unmortgage is: 1.1 * mortgage_value, rounded up
    cards = {"Mediterranean Avenue": [1, [2, 4, 10, 30, 90, 160, 250], 30, 50],
           "Baltic Avenue": [3, [4, 8, 20, 60, 180, 320, 450], 30, 50],
           "Reading Railroad": [5, [25, 50, 100, 200], 100],                        
           "Oriental Avenue": [6, [6, 12, 30, 90, 270, 400, 550], 50, 50],         
           "Vermont Avenue": [8, [6, 12, 30, 90, 270, 400, 550], 50, 50], 
           "Connecticut Avenue": [9, [8, 16, 40, 100, 300, 450, 600], 60, 50],         
           "St Charles Place":[11, [10, 20, 50, 150, 450, 625, 750], 70, 100],
           "Electric Company":[12, [4, 10], 75],
           "States Avenue":[13, [10, 20, 50, 150, 450, 625, 750], 70, 100],
           "Virginia Avenue":[14, [12, 24, 60, 180, 500, 700, 900], 80, 100],
           "Pennsylvania Railroad":[15, [25, 50, 100, 200], 100],                        
           "St James Place":[16, [14, 28, 70, 200, 550, 750, 950], 90, 100],     
           "Tennessee Avenue":[18, [14, 28, 70, 200, 550, 750, 950], 90, 100],     
           "New York Avenue":[19, [16, 32, 80, 220, 600, 800, 1000], 100, 100],
           "Kentucky Avenue":[21, [18, 36, 90, 250, 700, 875, 1050], 110, 150],
           "Indiana Avenue":[23, [18, 36, 90, 250, 700, 875, 1050], 110, 150],
           "Illinois Avenue":[24, [20, 40, 100, 300, 750, 925, 1100], 110, 120],
           "B&O Railroad":[25, [25, 50, 100, 200], 100],
           "Atlantic Avenue":[26, [22, 44, 110, 330, 800, 975, 1150], 130, 150],
           "Ventnor Avenue":[27, [22, 44, 110, 330, 800, 975, 1150], 130, 150],
           "Water Works":[28, [4, 10], 75],
           "Marvin Gardens":[29, [24, 48, 120, 360, 850, 1025, 1200], 140, 150],
           "Pacific Avenue":[31, [26, 52, 130, 390, 900, 1100, 1275], 150, 200],
           "North Carolina Avenue":[32, [26, 52, 130, 390, 900, 1100, 1275], 150, 200], 
           "Pennsylvania Avenue":[34, [28, 56, 150, 450, 1000, 1200, 1400], 160, 200], 
           "Shortline":[35, [25, 50, 100, 200], 100],
           "Park Place":[37, [35, 70, 175, 500, 1100, 1300, 1500], 175, 200],
           "Boardwalk":[39, [50, 100, 200, 600, 1400, 1700, 2000], 200, 200]
          }

    # Maps an april tag ID from computer vision to the name of a card
    cv_match = {44: "Mediterranean Avenue",
            45: "Baltic Avenue",
            37: "Reading Railroad",
            41: "Oriental Avenue",
            42: "Vermont Avenue",
            43: "Connecticut Avenue",
            39: "St Charles Place",
            32: "Electric Company",
            40: "States Avenue",
            38: "Virginia Avenue",
            35: "Pennsylvania Railroad",
            54: "St James Place",
            55: "Tennessee Avenue",
            56: "New York Avenue",
            57: "Kentucky Avenue",
            58: "Indiana Avenue",
            59: "Illinois Avenue",
            34: "B&O Railroad",
            49: "Atlantic Avenue",
            50: "Ventnor Avenue",
            33: "Water Works",
            51: "Marvin Gardens",
            46: "Pacific Avenue",
            47: "North Carolina Avenue",
            48: "Pennsylvania Avenue",
            36: "Shortline",
            52: "Park Place",
            53: "Boardwalk"}


          
#     cards = {44"Mediterranean Avenue": [1, [2, 4, 10, 30, 90, 160, 250], 30, 50],
#           45"Baltic Avenue": [3, [4, 8, 20, 60, 180, 320, 450], 30, 50],
#           37 "Reading Railroad": [5, [25, 50, 100, 200], 100],                        
#           41"Oriental Avenue": [6, [6, 12, 30, 90, 270, 400, 550], 50, 50],         
#           42"Vermont Avenue": [8, [6, 12, 30, 90, 270, 400, 550], 50, 50], 
#           43"Connecticut Avenue": [9, [8, 16, 40, 100, 300, 450, 600], 60, 50],         
#           39"St Charles Place":[11, [10, 20, 50, 150, 450, 625, 750], 70, 100],
#           32"Electric Company":[12, [4, 10], 75],                                    
#           40"States Avenue":[13, [10, 20, 50, 150, 450, 625, 750], 70, 100],
#           38"Virginia Avenue":[14, [12, 24, 60, 180, 500, 700, 900], 80, 100],
#           35"Pennsylvania Railroad":[15, [25, 50, 100, 200], 100],                        
#           54"St James Place":[16, [14, 28, 70, 200, 550, 750, 950], 90, 100],     
#           55"Tennessee Avenue":[18, [14, 28, 70, 200, 550, 750, 950], 90, 100],     
#           56"New York Avenue":[19, [16, 32, 80, 220, 600, 800, 1000], 100, 100],
#           57"Kentucky Avenue":[21, [18, 36, 90, 250, 700, 875, 1050], 110, 150],
#           58"Indiana Avenue":[23, [18, 36, 90, 250, 700, 875, 1050], 110, 150],
#           59"Illinois Avenue":[24, [20, 40, 100, 300, 750, 925, 1100], 110, 120],
#           34"B&O Railroad":[25, [25, 50, 100, 200], 100],
#           49"Atlantic Avenue":[26, [22, 44, 110, 330, 800, 975, 1150], 130, 150],
#           50"Ventnor Avenue":[27, [22, 44, 110, 330, 800, 975, 1150], 130, 150],
#           33"Water Works":[28, [4, 10], 75],
#           51"Marvin Gardens":[29, [24, 48, 120, 360, 850, 1025, 1200], 140, 150],
#           46"Pacific Avenue":[31, [26, 52, 130, 390, 900, 1100, 1275], 150, 200],
#           47"North Carolina Avenue":[32, [26, 52, 130, 390, 900, 1100, 1275], 150, 200], 
#           48"Pennsylvania Avenue":[34, [28, 56, 150, 450, 1000, 1200, 1400], 160, 200], 
#           36"Shortline":[35, [25, 50, 100, 200], 100],
#           52"Park Place":[37, [35, 70, 175, 500, 1100, 1300, 1500], 175, 200],
#           53"Boardwalk":[39, [50, 100, 200, 600, 1400, 1700, 2000], 200, 200]
#          }


     # Return the rent of a space based on presence of a set and number of buildings
     # TODO: implement rent mechanics for utilites
    def rentLookup(self, space, isSet = False, numHouses = 0, numHotel = 0, isMortgaged = False):
         try:
            rentList = self.cards[space][1]    
         except:
             return -1 # invalid space

         if isSet == True:
             return rentList[1]
         elif numHouses > 0:
             return rentList[1+numHouses]
         elif numHotel == 1:
             return rentList[6]
         elif isMortgaged == True:
             return 0   # Mortgaged properties do not provide rent
         else:
             return rentList[0]

     # get the cost of building a house or hotel. Does not imply that said buildings are available
    def getBuildCost(self, space):
         return self.cards[space][3]

     # get the cash value of mortgaging a property
    def mortgageProperty(self, space):
         return self.cards[space][2]
# TODO
# Jacob Boe: This functions wasn't working when I tried it (can't use ceil on list)

    def unmortgageProperty(self, space):
         cost = ceil(self.cards[space][2] * 1.1) # round up to next integer
         return cost
     
    def getSquare(self, space):
       return self.cards[space][0]

# This class handles the mechanics of building; it will only be called if the player has met financial conditions
class Buildings(object):
    # Quantity of houses and hotelsi in game. Cannot build if all buildings are allocated
    house_count = 34
    hotel_count = 13

    # numHouses: number of houses on the property to be built on
    # lowest_set_house_count: all properties in set must be within 1 house of each other
    # mortgage: bool, checks if any properties in the set are mortgaged
    def buildHouse(self, num_houses, lowest_set_house_count, mortgage):
        if mortgage is True:
            return "error: mortgaged properties in set" 
        elif num_houses > 4:
            return "error: numHouses > 4" # Attempted to build a 5th house
        elif num_houses > (lowest_set_house_count + 1):
            return "error: numHouses not equal" # Properties in set do not have an equal number of houses
        elif num_houses <= 0:
            return "error: houseCount = 0"  # No houses remaining in supply

        num_houses = num_houses - 1
        return "house"  
        
    def buildHotel(self, numHouses, hotelCount, mortgage):
        if mortgage is True:
            return "error: mortgaged properties in set"
        elif numHouses < 4:
            return "error: numHouses < 4" # must have 4 houses before a hotel can be built
        elif hotelCount <= 0:
            return "error: hotelCount = 0" # No hotel remaining in supply

        hotelCount = hotelCount - 1
        numHouses = numHouses + 4   # houses must be return to supply!
        return "hotel; houses -4"

class ChanceCommunityCards(object):
    # Card Schema: 
    # {CardID number = [<actions to take>, <card nickname>]
    # All movement cards allow the player to gain $200 for passing Go
    chanceCards = {16:["Pay 15", "Speeding"],
            17:["Gain 50", "Dividends"],
            18: ["Move to next railroad (5, 15, 25, 35); buy or pay rent * 2", "Jump to railroad 1"],
            19: ["Each house: pay 25; Each hotel: pay 100", "General Repairs"],
            20: ["Move to 40", "Jump to Go"],
            21:["Move to current - 3", "Go back 3"],
            22: ["Move to 24", "Jump to Illnois"],
            23:["Pay 50 to player", "Chairman"],
            24: ["Move to 11", "Jump to St. Charles"],
            25:["Move to 10; Jail", "Go directly to Jail"], # Do not gain 200 for passing Go
            26: ["Move to next utility (12, 28); buy or pay new dice roll * 10", "Jump to utility"],
            27: ["Move to 39", "Jump to Boardwalk"],     # Player will never pass Go as a result of this
            28: ["Move to 5", "Jump to Reading R.R."],
            29:["Keep; use to leave jail", "Get-out-of-Jail-free"],
            30:["Gain 150", "Loan matures"],
            31: ["Move to next railroad (5, 15, 25, 35); buy or pay rent * 2", "Jump to railroad 2"]
            }
    
    communityCards = {0: ["Gain 10 from player", "Block party"],
            1:["Pay 50", "Animal shelter"],
            2: ["Gain 25", "Bake sale"],
            3:["Move to 10; Jail", "Go directly to Jail"], # Do not gain 200 for passing Go
            4: ["Pay 100", "Car wash"],
            5:["Keep; use to leave jail", "Get-out-of-Jail-free"],
            6: ["Gain 100", "Children's hospital"],
            7: ["Gain 50", "Clean up"],
            8: ["Each house: pay 40; Each hotel: pay 115", "Home improvement"],
            9: ["Gain 20", "Neighbor lunch"],
            10: ["Gain 10", "Blood drive"],
            11:["Pay 50", "Buy cookies"],
            12:["Gain 100", "Neighbor stories"],
            13:["Gain 100", "Playground"],
            14:["Gain 200", "Storm cleanup"],
            15: ["Move to 40", "Jump to Go"]
            }
   
    def parseCard(self, card_ID, card_type):
        if card_type == "community":
            return 


# Message Topic: Turn information
# Contents:
# String

# This will be expanded later
# To create this message type:
# https://wiki.ros.org/ROS/Tutorials/CreatingMsgAndSrv
# Substitute "num" for "Turn information"




#class playerTurn():
# Parts of this code is adapted from https://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29
def playerTurn():
    doublesCount = 0    # Track the number of doubles rolled
#def takeTurn():
     # This is the structure of a turn:

    # Roll dice
    # Move piece
    # Apply rules of space

    # Initialization
    pub = rospy.Publisher('TurnInfo', String, queue_size = 10) # Create publisher for topic TurnInfo
    
    rate = rospy.Rate(10)               # Send messages every 10 hz
    board = BoardSpaces()
    properties = TitleDeedCards()


    """ 
    # Input testing:
    spac = input("Enter a number:\n")
    numH = input("Enter the number of houses (can be 0):\n")
    numHotel = input("Is there a hotel?\n")


    print(board.parseSpace(spac))
    print("Rent is:")
    print(properties.rentLookup(spac, False, numH, numHotel))
    #print(properties.getBuildCost(spac))
    #print(properties.mortgageProperty(spac))
    """
    #gameSetup()
    #rospy.sleep(1)
    
    
    """while not rospy.is_shutdown():
        #rospy.sleep(2)

        # Core loop- Taking a turn
        for i in range(1,3):
            #result = rollDice()
            turnMessage = "Roll dice"
            pub.publish(turnMessage)
            rate.sleep()
#            if evaluateDice(result):
#                #print("I rolled {0}\n".format(result))
#                #print("I am taking my turn\n")
#                turnMessage = ("Move " + str(result))
#                if result[0] != result[1]:
#                    
#                    print("end of turn\n")
#                    # No double: end turn. Otherwise, take another turn
#                    break
#            
#            else:
#                print("Invalid dice roll!\n")
#
#                        


            print("I rolled doubles, I am taking another turn\n\n")
                # Doubles detected
            rospy.sleep(1)
                #doublesCount += 1
                #if doublesCount == 3:
                #    print("Go to Jail!")"""
    



    # This is the structure of a turn

    # Roll dice
    # Move piece
    # Apply rules of space
# End playerTurn()

def autoRollDice():
   values = []
   values.append(random.randrange(1,6))   
   values.append(random.randrange(1,6))   
   return tuple(values) 
   
def diceTotal(values):
    total = values[0] + values[1]
    return total

# Send the command to roll the dice to the motion planner
def rollDice():
    #rospy.init_node('rulesNode')       # Create ROS Node for pubsub interfacing
    diceMovePub = rospy.Publisher('diceRoll', Int16, queue_size=10)
    rospy.sleep(2.0)
#    values = []
    #total = 0
    """values.append(random.randrange(1,6))   
    values.append(random.randrange(1,6))   
    return tuple(values)"""
    
    msg = 0 # "0" means to roll the dice
    diceMovePub.publish(msg)
    print("My name is Rules and I'm publishing dice commands!\n")
    #rospy.spin()

def pullCard():
    diceMovePub = rospy.Publisher('diceRoll', Int16, queue_size=10)
    rospy.sleep(2.0)
    
    msg = 13 # "0" means to roll the dice
    diceMovePub.publish(msg) 

def donePullCard():
    diceMovePub = rospy.Publisher('diceRoll', Int16, queue_size=10)
    rospy.sleep(2.0)
    
    msg = 14 # "0" means to roll the dice
    diceMovePub.publish(msg)  
def publishDice(diceVal):
    diceMovePub = rospy.Publisher('diceRoll', Int16, queue_size=10)
    diceMovePub.publish(diceVal)
    rospy.sleep(2.0)

# Given a tuple containing dice roll values, verify that:
#   There are exactly two values
#   Those values are integers
#   Those values are between 1 and 6, inclusive
def evaluateDice(diceRoll):
    # Check that there are only two dice values submitted
    try: 
        if (len(diceRoll) != 2):
            return False
    except:
        return False

    dieOne = diceRoll[0]
    dieTwo = diceRoll[1]

    # Confirm that dice results are integers
    if not isinstance(dieOne, int) or not isinstance(dieTwo, int):
        return False

    # Confirm that dice results are within legal ranges
    if dieOne >= 1 and dieOne <= 6 and dieTwo >= 1 and dieTwo <= 6:
        return True

    return False

#class Money:
#    def PayMoney():


#def gainMoney():



#def main():
#    rospy.init_node('rules')
#    
#    # Wait for the AI to signal that it is ready to begin playing
#    # rospy.wait_for_message("Begin game", empty)
#
#    gameSetup() # Init the game state
#    rospy.sleep(1)
#
#    while not rospy.is_shutdown():
#            result = rollDice()
            

if __name__ == '__main__':
    #try:
    rospy.spin()
    #playerTurn()
    #except rospy.ROSInterruptException:
        #print("Error while instantiating playerTurn in rules.py!\n")"""
