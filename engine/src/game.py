from .board.game_board import GameBoard
from .dice.dice import Dice
from .input_manager import InputManager


class Game(object):
    def __init__(self):
        self.board = GameBoard(3)
        self.dice = Dice()
        self.players = InputManager.get_player_names()

    def start(self):
        self.game_loop()

    def game_loop(self):
        while True:
            for player_index in range(len(self.players)):
                print(self.players[player_index] + "'s turn")
                roll_value = self.dice.throw()
                #self.board.distribute_resources_for_roll(row_value)
                print('Diced value: ' + str(roll_value))
                InputManager(self, player_index).cmdloop()
