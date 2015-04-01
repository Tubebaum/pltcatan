# -*- coding: utf-8 -*-
import random
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

    FALLOW = None

    def __str__(self):
        return '{0}'.format(self.value)

    def __eq__(self, other):
        return self.value == other

    @classmethod
    def iter_non_fallow(cls):
        """Returns a generator over non-fallow enum members."""

        arable_types = ResourceType.__members__.items()[:-1]

        for resource_type in arable_types:
            yield resource_type

    @classmethod
    def count(cls):
        """Return number of non-fallow resources for this resource type."""
        return len(ResourceType.__members__.items()) - 1

    @classmethod
    def random(cls):
        """Return a random non-fallow ResourceType."""

        # Remove ResourceType.FALLOW from consideration.
        types = ResourceType.__members__.items()[:-1]
        random_index = random.randint(0, len(types) - 1)

        return types[random_index]

    @classmethod
    def find_by_value(cls, value):
        for resource in cls:
            if value == resource:
                return resource