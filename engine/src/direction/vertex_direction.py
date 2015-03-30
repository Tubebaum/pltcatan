# -*- coding: utf-8 -*-
from .direction import Direction


class VertexDirection(Direction):
    """The 6 directions of a hexagon's vertices using cubic coordinates.

    Each vertex direction is a direction we can follow from the center of a
    tile to one of its vertexes.

    If we consider the hexagon a cube, the values correspond to the cubic
    (x, y, z) coordinates of the various directions.

    See more on cubic coordinates here:
        http://www.redblobgames.com/grids/hexagons/#coordinates

    Note: Be wary of reordering the below; uses of the iterator in hex_board.py
          are sensitive to the ordering.
    """

    TOP = (1, 1, 0)
    TOP_RIGHT = (1, 0, 0)
    BOTTOM_RIGHT = (1, 0, 1)
    BOTTOM = (0, 0, 1)
    BOTTOM_LEFT = (0, 1, 1)
    TOP_LEFT = (0, 1, 0)

    def get_opposite_direction(self):
        coordinates = self.value

        def toggle(val):
            """Toggle val between 0 and 1."""
            return int(not bool(val))

        x = toggle(coordinates[0])
        y = toggle(coordinates[1])
        z = toggle(coordinates[2])

        return x, y, z

    @classmethod
    def pairs(cls):
        return (
            (cls.TOP, cls.TOP_RIGHT),
            (cls.TOP_RIGHT, cls.BOTTOM_RIGHT),
            (cls.BOTTOM_RIGHT, cls.BOTTOM),
            (cls.BOTTOM, cls.BOTTOM_LEFT),
            (cls.BOTTOM_LEFT, cls.TOP_LEFT),
            (cls.TOP_LEFT, cls.TOP)
        )