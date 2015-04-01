# -*- coding: utf-8 -*-
from engine.src.resource_type import ResourceType


class Player(object):

    def __init__(self, name):

        self.name = name

        # Create an empty resource hand
        self.resources = {}
        for arable_type in ResourceType.get_arable_types():
            self.resources[arable_type] = 0

    def add_resources(self, resource_type, count):
        """Add resources of the given type and count to this player's hand."""

        self.resources[resource_type] += count



