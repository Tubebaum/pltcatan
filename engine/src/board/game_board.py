# -*- coding: utf-8 -*-
import random
from .hex_board import HexBoard
from ..tile.game_tile import GameTile
from ..resource_type import ResourceType


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
        """Assign resource types to this board's tiles."""

        if assignment_func is None:
            self._randomly_assign_tile_resources()
        else:
            assignment_func()

    def _default_assign_tile_resources(self):
        """Distributes non-fallow resource types across the board evenly.

        Specifically, assigns one ResourceType.FALLOW tile, then splits the
        resource types of the remaining tiles evenly.
        """

    #     # Get a randomized list of the tiles of this board.
    #     tiles = list(self.iter_tiles())
    #     random.shuffle(tiles)
    #
    #     resource_type_count = int( (len(tiles) - 1) / ResourceType.count() )
    #     resources =
    #
    #     while tiles:
    #         tile = tiles.pop()
    #
    #
    #
        pass

    def _randomly_assign_tile_resources(self):
        """Randomly assign resource types to this board's tiles."""

        for tile in self.iter_tiles():
            tile.resource_type = ResourceType.random()

    def assign_tile_chit_values(self, assignment_func=None):
        """Assign chit values to this board's tiles."""

        if assignment_func is None:
            self._default_assign_tile_chit_values()
        else:
            assignment_func()

    def _default_assign_tile_chit_values(self):
        pass

