#!/usr/bin/env python

"""
Author: Adam Hurd
Assignment: CS 426 Senior Project

This file contains rule logic for Monopoly. It is designed to be used with an AI module
that will make decisions based on the responses of the rules
"""

import rospy
import sys
import os
import random   # for random dice values
from std_msgs.msg import String

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

# end gameSetup






# Message Topic: Turn information
# Contents:
# String

# This will be expanded later
# To create this message type:
# https://wiki.ros.org/ROS/Tutorials/CreatingMsgAndSrv
# Substitute "num" for "Turn information"


#class playerTurn():
# Parts of this code is adapt from https://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29
def playerTurn():
    doublesCount = 0    # Track the number of doubles rolled
#def takeTurn():
    pub = rospy.Publisher('TurnInfo', String, queue_size = 10)
    rospy.init_node('playerTurn')
    rate = rospy.Rate(10) # Send messages every 10 hz

    gameSetup()
    rospy.sleep(1)

    while not rospy.is_shutdown():
        rospy.sleep(2)
        for i in range(1,3):
            result = rollDice()
            print("I rolled {0}\n".format(result))
            print("I am taking my turn\n")
            if result[0] != result[1]:
                print("end of turn\n")
                # No double: end turn. Otherwise, take another turn
                break
            print("I rolled doubles, I am taking another turn\n\n")
                # Doubles detected
            rospy.sleep(1)
                #doublesCount += 1
                #if doublesCount == 3:
                #    print("Go to Jail!")




    # This is the structure of a turn

    # Roll dice
    # Move piece
    # Apply rules of space


    # result = rollDice(iteration)

    # if result >= 2:
        # continue with turn
        
        # action, etc.

    # else:
    # go to jail
# Check for three doubles in a row
#    for i in range(1, 3):

# End playerTurn()


# Generate two random values between 1 and 6, representing a dice roll
def rollDice():
    values = []
    values.append(random.randrange(1,6))   
    values.append(random.randrange(1,6))   
    return tuple(values)



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
    try:
        playerTurn()
    except rospy.ROSInterruptException:
        print("Error while instantiating playerTurn(0 in rules.py!\n")
