from .board.game_board import GameBoard
from .dice.dice import Dice
from .input_manager import InputManager


class Game(object):
    def __init__(self):
        self.board = GameBoard(3)
        self.dice = Dice()
        self.players = InputManager.get_player_names()

    def start(self):
        self.loop_turns()


    def loop_turns(self):
        while True:
            for player_index in range(len(self.players)):
                print(self.players[player_index] + "'s turn")
                diced = self.dice.throw()
                print('Diced value: ' + str(diced))
                InputManager(self, player_index).cmdloop()
