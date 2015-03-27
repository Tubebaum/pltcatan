# -*- coding: utf-8 -*-

from tile import *


class Board(object):
    """A horizontal hextile board, such as that used in Settlers of Catan.

    Hextiles are referred to using axial coordinates.
        See http://devmag.org.za/2013/08/31/geometry-with-hex-coordinates/
        for more on axial hex coordinates.

    Attributes:
        radius (int): The number of tiles between the center tile and the edge
          of the board, including the center tile itself. Should be >= 1.

        tiles (dict): A dictionary of tiles, indexed using axial coordinates
        
    Args:
        radius (int): The number of tiles between the center tile and the edge
          of the board, including the center tile itself. Should be >= 1.

    TODO: This class currently assumes a board of hextiles but ideally should
          be generalized for differently shaped tiles.
    """

    def __init__(self, radius):

        # TODO: enforce positive integer radius
        self.radius = radius

        self.tiles = {}
        self._create_tiles(radius)

    def _create_tiles(self, radius):
        """Generates a dictionary of tiles, indexed by axial coordinates.

        We can consider a hextile board a series of concentric rings where the
        radius counts the number of concentric rings that compose the board.
        When adding tiles to the board, we add each such ring one at a time,
        starting from the innermost ring (i.e. the single center tile)
        that has ring_index 0 to the outermost ring (i.e. the ring consisting
        of tiles on the edge of the board) that has ring_index radius - 1.

        When filling in a ring, we start from the westernmost tile of that ring
        and continue around the ring in a clockwise fashion. We stop at the tile
        directly before the easternmost ring. We can do this because, every time
        we add a tile in the ring, we can add the tile mirror opposite it on
        the ring by simpling flipping the axial coordinates.
        
        Args:
            radius (int): the number of tiles between the center tile and the
              edge of the board, including the center tile itself.
              Should be >= 1. Can also be though of as the number of concentric
              rings on the board + 1.
        
        Returns:
            None (Modifies self.tiles)
        """

        self.tiles = {}

        # We'll go ahead and add the center tile.
        self._add_tile_with_coords(0, 0)

        for ring_index in range(radius):
            # We start adding tiles from the westernmost one.
            x = -1 * ring_index
            y = 0

            # First we scale the northwest side of the ring.
            # This is equivalent to moving along the y-axis of the board.
            while y != ring_index:
                self._add_tile_with_coords(x, y)
                # Add the mirror tile along the southeast side of the ring.
                self._add_tile_with_coords(y, x)
                y += 1

            # Then we scale the northern side of the ring.
            # This is equivalent to moving along the x-axis of the board.
            while x != 0:
                self._add_tile_with_coords(x, y)
                # Add the mirror tile along the south side of the ring.
                self._add_tile_with_coords(y, x)
                x += 1

            # Finally we scale the northeast side of the ring.
            # This is equivalent to moving along the z-axis of the board.
            while x != ring_index or y != 0:
                self._add_tile_with_coords(x, y)
                # Add mirror tile along the southwest side of the ring.
                self._add_tile_with_coords(y, x)
                x += 1
                y -= 1

        # print self.tiles

    def _add_tile_with_coords(self, x, y):
        """Add a tile to the board at the given axial coordinates."""

        if x not in self.tiles:
            self.tiles[x] = {}

        self.tiles[x][y] = Tile(x, y)

    def get_tile_with_coords(self, x, y):
        """Get the tile at the given coordinates, or None if no tile exists."""

        if x in self.tiles and y in self.tiles[x]:
            return self.tiles[x][y]

        return None

    def get_neighboring_tile(self, tile, edge_direction):
        """Get the tile neighboring the given tile in the given direction.

        Args:
            tile (tile.Tile): The tile for which we'd like to find the neighbor.

            direction (tile.EdgeDirection): hextiles have 6 edges and thus
              neighbors in 6 different directions.

        Returns:
            Tile. None if the tile has no valid neighbor in that direction.

        TODO: enforce that direction is actually in Direction
        """

        x = tile.x + edge_direction[0]
        y = tile.y + edge_direction[1]

        return self.get_tile_with_coords(x, y)



