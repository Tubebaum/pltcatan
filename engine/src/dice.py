# -*- coding: utf-8 -*-
import random


class Dice(object):
    """ Represents a set of game dice.

    Args:
        dice_count (int): Number of dice in the game.
        
        range (list): List of possible dice values.
    """

    def __init__(self, dice_count=2, values=range(1, 7)):
        self.dice_count = dice_count
        self.values = values

    def roll(self):
        """ Rolls dice.

        Returns:
            int. Sum of dice face values after a random throw.
        """

        return sum(random.choice(self.values) for _ in range(self.dice_count))
