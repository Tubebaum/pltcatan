from game_data import Game
import unittest

class TestGameData(unittest.TestCase):
    def setUp(self):
        self.game = Game(2, 2)

    #tests BFS_gen and nodes iterator
    #iterator should return nodes with
    #ids in order
    def test_gen_it(self):
        self.game.gen_board()
        ids = [tile.n_id for tile in self.game.tiles()]
        self.assertEqual(ids, list(range(19)))

if __name__ == '__main__':
    unittest.main()
