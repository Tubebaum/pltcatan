from game_data import Game
import cmd


#Some parsing utils
def get_player_names():
    players = []
    nplayers = int(input("Nplayers: "))
    for i in range(nplayers):
        pname = input("p"+str(i+1) + ": ")
        players.append(pname)
    return players


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

        #I'm thinking of this to print the current
        #board situation
        def do_print(self, line):
            print("This should print the board state.")

        def do_end(self, line):
            print("Ended turn")
            return True
        # def run_turn(self, pdix):
        #     diced = self.roll_dice()
        #     print "Dice roll: " + str(diced) + "\n"

        #     print "Trading... not implemented\n"

        #     print "Building...\n"

        #     print "Playing card... not implemented\n"


class GameLoop:

    def start(self):
        self.players = get_player_names()
        print("Generating board...")
        self.game = Game(len(self.players))
        self.game.gen_board()
        print("Placing initial settlements...")
        self.initial_settlements()
        self.loop_turns()
        # print self.game.count_nodes()


    def initial_settlements(self):
        return
    
    def loop_turns(self):
        while True:
            for pidx in range(len(self.players)):
                print(self.players[pidx] + "'s turn")
                # self.run_turn(pidx)
                TurnCmd(self, pidx).cmdloop()


    def roll_dice(self):
        import random
        return random.randint(0,9)


if __name__ == '__main__':
    GameLoop().start()