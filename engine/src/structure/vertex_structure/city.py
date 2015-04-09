# -*- coding: utf-8 -*-
from engine.src.structure.upgrade_structure import UpgradeStructure
from engine.src.structure.vertex_structure.settlement import Settlement
from engine.src.vertex import Vertex
from engine.src.resource_type import ResourceType


class City(UpgradeStructure, Vertex):
    """Represents a city from the Settlers of Catan game.

    Attributes:
        owning_player (Player): Player who built this city and for whom this
          city yields resources.

        base_structure_cls (class): Class of structure this City upgrades.

    Args:
        owning_player (Player): See above.
    """
    
    BASE_YIELD = 2
    
    def __init__(self, owning_player):
        
        self.owning_player = owning_player
        self.base_structure_cls = Settlement

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
