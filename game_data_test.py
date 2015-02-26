from game_data import Game
import unittest

class TestGameData(unittest.TestCase):

    def setUp(self):
        self.game = Game(2, 3)

    #tests BFS_gen and nodes iterator
    #iterator should return nodes with
    #ids in order
    def test_gen_it(self):
        self.game.gen_board()
        ids = [node.n_id for node in self.game.nodes()]
        self.assertEqual(ids, list(range(19)))

if __name__ == '__main__':
    unittest.main()