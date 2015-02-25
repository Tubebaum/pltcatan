from game_data import Game


#Some parsing utils
def get_player_names():
    players = []
    nplayers = int(raw_input("Nplayers: "))
    for i in range(nplayers):
        pname = raw_input("p"+str(i+1) + ": ")
        players.append(pname)
    return players

class GameLoop:
        

    def start(self):
        self.players = get_player_names()
        print "Generating board..."
        self.game = Game(len(self.players))
        self.game.gen_board()
        print "Placing initial settlements..."
        self.initial_settlements()


    def initial_settlements(self):
        return
    
    def loop_turns():
        None

if __name__ == '__main__':
    GameLoop().start()