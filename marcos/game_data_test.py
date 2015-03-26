from game_data import Game
import unittest

class TestGameData(unittest.TestCase):
    def setUp(self):
        self.game = Game(2, 2)

    #tests BFS_gen and nodes iterator
    #iterator should return nodes with
    #ids in order
    def testGenerator(self):
        self.game.generateBoard()
        ids = [tile.idNumber for tile in self.game.tiles()]
        self.assertEqual(ids, list(range(19)))

if __name__ == '__main__':
    unittest.main()
