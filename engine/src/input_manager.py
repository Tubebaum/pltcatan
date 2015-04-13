import cmd
from engine.src.config import Config
from engine.src.direction.vertex_direction import VertexDirection
from engine.src.direction.edge_direction import EdgeDirection
from engine.src.direction.edge_vertex_mapping import EdgeVertexMapping
from engine.src.resource_type import ResourceType


class InputManager(cmd.Cmd):
    """Class managing input for a given player's turn. See docs for cmd.Cmd.

    Args:
        game (Game): The game being played.
        player (Player): Current player.

    """
    def __init__(self, game, player):

        cmd.Cmd.__init__(self)

        self.game = game
        self.player = player
        self.prompt = '> {0}: '.format(self.player.name)

        self.has_rolled = False
        self.has_played_card = False

    def default(self, line):
        """Print menu of commands when unrecognized command given."""

        print 'Unrecognized command <{0}> given.'.format(line)
        print 'Please try one of the following commands:\n{0}'.format(
            InputManager.list_cmds())

    def preloop(self):
        """Announce start of player turn."""

        print "{0}'s turn: ".format(self.player.name)

    def postloop(self):
        """Announce end of player turn."""

        print "End of {0}'s turn.".format(self.player.name)

    def do_roll(self, line):
        """Roll the dice (and have game handle resulting roll value)."""

        self.game.roll_dice()
        self.has_rolled = True

    @staticmethod
    def announce_roll_value(roll_value):
        print 'Player rolled a {0}'.format(roll_value)

    def do_trade(self, line):

        # TODO: consider reusable wrapper function.
        if not self.has_rolled:
            print 'You must roll before you can trade.'
            return
        else:
            print 'Trade not implemented.'

    def do_build(self, line):

        if not self.has_rolled:
            print 'You must roll before you can trade.'
            return
        else:
            print 'Building not implemented.'

    def do_buy_card(self, line):

        if self.has_played_card:
            print 'You may only play one card per turn.'
        else:
            print 'Purchasing development cards not implemented.'

    def do_play_card(self, line):

        if self.has_played_card:
            print 'You may only play one card per turn.'
        else:
            print 'Development cards not implemented.'

    def do_print_board(self, line):
        for tile in self.game.board.iter_tiles():
            print('({0:2d}, {1:2d})'.format(tile.x, tile.y))

    def do_end(self, line):
        """End the player's turn and exit the command loop."""

        if not self.has_rolled:
            print 'You must roll before you can end your turn.'
        else:
            return True

    @staticmethod
    def list_cmds():
        # TODO: improve
        cmds = ['trade', 'build', 'play card', 'print board', 'help', 'end']
        display_cmds_str = ''

        for cmd in cmds:
            display_cmds_str += '\t{0}\n'.format(cmd)

        return display_cmds_str

    @staticmethod
    def input_default(msg, default=None, read_result=True):
        """Asks for user data using the format specified below.

        Returns:
            str. string entered by the user, or default if nothing was entered.
        """

        prompt = '> {0}'.format(msg)

        if default:
            prompt += " (or press enter to use default of {0}): ".format(default)

        if read_result:
            prompt += '\n< '
            result = raw_input(prompt)
            return result if result else default
        else:
            print prompt

    @staticmethod
    def get_player_names():
        """Prompts for and takes in player names.

        Returns:
            list. Of player name strings.
        """
        player_names = []
        num_players = 0

        while num_players <= 0:
            try:
                num_players = int(
                    InputManager.input_default('Enter number of players',
                                               Config.DEFAULT_PLAYER_COUNT))

                if num_players <= 0:
                    raise ValueError

            except ValueError:
                msg = 'Invalid number of players. Number must be an integer' + \
                    ' greater than zero.'
                InputManager.input_default(msg, None, False)

        # Shift range by 1 so prompts starting with player 1, not player 0
        for i in range(1, num_players + 1):
            msg = "Specify player {0}'s name".format(i)
            default = 'p{0}'.format(i)
            player_name = InputManager.input_default(msg, default)
            player_names.append(player_name)

        return player_names

    @staticmethod
    def prompt_tile_coordinates(game):

        x, y = None, None

        valid_coords = False

        while not valid_coords:
            x = int(InputManager.input_default(
                'Please specify a tile x coordinate:', None))

            y = int(InputManager.input_default(
                'Please specify a tile y coordinate:', None))

            valid_coords = game.board.valid_tile_coords(x, y)

            if not valid_coords:
                error_msg = "Invalid coordinates. Please try again."
                InputManager.input_default(error_msg, None, False)

        return x, y

    @staticmethod
    def prompt_select_enum_value(enum_cls, prompt_msg):

        enums = list(enum_cls)
        selected_enum = None

        while selected_enum not in enums:

            for index, enum in enumerate(enums):
                print '({0}) {1}'.format(index + 1, enum)

            index = int(InputManager.input_default(prompt_msg))

            try:
                selected_enum = enums[index - 1]
            except IndexError:
                print "Invalid number given. You must give a number " + \
                      "between 1 and {0}.".format(len(enums))

        return selected_enum

    @staticmethod
    def prompt_select_resource_type():

        msg = "Please enter the number (e.g. '1') of the resource type" + \
              "you would like to choose."

        return InputManager.prompt_select_enum_value(ResourceType, msg)

    @staticmethod
    def prompt_vertex_direction():

        msg = "Please enter the number (e.g. '1') of the direction " + \
              "from the center of the tile to the vertex you would " + \
              "like to place a structure on."

        return InputManager.prompt_select_enum_value(VertexDirection, msg)

    @staticmethod
    def prompt_edge_direction():

        msg = "Please enter the number (e.g. '1') of the direction " + \
              "from the center of the tile to the edge you would " + \
              "like to place a structure on."

        return InputManager.prompt_select_enum_value(EdgeDirection, msg)

    @staticmethod
    def prompt_vertex_placement(game):

        x, y = InputManager.prompt_tile_coordinates(game)

        vertex_dir = InputManager.prompt_vertex_direction()

        return x, y, vertex_dir

    @staticmethod
    def prompt_edge_placement(game):

        x, y = InputManager.prompt_tile_coordinates(game)

        edge_dir = InputManager.prompt_edge_direction()

        return x, y, edge_dir

    @staticmethod
    def announce_initial_structure_placement_stage():
        prompt = 'Beginning initial structure placement stage.'
        InputManager.input_default(prompt, None, False)

    @staticmethod
    def announce_player_turn(player):
        prompt = "Beginning {0}'s turn.".format(player.name)
        InputManager.input_default(prompt, None, False)

    @staticmethod
    def announce_structure_placement(player, structure_cls):
        prompt = "{0}, select where you would like to place your {1}".format(
            player.name, structure_cls.__name__.lower()
        )
        InputManager.input_default(prompt, None, False)

    @staticmethod
    def announce_development_card_played(player, development_card):
        prompt = "{0} played a development card: {1}".format(
            player.name, development_card.__class__)
        InputManager.input_default(prompt, None, False)

    @staticmethod
    def announce_resource_distributions(distributions):

        msg = 'Distributing resources.'
        InputManager.input_default(msg, None, False)

        for player in distributions:
            for resource_type in distributions[player]:
                count = distributions[player][resource_type]

                if count:
                    msg = '{0} received {1} {2} cards.'.format(
                        player.name, count, resource_type)
                    InputManager.input_default(msg, None, False)
