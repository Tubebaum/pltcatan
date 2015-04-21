# -*- coding: utf-8 -*-
from engine.src.trading.trading_entity import TradingEntity
from engine.src.exceptions import NotEnoughStructuresException


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

        self.development_cards = []

        self.points = 0
        self.hidden_points = 0

        self.knights = 0
        self.longest_road_length = 0

        # TODO: move to config
        # TODO: programatically set these attributes
        self.remaining_road_count = 15
        self.remaining_settlement_count = 5
        self.remaining_city_count = 5

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name
    
    def get_total_points(self):
        return self.points + self.hidden_points

    def get_structure(self, structure_cls):
        """Get the given structure from the player's stock, if any remains.

        Every time a player builds a structure, we need to remove from their
        stock, e.g. remaining_road_count etc. This method generalizes this
        process of removal for all structures.

        Args:
            structure_cls (class): Class of structure to build.
        """

        cls_str = structure_cls.__name__.lower()
        relevant_property = 'remaining_{0}_count'.format(cls_str)

        structure_count = getattr(self, relevant_property)

        if structure_count > 0:
            setattr(self, relevant_property, structure_count - 1)
            return structure_cls(self)
        else:
            raise NotEnoughStructuresException(self, structure_cls)
