from collections import deque
from config import config
from Vector2 import Vector2


class Tile(object):
	n_id_count = 0

	def __init__(self):
		self.n_id = Tile.n_id_count
		Tile.n_id_count += 1


directions = [
   Vector2(+1,  0), Vector2(+1, -1), Vector2( 0, -1),
   Vector2(-1,  0), Vector2(-1, +1), Vector2( 0, +1)
]

def hexag_ring(center, radius):
    cube = center + directions[0]*radius
    for i in range(6):
        for j in range(radius):
            yield cube
            cube = cube + directions[(i+2)%6]

def hexag_spiral(center, radius):
    yield center
    for r in range(1, radius+1):
        for h in hexag_ring(center, r):
            yield h

class Game(object):

	def __init__(self, nplayers, boardsize=2):
		self.nplayers = nplayers
		self.player_resources = {}
		self.boardsize = boardsize


	def gen_board(self):
		self.board = {}
		for hexag in hexag_spiral(Vector2(0,0), self.boardsize):
			self.board[hexag] = Tile()

	# Intended for testing
	def count_nodes(self):
		return len(list(self.nodes()))

	# Python generator returning each tile
	def tiles(self):
		for k in hexag_spiral(Vector2(0,0), self.boardsize):
			yield self.board[k]
