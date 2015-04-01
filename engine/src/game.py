from engine.src.dice.dice import Dice
from engine.src.input_manager import InputManager
from engine.src.board.game_board import GameBoard


class Game(object):
    def __init__(self):
        self.board = GameBoard(GameBoard.DEFAULT_RADIUS)
        self.dice = Dice()
        #TODO: Move this to the player class
        self.players = InputManager.get_player_names()

    def start(self):
        self.game_loop()

    def game_loop(self):
        while True:
            for player_index in range(len(self.players)):
                print(self.players[player_index] + "'s turn")
                roll_value = self.dice.throw()
                self.board.distribute_resources_for_roll(roll_value)
                print('You rolled a ' + str(roll_value))
                InputManager(self, player_index).cmdloop()
