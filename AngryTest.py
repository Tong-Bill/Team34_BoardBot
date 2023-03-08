import unittest
from expressions import Angry

'''
Author: Bill Tong
Purpose: Unit test created to test that a dialogue returned from the Angry function is one of the preset strings from the appropriate list.

Note: This test was created based with the help of the following resource:
https://docs.python.org/3/library/unittest.html
'''

class TestDialogue(unittest.TestCase):
	def testAngry(self):
		angry_list = ["I can't believe my luck is so bad. This game is rigged!","That's it, I'm done playing with you. You always cheat and ruin the game for everyone else!","I can't believe how unfair this game is! It's like everything is going against me!","I don't even want to talk to you right now. You're making me so angry with your constant greed and manipulation."]		
		result = Angry()
		self.assertIn(result, angry_list)

if __name__== "__main__":
	unittest.main()


