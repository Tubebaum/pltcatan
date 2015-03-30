# -*- coding: utf-8 -*-
from enum import Enum


class ResourceType(Enum):
    """Defines the resource types available in a game of Settlers of Catan.

    Resources are produced by GameTile's of the given resource type, and are
    used to build/buy structures, cards, etc.
    """

    ORE = 'ore'
    GRAIN = 'grain'
    LUMBER = 'lumber'
    WOOL = 'wool'
    BRICK = 'brick'

    def __str__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other

    @classmethod
    def find_by_value(cls, value):
        for resource in cls:
            if value == resource:
                return resource