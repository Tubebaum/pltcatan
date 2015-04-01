# -*- coding: utf-8 -*-
import random
import math
from ..lib.utils import Utils
from .hex_board import HexBoard
from ..tile.game_tile import GameTile
from ..resource_type import ResourceType
from ..calamity.calamity import Calamity


class GameBoard(HexBoard):
    """A Settlers of Catan playing board.

    Args:
        radius (int): See HexBoard.
    """

    def __init__(self, radius):

        super(GameBoard, self).__init__(radius, GameTile)

        # We have tiles, but they currently have no value and are all FALLOW.
        # Here we assign resource types and chit values.
        self.assign_tile_resources()
        self.assign_tile_chit_values()

    def assign_tile_resources(self, assignment_func=None):
        """Assign resource types to this board's tiles.

        Args:
            assignment_func (func): Resources will assigned according to this
              function. If not provided, will default to
              self._default_assign_tile_resources()

        Returns:
            None.
        """

        if assignment_func is None:
            self._default_assign_tile_resources()
        else:
            assignment_func()

    def _default_assign_tile_resources(self):
        """Distributes non-fallow resource types across the board evenly.

        Specifically, assigns one ResourceType.FALLOW tile, then splits the
        resource types of the remaining tiles evenly.

        Returns:
            None.
        """

        # Get a randomized list of the tiles of this board.
        tiles = list(self.iter_tiles())
        random.shuffle(tiles)

        resource_type_count = len(ResourceType.get_arable_types())

        # We'll allocate one fallow tile so divide arable resources among
        # total number of tiles - 1.
        per_resource_count = (len(tiles) - 1) / float(resource_type_count)

        # Say that we find that we need to allocate 3.6 tiles per resource.
        # Clearly we can only allocate whole number tiles. So we take the
        # difference between what we calculated and its floor (e.g. .6),
        # and multiply it by the number of tiles to get the number of
        # leftover tiles that need to be assigned.
        leftover_count = int((per_resource_count - int(per_resource_count)) *
                             resource_type_count)

        per_resource_count = int(per_resource_count)

        # Get a list containing resource_type_count occurrences of each
        # resource_type.
        resources = Utils.flatten(map(
            lambda resource: [resource] * per_resource_count,
            ResourceType.get_arable_types()
        ))

        # We then allocate leftover tiles according to some priority. In a
        # base Settlers of Catan game, this priority manifests as having only
        # 3 brick and ore tiles, by 4 lumber, wool, and wheat tiles.
        while leftover_count:
            resources.append(
                ResourceType.get_priority_arable_types()[leftover_count - 1])
            leftover_count -= 1

        # Add a single occurrence of ResourceType.FALLOW.
        resources.append(ResourceType.FALLOW)

        # Assign the resource types to the shuffled tiles.
        for tile, resource_type in zip(tiles, resources):
            tile.resource_type = resource_type

    def _randomly_assign_tile_resources(self):
        """Randomly assign resource types to this board's tiles.

        Note that this randomly draws from all ResourceType's, i.e. including
        ResourceType.FALLOW.

        Returns:
            None.
        """

        for tile in self.iter_tiles():
            tile.resource_type = ResourceType.random()

    def assign_tile_chit_values(self, assignment_func=None):
        """Assign chit values to this board's tiles.

        Args:
            assignment_func (func): Chit values will assigned according to this
              function. If not provided, will default to
              self._default_assign_tile_chit_values()

        Returns:
            None.
        """

        if assignment_func is None:
            self._default_assign_tile_chit_values()
        else:
            assignment_func()

    def _randomly_assign_tile_chit_values(self, start=2, end=12,
                                          exclude=Calamity.DEFAULT_ROLL_VALUES):
        """Randomly assign chit values to this board's tiles.

        Args:
            start (int): The set of possible chit values from which values to
              assign will be randomly drawn is defined by the range defined by
              start and end.

            end (int): See above.

            exclude (list): A list of values that lie in the range given by
              start and end that should not be included in the set of possible
              chit values.

        Returns:
            None
        """

        chit_values = frozenset(range(start, end + 1)).intersection(exclude)

        for chit_value, tile in zip(chit_values, self.iter_tiles()):
            tile.chit_value = chit_value

    def _default_assign_tile_chit_values(self, start=2, end=12,
                                         exclude=Calamity.DEFAULT_ROLL_VALUES):
        """Assign chit values in a manner similar to that of the original game.

        Specifically, find out how many times each value would occur if we
        were to distribute them over the board's non-fallow tiles evenly,
        except for the highest and lowest values (presumably the least likely
        to occur), which should only appear on the board half as often.

        Args:
            start (int): Together with end, defines the range of possible
              chit values.

            end (int): See above.

            exclude (list): A list of values that lie in the range defined by
              start and end that should not be included in the set of possible
              chit values.

        Returns:
            None.

        TODO: Consider storing self.tile_count instead of using the length
              of the iterator. For now, however, performance not an issue.
        """

        chit_values = filter(
            lambda value: value not in exclude, range(start, end + 1)
        )

        min_chit_value = chit_values[0]
        max_chit_value = chit_values[-1]

        # We only want to consider arable tiles.
        arable_tiles = list(self.iter_arable_tiles())
        tile_count = len(arable_tiles)

        # Since the lowest and highest chit values will occur half as
        # frequently, we act as if we were only had len(chit_values) - 1 values.
        per_value_count = tile_count / (len(chit_values) - 1)

        # We want the highest and lowest value chits to appear half as often.
        def get_value_occurrence_count(value):
            if value == min_chit_value or value == max_chit_value:
                return per_value_count / 2
            else:
                return per_value_count

        # Get a list of all the chit values we will place e.g. if we expect
        # to place 5 chits of value 3, then 3 should occur 5 times in the list.
        chit_values_to_assign = Utils.flatten(map(
            lambda value: [value] * get_value_occurrence_count(value),
            chit_values
        ))

        # Assign chit values to arable tiles only.
        for tile, chit_value_to_assign in zip(arable_tiles,
                                              chit_values_to_assign):
            tile.chit_value = chit_value_to_assign

    def iter_arable_tiles(self):
        """Iterate over this board's non-fallow i.e. arable tiles."""

        for tile in self.iter_tiles():
            if tile.resource_type != ResourceType.FALLOW:
                yield tile





