from game_data import Game
from config import config
import cmd



#Some parsing utils
def get_player_names():
    players = []
    nplayers = int(input_def("Nplayers", "3"))
    for i in range(nplayers):
        pname = input_def("Player "+str(i+1), "p"+str(i+1))
        players.append(pname)
    return players

def input_def(msg, default):
    result = input(msg + " [" + default + "]: ")
    if (result == ""):
        return default
    return result


class TurnCmd(cmd.Cmd):

        def __init__(self, game_loop, pidx):
            super(self.__class__,self).__init__()
            self.prompt = game_loop.players[pidx] + ": "
            self.gameloop = game_loop
            self.pidx = pidx

        def do_trade(self, line):
            print("Trade not implemented.")


        def do_build(self, line):
            print("Building not implemented.")

        def do_playcard(self, line):
            print("Development cards not implemented.")

        def do_print(self, line):
            print("This should print the board state.")
            for node in self.gameloop.game.nodes():
                print('Tile {0:2d}: {1:2d}'.format(node.n_id, 0))

        def do_end(self, line):
            print("Ended turn")
            return True


class GameLoop:

    def start(self):
        self.players = get_player_names()
        print("Generating board...")
        self.game = Game(len(self.players))
        self.game.gen_board()
        print("Placing initial settlements...")
        self.initial_settlements()
        self.loop_turns()


    def initial_settlements(self):
        return
    
    def loop_turns(self):
        while True:
            for pidx in range(len(self.players)):
                print(self.players[pidx] + "'s turn")
                diced = config["dicer"]()
                print("Diced value: " + str(diced))
                TurnCmd(self, pidx).cmdloop()


if __name__ == '__main__':
    GameLoop().start()