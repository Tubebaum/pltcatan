#!/usr/bin/env python
# -*- coding: utf-8 -*-

from game_data import Game
from config import config
import cmd

#Python2/3 compatibility
try:
    input = raw_input
except NameError:
    pass

#Some parsing utils
def getPlayerNames():
    players = []
    numPlayers = int(inputDef('Nplayers', '3'))
    for i in range(numPlayers):
        playerName = inputDef('Player ' + str(i + 1), 'p' + str(i + 1))
        players.append(playerName)
    return players

def inputDef(msg, default):
    result = input(msg + ' [' + default + ']: ')
    if (result == ''):
        return default
    return result

class TurnCmd(cmd.Cmd):
    def __init__(self, gameLoop, playerIndex):
        cmd.Cmd.__init__(self)
        self.prompt = gameLoop.players[playerIndex] + ': '
        self.gameLoop = gameLoop
        self.playerIndex = playerIndex

    def do_trade(self, line):
        print('Trade not implemented.')

    def do_build(self, line):
        print('Building not implemented.')

    def do_playcard(self, line):
        print('Development cards not implemented.')

    def do_print(self, line):
        print('This should print the board state.')
        for tile in self.gameLoop.game.tiles():
            print('Tile {0:2d}: {1:2d}'.format(tile.idNumber, 0))

    def do_end(self, line):
        print('Ended turn')
        return True

class GameLoop(object):
    def start(self):
        self.players = getPlayerNames()
        print('Generating board...')
        self.game = Game(len(self.players))
        self.game.generateBoard()
        print('Placing initial settlements...')
        self.initialSettlements()
        self.loopTurns()

    def initialSettlements(self):
        return

    def loopTurns(self):
        while True:
            for playerIndex in range(len(self.players)):
                print(self.players[playerIndex] + "'s turn")
                diced = config['dicer']()
                print('Diced value: ' + str(diced))
                TurnCmd(self, playerIndex).cmdloop()

if __name__ == '__main__':
    try:
        GameLoop().start()
    except KeyboardInterrupt:
        print u'\n(╯°□°）╯︵ ┻━┻)'
