# -*- coding: utf-8 -*-
from engine.src.edge.structure.structure import Structure
from engine.src.resource_type import ResourceType


class City(Structure):
    """Represents a city from the Settlers of Catan game.

    Args:
        owning_player (Player): The player who built this city.
    """
    
    BASE_YIELD = 2
    
    def __init__(self, owning_player):
        
        self.owning_player = owning_player

    def __str__(self):
        return 'City of {0}\n'.format(self.owning_player.name)

    @classmethod
    def base_yield(cls):
        """Determines how many resources a city generates."""
        return cls.BASE_YIELD

    @classmethod
    def cost(cls):
        """Get the resource cost of a city."""
        return (ResourceType.ORE, 3), (ResourceType.GRAIN, 2)
