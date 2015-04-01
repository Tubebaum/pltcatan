# -*- coding: utf-8 -*-
import random
from enum import Enum


class ResourceType(Enum):
    """Defines the resource types available in a game of Settlers of Catan.

    Resources are produced by GameTile's of the given resource type, and are
    used to build/buy structures, cards, etc.
    """

    # Arable tiles are non-fallow tiles.
    GRAIN = 'grain'
    LUMBER = 'lumber'
    WOOL = 'wool'
    ORE = 'ore'
    BRICK = 'brick'

    FALLOW = None

    def __str__(self):
        return '{0}'.format(self.value)

    def __eq__(self, other):
        return self.value == other

    @classmethod
    def get_priority_arable_types(cls):

        return cls.GRAIN, cls.LUMBER, cls.WOOL, cls.ORE, cls.BRICK

    @classmethod
    def get_arable_types(cls):
        """Get a list of non-fallow ResourceTypes only."""

        arable_types = filter(
            lambda resource_type: resource_type != ResourceType.FALLOW,
            list(ResourceType)
        )

        return arable_types

    @classmethod
    def iter_arable_types(cls):
        """Returns a generator over non-fallow enum members."""

        for resource_type in ResourceType.get_arable_types():
            yield resource_type

    @classmethod
    def random_arable_type(cls):
        """Return a random non-fallow ResourceType."""

        arable_types = ResourceType.get_arable_types()
        random_index = random.randint(0, len(arable_types))

        return arable_types[random_index]

    @classmethod
    def find_by_value(cls, value):
        """Find the ResourceType of the given value."""

        for resource in cls:
            if value == resource:
                return resource