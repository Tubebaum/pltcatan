import pdb
from engine.src.config.config import Config
from engine.src.lib.utils import Utils
from engine.src.exceptions import *
from engine.src.player import Player
from engine.src.dice import Dice
from engine.src.trading.trade_offer import TradeOffer
from engine.src.input_manager import InputManager
from engine.src.board.game_board import GameBoard
from engine.src.resource_type import ResourceType
from engine.src.position_type import PositionType
from engine.src.structure.structure import Structure
from engine.src.calamity.robber import Robber
from engine.src.longest_road_search import LongestRoadSearch

from imperative_parser.oracle import ORACLE

class Game(object):
    """A game of Settlers of Catan."""

    def __init__(self):

        Config.init()
        ORACLE.set('game', self)

        self.dice = Dice()
        self.board = GameBoard(Config.get('game.board.radius'))
        ORACLE.set('board', self.board)

        # Place the robber on a fallow tile.
        self.robber = Robber()
        tile = self.board.get_tile_of_resource_type(ResourceType.FALLOW)
        tile.add_calamity(self.robber)

        self.players = []
        self.input_manager = InputManager

    def start(self):
        self.create_players()
        self.initial_settlement_and_road_placement()
        self.game_loop()

    def game_loop(self):

        max_point_count = 0

        while max_point_count < Config.get('game.points_to_win'):
            for player in self.players:
                ORACLE.set('player', player)
                InputManager(self, player).cmdloop()
                self.update_point_counts()
                max_point_count = self.get_winning_player().get_total_points()

        # Print out game over message.
        winner = self.get_winning_player()
        print 'Game over. {0} wins with {1} points!\n'\
            .format(winner.name, winner.get_total_points())

    def create_players(self):
        """Create a new batch of players."""

        self.players = []
        player_names = InputManager.get_player_names()

        for player_name in player_names:
            self.players.append(Player(player_name))

        ORACLE.set('players', self.players)

    def place_structure(self, player, structure_name, must_border_claimed_edge=True,
                        struct_x=None, struct_y=None, struct_vertex_dir=None, free_to_build=False):
        """Place an edge or vertex structure.

        Prompts for placement information and attempts to place on board. Does
        not do any exception handling.
        """

        try:

            structure = player.get_structure(structure_name)

            if not free_to_build:
                # Requesting structure, not further resources
                trade_offer = TradeOffer(structure.cost, {})
                obstructing_entity, obstructing_resource_type = \
                    trade_offer.validate(player, self.board.bank)

                if not obstructing_entity and not obstructing_resource_type:
                    trade_offer.execute(player, self.board.bank)
                else:
                    raise NotEnoughResourcesException(obstructing_entity, obstructing_resource_type)

            if structure.position_type == PositionType.EDGE:
                prompt_func = InputManager.prompt_edge_placement
                placement_func = self.board.place_edge_structure
            elif structure.position_type == PositionType.VERTEX:
                prompt_func = InputManager.prompt_vertex_placement
                placement_func = self.board.place_vertex_structure

            x, y, struct_dir = prompt_func(self)

            params = [x, y, struct_dir, structure, must_border_claimed_edge]

            if struct_vertex_dir is not None:
                params.extend([struct_x, struct_y, struct_vertex_dir])

            placement_func(*params)

            player = structure.owning_player

            # Allocate points
            if structure.augments():
                # TODO: conversions from camelcase to underscore
                points = structure.point_value - Config.get('game.structure.player_built.' + structure_name.lower()).point_value
            else:
                points = structure.point_value

            player.points += points

            return x, y, struct_dir, structure

        except (NotEnoughStructuresException, NotEnoughResourcesException), e:
            raise
        except (BoardPositionOccupiedException, InvalidBaseStructureException,
                InvalidStructurePlacementException), e:

            if not free_to_build:
                # If we bought the structure but didn't place it properly,
                # return the cost of the structure to the player.
                player.deposit_multiple_resources(structure.cost)

            # And return the structure to their storage.
            player.restore_structure(structure_name)

            # Raise the caught error so that callers of this method can handle
            # it in a custom fashion.
            raise

    def place_init_structure(self, player, structure_name,
                             must_border_claimed_edge=False,
                             struct_x=None, struct_y=None,
                             struct_vertex_dir=None):

        valid = False

        while not valid:
            try:
                free_to_build = True

                x, y, struct_dir, struct = self.place_structure(player, structure_name, must_border_claimed_edge,
                                     struct_x, struct_y, struct_vertex_dir, free_to_build)

                valid = True
            except (BoardPositionOccupiedException,
                    InvalidBaseStructureException,
                    InvalidStructurePlacementException), e:
                player.restore_structure(structure_name)
                InputManager.input_default(e, None, False)

        return x, y, struct_dir

    def initial_settlement_and_road_placement(self):

        InputManager.announce_initial_structure_placement_stage()

        for player in self.players:

            InputManager.announce_player_turn(player)

            # Place settlement
            InputManager.announce_structure_placement(player, 'Settlement')
            x, y, vertex_dir = self.place_init_structure(player, 'Settlement')

            # Place road
            InputManager.announce_structure_placement(player, 'Road')
            self.place_init_structure(player, 'Road', False, x, y, vertex_dir)

        distributions = Utils.nested_dict()

        for player in list(reversed(self.players)):

            InputManager.announce_player_turn(player)

            # Place settlement
            InputManager.announce_structure_placement(player, 'Settlement')
            x, y, vertex_dir = self.place_init_structure(player, 'Settlement')

            # Place road
            InputManager.announce_structure_placement(player, 'Road')
            self.place_init_structure(player, 'Road', False, x, y, vertex_dir)

            # Give initial resource cards
            resource_types = filter(
                lambda resource_type: resource_type != ResourceType.FALLOW,
                map(lambda tile: tile.resource_type,
                    self.board.get_adjacent_tiles_to_vertex(x, y, vertex_dir))
            )

            for resource_type in resource_types:

                if not distributions[player][resource_type]:
                    distributions[player][resource_type] = 0

                distributions[player][resource_type] += \
                    Config.get('game.structure.player_built.settlement.base_yield')

        self.board.distribute_resources(distributions)
        InputManager.announce_resource_distributions(distributions)

    def roll_dice(self, value=None):

        roll_value = self.dice.roll()
        InputManager.announce_roll_value(roll_value)
        ORACLE.set('dice_value', roll_value)

        # If a calamity value, handle calamity
        distributions = self.board.distribute_resources_for_roll(roll_value)

        InputManager.announce_resource_distributions(distributions)

    def get_winning_player(self):
        """Get the player who is winning this game of Settlers of Catan."""

        return max(self.players, key=lambda player: player.points)

    def update_point_counts(self):

        for player in self.players:
            player.special_points = 0

        player_with_largest_army = max(self.players, key=lambda player: player.knights)

        # TODO: Move thresholds to config
        if player_with_largest_army.knights >= 3:
            print 'Largest army given to: {}'.format(player_with_largest_army)
            player_with_largest_army.special_points += 2

        player_road_len_dict = LongestRoadSearch(self.board).execute()

        for player, road_len in player_road_len_dict.iteritems():
            player.longest_road_length = road_len

        player_with_longest_road = max(player_road_len_dict)

        if player_with_longest_road.longest_road_length >= 5:
            print 'Longest road given to: {}'.format(player_with_longest_road)
            player_with_longest_road.special_points += 2
