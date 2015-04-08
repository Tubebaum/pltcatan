# -*- coding: utf-8 -*-
from engine.src.edge.structure.structure import Structure
from engine.src.resource_type import ResourceType


class Settlement(Structure):
    """Represents a settlement from the Settlers of Catan game.

    Args:
        owning_player (Player): The player who built this settlement.
    """

    BASE_YIELD = 1

    def __init__(self, owning_player):

        self.owning_player = owning_player

    @classmethod
    def base_yield(cls):
        """Determines how many resources a settlement generates."""
        return cls.BASE_YIELD

    @classmethod
    def cost(cls):
        """Get the resource cost of a settlement."""
        return (ResourceType.LUMBER, 1), \
               (ResourceType.BRICK, 1), \
               (ResourceType.WOOL, 1), \
               (ResourceType.GRAIN, 1)

