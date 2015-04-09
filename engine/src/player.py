# -*- coding: utf-8 -*-
from engine.src.trading.trading_entity import TradingEntity


class Player(TradingEntity):
    """A player in a game of Settlers of Catan.

    Attributes:
        resources (dict): See TradingEntity.

        name (str): This player's name.

    Args:
        name (str): Name to assign a new player.
    """

    def __init__(self, name):

        super(Player, self).__init__()

        self.name = name
        self.points = 0
        self.development_cards = []

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name



