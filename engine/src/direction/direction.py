# -*- coding: utf-8 -*-
from enum import Enum


class Direction(Enum):
    """An abstract class that defines basic functions needed by direction enums.

    TODO: Enforce that this class is an abstract class by having
          its metaclass be ABCMeta. This seems to create some issues since
          Enum is not a regular class and comes from a backport.
    """

    def __str__(self):
        return '{0}: {1}'.format(self.name, self.value)

    def __getitem__(self, index):
        return self.value[index]

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        return iter(self.value)

    def __eq__(self, other):

        if not other:
            return False

        if not len(other) == len(self):
            return False

        for index, value in enumerate(self):
            if not value == other[index]:
                return False

        return True

    @classmethod
    def find_by_value(cls, value):
        for direction in cls:
            if value == direction:
                return direction

