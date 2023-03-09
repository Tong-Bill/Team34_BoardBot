#!/usr/bin/env python

import unittest
from rules import evaluateDice

"""
Author: Adam Hurd

To run:
$ python -m unittest testdice


These tests are based on the Python unit test library found here:

https://docs.python.org/3/library/unittest.html
"""

class TestEvaluateDice(unittest.TestCase):
    def test_notInts(self):
        tuple1 = (1.0, 4.0)
        tuple2 = (0.22, 9.999)
        tuple3 = (1, 5)
        tuple4 = (4, 4)
        self.assertFalse(evaluateDice(tuple1))
        self.assertFalse(evaluateDice(tuple2))
        self.assertTrue(evaluateDice(tuple3))
        self.assertTrue(evaluateDice(tuple4))

    def test_tooManyDice(self):
        tuple5 = ()
        tuple6 = (1)
        tuple7 = (1, 5, 4)
        tuple8 = (1, 5)
        self.assertFalse(evaluateDice(tuple5))
        self.assertFalse(evaluateDice(tuple6))
        self.assertFalse(evaluateDice(tuple7))
        self.assertTrue(evaluateDice(tuple8))

    def test_notD6(self):
        tuple9 = (0, 5)
        tuple10 = (12, 8)
        tuple11 = (1, 20)
        tuple12 = (3, 2)
        self.assertFalse(evaluateDice(tuple9))
        self.assertFalse(evaluateDice(tuple10))
        self.assertFalse(evaluateDice(tuple11))
        self.assertTrue(evaluateDice(tuple12))


if __name__ == '__main__':
    TestEvaluateDice()
