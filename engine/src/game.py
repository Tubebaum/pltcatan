from .board.game_board import GameBoard
from .dice.dice import Dice
import cmd


class Game(object):
    def __init__(self):
        self.board = GameBoard(3)
        self.dice = Dice()
        self.players = TurnCmd.get_player_names()

    def start(self):
        self.loop_turns()


    def loop_turns(self):
        while True:
            for player_index in range(len(self.players)):
                print(self.players[player_index] + "'s turn")
                diced = self.dice.throw()
                print('Diced value: ' + str(diced))
                TurnCmd(self, player_index).cmdloop()


class TurnCmd(cmd.Cmd):
    def __init__(self, game, playerIndex):
        cmd.Cmd.__init__(self)
        self.prompt = game.players[playerIndex] + ': '
        self.game = game
        self.playerIndex = playerIndex

    def do_trade(self, line):
        print('Trade not implemented.')

    def do_build(self, line):
        print('Building not implemented.')

    def do_playcard(self, line):
        print('Development cards not implemented.')

    def do_print(self, line):
        print('This should print the board state.')
        for tile in self.game.board.iter_tiles():
            print('({0:2d}, {1:2d})'.format(tile.x, tile.y))
            # print('Tile {0:2d}: {1:2d}'.format(tile.idNumber, 0))

    def do_end(self, line):
        print('Ended turn')
        return True

    @staticmethod
    def input_default(msg, default):
        result = raw_input(msg + ' [' + default + ']: ')
        if (result == ''):
            return default
        return result

    @staticmethod
    def get_player_names():
        players = []
        numPlayers = int(TurnCmd.input_default('Nplayers', '3'))
        for i in range(numPlayers):
            playerName = TurnCmd.input_default('Player ' + str(i + 1), 'p' + str(i + 1))
            players.append(playerName)
        return players
