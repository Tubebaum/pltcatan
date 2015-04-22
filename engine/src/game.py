from engine.src.config.config import Config
from engine.src.lib.utils import Utils
from engine.src.exceptions import BoardPositionOccupiedException
from engine.src.player import Player
from engine.src.dice import Dice
from engine.src.input_manager import InputManager
from engine.src.board.game_board import GameBoard
from engine.src.resource_type import ResourceType
from engine.src.structure.structure import Structure
from engine.src.calamity.robber import Robber


class Game(object):
    """A game of Settlers of Catan."""

    def __init__(self):

        self.dice = Dice()
        self.board = GameBoard(Config.get('board.default_radius'))

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
                InputManager(self, player).cmdloop()

            self.update_point_counts()
            max_point_count = self.get_winning_player().points

        # Print out game over message.
        winner = self.get_winning_player()
        print 'Game over. {0} wins with {1} points!\n'\
            .format(winner.name, winner.victory_point_count)

    def create_players(self):
        """Create a new batch of players."""

        self.players = []
        player_names = InputManager.get_player_names()

        for player_name in player_names:
            self.players.append(Player(player_name))

    def place_vertex_structure(self, player, structure_name):

        valid = False

        while not valid:
            try:
                x, y, vertex_dir = \
                    InputManager.prompt_vertex_placement(self)

                # TODO: Enforce valid.
                self.board.place_vertex_structure(
                    x, y, vertex_dir, player.get_structure(structure_name))

                valid = True
            except BoardPositionOccupiedException as b:
                InputManager.input_default(b, None, False)

        return x, y, vertex_dir

    def place_edge_structure(self, player, structure_name):

        valid = False

        while not valid:
            try:
                x, y, edge_dir = \
                    InputManager.prompt_edge_placement(self)

                # TODO: Enforce valid.
                self.board.place_edge_structure(
                    x, y, edge_dir, player.get_structure(structure_name))

                valid = True
            except BoardPositionOccupiedException as b:
                InputManager.input_default(b, None, False)

        return x, y, edge_dir

    # TODO: refactoring
    def initial_settlement_and_road_placement(self):

        InputManager.announce_initial_structure_placement_stage()

        for player in self.players:

            InputManager.announce_player_turn(player)

            # Place settlement
            InputManager.announce_structure_placement(player, 'settlement')
            self.place_vertex_structure(player, 'settlement')

            # Place road
            InputManager.announce_structure_placement(player, 'road')
            self.place_edge_structure(player, 'road')

        distributions = Utils.nested_dict()

        for player in list(reversed(self.players)):

            InputManager.announce_player_turn(player)

            # Place settlement
            InputManager.announce_structure_placement(player, 'settlement')
            x, y, vertex_dir = self.place_vertex_structure(player, 'settlement')

            # Place road
            InputManager.announce_structure_placement(player, 'road')
            self.place_edge_structure(player, 'road')

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
                    Config.get('structure.player_built.settlement.base_yield')

        self.board.distribute_resources(distributions)
        InputManager.announce_resource_distributions(distributions)

    def roll_dice(self, value=None):

        roll_value = self.dice.roll()
        InputManager.announce_roll_value(roll_value)

        # If a calamity value, handle calamity
        distributions = self.board.distribute_resources_for_roll(roll_value)

        InputManager.announce_resource_distributions(distributions)

    def get_winning_player(self):
        """Get the player who is winning this game of Settlers of Catan."""

        return max(self.players, key=lambda player: player.points)

    def update_point_counts(self):

        # Determine largest army
        player_with_largest_army = max(self.players, key=lambda player: player.knights)

        print('update_point_counts not implemented.')

