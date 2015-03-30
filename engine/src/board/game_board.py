# -*- coding: utf-8 -*-
from .hex_board import HexBoard
from ..tile.game_tile import GameTile

class GameBoard(HexBoard):
    """A Settlers of Catan playing board.

    Args:
        radius (int): See HexBoard.
    """

    def __init__(self, radius):

        super(GameBoard, self).__init__(radius, GameTile)

