import cmd


class InputManager(cmd.Cmd):
    """Class managing input for a given player's turn. See docs for cmd.Cmd.

    Args:
        game (Game): The game being played.
        player_index(int): Index of the current player.

    """
    def __init__(self, game, player_index):
        cmd.Cmd.__init__(self)
        self.prompt = game.players[player_index] + ': '
        self.game = game
        self.player_index = player_index

    def do_trade(self, line):
        print('Trade not implemented.')

    def do_build(self, line):
        print('Building not implemented.')

    def do_play_card(self, line):
        print('Development cards not implemented.')

    def do_print(self, line):
        for tile in self.game.board.iter_tiles():
            print('({0:2d}, {1:2d})'.format(tile.x, tile.y))

    def do_end(self, line):
        print('Ended turn')
        return True

    @staticmethod
    def input_default(msg, default):
        """
        Asks for user data using the format "msg [default]:"

        Returns:
            str. string entered by the user, or default if nothing was entered.
        """
        result = raw_input(msg + ' [' + default + ']: ')
        if result == '':
            return default
        return result

    @staticmethod
    def get_player_names():
        """
        Prompts the user for player names.

        Returns:
            list. Player names.
        """
        players = []
        num_players = int(InputManager.input_default('Nplayers', '3'))
        for i in range(num_players):
            player_name = InputManager.input_default('Player ' + str(i + 1), 'p' + str(i + 1))
            players.append(player_name)
        return players
