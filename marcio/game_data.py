from Vector2 import Vector2

class Tile(object):
    idCount = 0

    def __init__(self):
        self.idNumber = Tile.idCount
        Tile.idCount += 1

directions = [Vector2(1, 0), Vector2(1, -1), Vector2(0, -1), Vector2(-1, 0),
        Vector2(-1, 1), Vector2(0, 1)]

def hexagRing(center, radius):
    cube = center + directions[0] * radius
    for i in range(6):
        for j in range(radius):
            yield cube
            cube = cube + directions[(i + 2) % 6]

def hexagSpiral(center, radius):
    yield center
    for r in range(1, radius + 1):
        for h in hexagRing(center, r):
            yield h

class Game(object):
    def __init__(self, numPlayers, boardSize=2):
        self.numPlayers = numPlayers
        self.player_resources = {}
        self.boardSize = boardSize
        self.dice = Dice()
        self.board = {}

    def generateBoard(self):
        self.board = {}
        for hexag in hexagSpiral(Vector2(0, 0), self.boardSize):
            self.board[hexag] = Tile()

    # Intended for testing
    def count_nodes(self):
        return len(list(self.nodes()))

    # Python generator returning each tile
    def tiles(self):
        for k in hexagSpiral(Vector2(0, 0), self.boardSize):
            yield self.board[k]
