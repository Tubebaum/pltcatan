# -*- coding: utf-8 -*-
from enum import Enum


class PositionType(Enum):

    VERTEX = 'vertex'
    EDGE = 'edge'

    def __str__(self):
        return '{0}'.format(self.value)

    def __eq__(self, other):
        return self.value == other

    @classmethod
    def find_by_value(cls, value):
        """Find the PositionType of the given value."""

        for position in cls:
            if value == position:
                return position
