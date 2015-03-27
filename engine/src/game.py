from board import *

b = Board(2)

tile = b.get_tile_with_coord(0, 0)

print b.get_neighboring_tile(tile, Direction.NORTH_EAST)