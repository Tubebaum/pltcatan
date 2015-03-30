# -*- coding: utf-8 -*-
from enum import Enum


class Direction(Enum):

    def __str__(self):
        return '{0}'.format(self.value)

    def __getitem__(self, index):
        return self.value[index]

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        return iter(self.value)

    def __eq__(self, other):

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

