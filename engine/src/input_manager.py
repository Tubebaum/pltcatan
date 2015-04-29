import cmd
import sys

from engine.src.config.config import Config
from engine.src.direction.vertex_direction import VertexDirection
from engine.src.direction.edge_direction import EdgeDirection
from engine.src.resource_type import ResourceType
from engine.src.vertex import Vertex
from engine.src.edge import Edge
from engine.src.exceptions import *
from engine.src.trading.trade_offer import TradeOffer
from engine.src.structure.structure import Structure


class InputManager(cmd.Cmd):
    """Class managing input for a given player's turn. See docs for cmd.Cmd.

    Args:
        game (Game): The game being played.
        player (Player): Current player.

    Note that method docstrings are displayed to the user when they enter help.
    Implementation documentation should thus be given below the usual docstring.
    TODO: Commands do not support cancellation part way through.
    """
    def __init__(self, game, player):

        cmd.Cmd.__init__(self)

        self.game = game
        self.player = player
        self.prompt = '> {0}: '.format(self.player.name)

        self.has_rolled = False
        self.has_played_card = False

        self.structure_names = Utils.pluck(Config.get('structure.player_built'), 'name')

    def emptyline(self, line):
        """Override default emptyline behavior, which repeats last command."""
        self.default(line)

    def default(self, line):
        """Print menu of commands when unrecognized command given."""

        print 'Unrecognized command <{0}> given.'.format(line)
        self.do_help(None)

    def preloop(self):
        """Announce start of player turn."""

        msg = "{0}'s turn: ".format(self.player.name)
        InputManager.input_default(msg, None, False)

    def postloop(self):
        """Announce end of player turn."""

        msg = "End of {0}'s turn.".format(self.player.name)
        InputManager.input_default(msg, None, False)

    def do_roll(self, value):
        """Roll the dice."""

        self.game.roll_dice(value)
        self.has_rolled = True

    # TODO: Move core logic to game.
    def do_trade_player(self, line):
        """Trade resources with other players or with the bank."""

        if not self.has_rolled:
            print 'You must roll before you can trade.'
            return
        else:

            # Get list of requested resources
            msg = "Please enter a comma separated list of the number(s) " + \
                  "of the resource(s) you would like to offer."

            # offered_resources => resource_type => count
            offered_resources = InputManager.prompt_select_list_subset(
                msg, ResourceType.get_arable_types(),
                self.player.validate_resources
            )

            # Take csv list of offered resources
            msg = "Please enter a comma separated list of the number(s) " + \
                  "of the resource(s) you would like to receive."

            # requested_resources => resource_type => count
            requested_resources = InputManager.prompt_select_list_subset(
                msg, ResourceType.get_arable_types())

            # Create a trade offer
            trade_offer = TradeOffer(offered_resources, requested_resources)

            # Get player who will give requested resources and receive
            # offered resources.
            msg = "Please enter the number (e.g. '1') of the player " + \
                  "you would like to trade with."

            tradeable_players = filter(lambda player: player != self.player,
                                       self.game.players)

            if not tradeable_players:
                msg = 'No players to trade with.'
                InputManager.input_default(msg, None, False)
                return

            other_player = InputManager.prompt_select_list_value(
                msg, map(lambda player: player.name, tradeable_players),
                tradeable_players
            )

            try:
                other_player.trade(self.player, trade_offer)

                distributions = {
                    self.player: requested_resources,
                    other_player: offered_resources
                }

                InputManager.input_default('Trade complete.', None, False)

            # TODO: Specify explicit possible exceptions.
            except Exception as e:
                InputManager.input_default(e, None, False)

    # TODO
    def do_trade_bank(self, line):
        print('not yet implemented')

    # TODO
    # TODO: long term. Refactor to be compatible w/ any trade intermediary.
    def do_trade_harbor(self, line):
        print('not yet implemented')

    def do_build(self, line):
        """Build structures, including settlements, cities, and roads."""

        if not self.has_rolled:
            print 'You must roll before you can build.'
            return

        try:
            msg = "Please enter the number (e.g. '1') of the structure " + \
                  "you would like to build."

            structure_name = InputManager.prompt_select_list_value(
                msg, self.structure_names)

            self.game.place_structure(self.player, structure_name)

        except (NotEnoughStructuresException, BoardPositionOccupiedException,
                InvalidBaseStructureException,
                InvalidStructurePlacementException), e:
            self.player.restore_structure(structure_name)
            InputManager.input_default(e, None, False)

    # TODO: Enforce can't play card bought during same turn.
    def do_buy_card(self, line):
        """Buy a development card."""

        if not self.has_rolled:
            msg = 'You must roll before you can buy a development card.'
            InputManager.input_default(msg, None, False)
        elif self.has_played_card:
            msg = 'You may only play one card per turn.'
            InputManager.input_default(msg, None, False)
        else:

            try:
                dev_card = self.game.board.bank.buy_development_card(self.player)

                success_msg = 'You received a {0}!'.format(str(dev_card))

                InputManager.input_default(success_msg, None, False)

            except NotEnoughDevelopmentCardsException as n:
                InputManager.input_default(n, None, False)
            except NotEnoughResourcesException as n:
                InputManager.input_default(n, None, False)

    def do_play_card(self, line):
        """Play a development card."""

        if self.has_played_card:
            msg = 'You may only play one card per turn.'
            InputManager.input_default(msg, None, False)
        else:

            msg = "Please enter the number (e.g. '1') of the development " + \
                  "card you would like to play."

            dev_card = InputManager.prompt_select_list_value(
                msg,
                map(lambda card: card.name, self.player.development_cards),
                self.player.development_cards
            )

            if not dev_card:
                InputManager.input_default(
                    'Player has no development cards to choose from',
                    None, False)
                return

            try:
                dev_card.play_card(self.game, self.player)

            # TODO: Make clear which exceptions can be caught.
            except Exception as e:
                InputManager.input_default(e, None, False)

    # TODO: Improve.
    def do_print_board(self, line):
        """View the board."""

        for tile in self.game.board.iter_tiles():
            print tile

    def do_view_resource_cards(self, line):
        """View your resource cards."""

        msg = map(lambda resource_type: str(resource_type),
                  self.player.get_resource_list())

        InputManager.input_default(msg, None, False)

    # TODO
    def do_view_structures(self, line):
        """View your vertex and edge structures."""

        edge_structures = []
        vertex_structures = []

        for x, y in self.game.board.iter_tile_coords():
            tile = self.game.board.get_tile_with_coords(x, y)

            if not tile:
                continue

            for edge_dir in EdgeDirection:
                edge_val = tile.get_edge(edge_dir)

                if isinstance(edge_val, Structure) and \
                              edge_val.owning_player == self.player:

                    edge_structures.append( (tile, edge_dir, edge_val) )

            for vertex_dir in VertexDirection:
                vertex_val = tile.get_vertex(vertex_dir)

                if isinstance(vertex_val, Structure) and \
                              vertex_val.owning_player == self.player:
                    vertex_structures.append( (tile, vertex_dir, vertex_val) )

        structures = []
        tups_to_print = []

        for s in edge_structures:
            if s[2] not in structures:
                structures.append(s[2])
                tups_to_print.append(s)

        for s in vertex_structures:
            if s[2] not in structures:
                structures.append(s[2])
                tups_to_print.append(s)

        msg = '\n' + '\n'.join(map(lambda tup: 'Tile: {}\tDirection: {}\tStructure: {}'.format(
            tup[0], tup[1], tup[2].name), tups_to_print))

        InputManager.input_default(msg, None, False)

    def do_end_turn(self, line):
        """End your current turn."""

        if not self.has_rolled:
            print 'You must roll before you can end your turn.'
        else:
            return True

    def do_quit(self, line):
        """Quit the game for all players."""
        print '\nYou quit the game.'
        sys.exit(0)

    # Testing Methods
    def do_aybabtu(self, count):
        """All your base are belong to us."""

        if not count:
            count = 100
        else:
            count = int(count)

        for resource_type in ResourceType.get_arable_types():
            self.player.deposit_resources(resource_type, count)

    @staticmethod
    def input_default(msg, default=None, read_result=True):
        """Asks for user data using the format specified below.

        Returns:
            str. string entered by the user, or default if nothing was entered.
        """

        prompt = '> {0}'.format(str(msg))

        if default:
            prompt += " (or press enter to use default {0}): ".format(default)

        if read_result:
            prompt += '\n< '
            result = raw_input(prompt)
            # TODO: only return default if default flag true
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
                    InputManager.input_default(
                        'Enter number of players',
                        Config.get('game.default_player_count')
                    )
                )

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
    def prompt_select_player(game, players=None):

        if players is None:
            players = game.players

        msg = "Please enter the number (e.g. '1') of the player" + \
              "you would like to choose."

        return InputManager.prompt_select_list_value(msg, players)

    @staticmethod
    def prompt_tile_coordinates(game):

        x, y = None, None

        valid_coords = False

        while not valid_coords:
            try:
                x = int(InputManager.input_default(
                    'Please specify a tile x coordinate:', None))

                y = int(InputManager.input_default(
                    'Please specify a tile y coordinate:', None))

                valid_coords = game.board.valid_tile_coords(x, y)

                if not valid_coords:
                    raise ValueError
            except Exception:
                error_msg = "Invalid coordinates. Please try again."
                InputManager.input_default(error_msg, None, False)

        return x, y

    @staticmethod
    def prompt_select_list_value(prompt_msg, display_list, value_list=None):
        """Select and return a list element.

        Whenever we want to display a list and have the user select one entry
        in the list, we should use this method.

        If we want to display elements of one list to the user, but want to
        return a value different from the display value, we can provide both
        display and value lists. The user will select an index based on the
        values displayed, but the return value will result from using that same
        index to index into the value list.
        """

        if len(display_list) == 0:
            return None

        selected_element = None

        if value_list is None:
            value_list = display_list

        valid = False

        while not valid:

            for index, element in enumerate(display_list):
                print '({0}) {1}'.format(index + 1, element)

            try:
                index = int(InputManager.input_default(prompt_msg))
                selected_element = value_list[index - 1]

                valid = True

            except (IndexError, ValueError, TypeError):
                print "Invalid number given. You must give a number " + \
                      "between 1 and {0}.".format(len(display_list))

        return selected_element

    @staticmethod
    def prompt_select_list_subset(prompt_msg, allowed_values_lst,
                                  validate_func=None):
        """Prompt user to select a subset of the allowed values list.

        User should input comma separated value list, where each value is an
        index of one of the displayed list elements.
        """

        selected_elements = []

        # Show the list of elements; indices offset by one for user readability.
        for index, element in enumerate(allowed_values_lst):
            print '({0}) {1}'.format(index + 1, element)

        valid = False
        index_list = []

        while not valid:

            index_list = InputManager.input_default(prompt_msg)\
                .replace(' ', '').split(',')

            try:

                resource_count_dict = Utils.convert_list_to_count_dict(map(
                    lambda index: allowed_values_lst[int(index) - 1],
                    index_list
                ))

                valid = validate_func(resource_count_dict) \
                    if validate_func is not None else True

            except (IndexError, ValueError):
                print "Invalid number given. All numbers must be " + \
                      "between 1 and {0}.".format(len(allowed_values_lst))
            except NotEnoughResourcesException as n:
                InputManager.input_default(n, None, False)

        return resource_count_dict

    @staticmethod
    def prompt_select_resource_type():

        msg = "Please enter the number (e.g. '1') of the resource type" + \
              "you would like to choose."

        return InputManager.prompt_select_list_value(msg, list(ResourceType))

    @staticmethod
    def prompt_vertex_direction():

        msg = "Please enter the number (e.g. '1') of the direction " + \
              "from the center of the tile to the vertex you would " + \
              "like to place a structure on."

        return InputManager.prompt_select_list_value(msg, list(VertexDirection))

    @staticmethod
    def prompt_edge_direction():

        msg = "Please enter the number (e.g. '1') of the direction " + \
              "from the center of the tile to the edge you would " + \
              "like to place a structure on."

        return InputManager.prompt_select_list_value(msg, list(EdgeDirection))

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

    # TODO: Roll announce methods into single method? Or programatically set.

    @staticmethod
    def announce_roll_value(roll_value):

        prompt = 'Player rolled a {0}'.format(roll_value)
        InputManager.input_default(prompt, None, False)

    @staticmethod
    def announce_initial_structure_placement_stage():

        prompt = 'Beginning initial structure placement stage.'
        InputManager.input_default(prompt, None, False)

    @staticmethod
    def announce_player_turn(player):

        prompt = "Beginning {0}'s turn.".format(player.name)
        InputManager.input_default(prompt, None, False)

    @staticmethod
    def announce_structure_placement(player, structure_name):

        prompt = "{0}, select where you would like to place your {1}".format(
            player.name, structure_name
        )
        InputManager.input_default(prompt, None, False)

    @staticmethod
    def announce_development_card_played(player, development_card):

        prompt = "{0} played a development card: {1}".format(
            player.name, str(development_card))
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
