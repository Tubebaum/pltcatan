# -*- coding: utf-8 -*-
import random


class Dice(object):
    """ Represents a set of game dice.

    Args:
            number (int): Number of dice in the game.
            range (list): List of possible dice values.
    """

    def __init__(self, number=2, values=range(1, 7)):
        self.number = 2
        self.values = values

    def throw(self):
        """
        Returns:
        int. Sum of dice face values after a random throw.
        """
        total = 0
        for _ in range(self.number):
            total += random.choice(self.values)

        return total