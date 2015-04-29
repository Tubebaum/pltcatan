# -*- coding: utf-8 -*-
from engine.src.lib.utils import Utils
from engine.src.config.config import Config
from engine.src.structure.structure import Structure
from engine.src.trading.trading_entity import TradingEntity
from engine.src.exceptions import NotEnoughStructuresException


class Player(TradingEntity):
    """A player in a game of Settlers of Catan.

    Attributes:
        resources (dict): See TradingEntity.

        name (str): This player's name.

    Args:
        name (str): Name to assign a new player.
    """

    def __init__(self, name):

        super(Player, self).__init__()

        self.name = name

        self.development_cards = []

        self.points = 0
        self.hidden_points = 0
        self.special_points = 0

        self.knights = 0
        self.longest_road_length = 0

        self.remaining_structure_counts = {}
        self.init_structure_counts()

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name

    def init_structure_counts(self):

        self.remaining_structure_counts = {}

        for structure in Config.get('structure.player_built').values():
            self.remaining_structure_counts[structure['name']] = structure['count']

    def get_total_points(self):
        return self.points + self.hidden_points + self.special_points

    # TODO: pay for placing structure
    def get_structure(self, structure_name):
        """Get the given structure from the player's stock, if any remains.

        Every time a player builds a structure, we need to remove from their
        stock, e.g. remaining_road_count etc. This method generalizes this
        process of removal for all structures.

        Args:
            structure_name (str): Class of structure to build.
        """

        structure_count = self.remaining_structure_counts[structure_name]

        if structure_count > 0:
            self.remaining_structure_counts[structure_name] -= 1

            # TODO: conversions between underscore and camel case
            config_path = 'structure.player_built.' + structure_name.lower()
            structure_dict = Config.get(config_path)

            return Structure(self, **structure_dict)
        else:
            raise NotEnoughStructuresException(self, structure_name)

    # TODO: Restore cost of structure
    def restore_structure(self, structure_name):
        self.remaining_structure_counts[structure_name] += 1
