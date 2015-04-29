# -*- coding: utf-8 -*-
import random
import pdb

from engine.src.lib.utils import Utils
from engine.src.board.hex_board import HexBoard
from engine.src.tile.game_tile import GameTile
from engine.src.resource_type import ResourceType
from engine.src.position_type import PositionType
from engine.src.calamity.calamity import Calamity
from engine.src.calamity.calamity import CalamityTilePlacementEffect
from engine.src.calamity.robber import Robber
from engine.src.trading.bank import Bank
from engine.src.direction.edge_vertex_mapping import EdgeVertexMapping
from engine.src.direction.edge_direction import EdgeDirection
from engine.src.direction.vertex_direction import VertexDirection
from engine.src.exceptions import *
from engine.src.structure.structure import Structure


class GameBoard(HexBoard):
    """A Settlers of Catan playing board.

    Attributes:
        radius (int): See HexBoard.

        tiles (dict): See HexBoard.

        tile_cls (class): See HexBoard.

        bank (Bank): Bank of resources the board will interact with.

    Args:
        radius (int): See HexBoard.
    """

    def __init__(self, radius):

        super(GameBoard, self).__init__(radius, GameTile)

        # We have tiles, but they currently have no value and are all FALLOW.
        # Here we assign resource types and chit values.
        self.assign_tile_resources()
        self.assign_tile_chit_values()
        self.assign_tile_harbors()

        self.bank = Bank(len(list(self.iter_tiles())))

    def assign_tile_resources(self, assignment_func=None):
        """Assign resource types to this board's tiles.

        Args:
            assignment_func (func): Resources will assigned according to this
              function. If not provided, will default to
              self._default_assign_tile_resources()

        Returns:
            None.
        """

        if assignment_func is None:
            self._default_assign_tile_resources()
        else:
            assignment_func()

    def _default_assign_tile_resources(self):
        """Distributes non-fallow resource types across the board evenly.

        Specifically, assigns one ResourceType.FALLOW tile, then splits the
        resource types of the remaining tiles evenly.

        Returns:
            None.

        TODO: Defaults to only one FALLOW tile regardless of board size.
              Perhaps should make fallow tile count relative to board size.
        """

        # Get a randomized list of the tiles of this board.
        tiles = list(self.iter_tiles())
        random.shuffle(tiles)

        resource_type_count = len(ResourceType.get_arable_types())

        # We'll allocate one fallow tile so divide arable resources among
        # total number of tiles - 1.
        per_resource_count = (len(tiles) - 1) / float(resource_type_count)

        # Say that we find that we need to allocate 3.6 tiles per resource.
        # Clearly we can only allocate whole number tiles. So we take the
        # difference between what we calculated and its floor (e.g. .6),
        # and multiply it by the number of tiles to get the number of
        # leftover tiles that need to be assigned.
        leftover_count = int((per_resource_count - int(per_resource_count)) *
                             resource_type_count)

        per_resource_count = int(per_resource_count)

        # Get a list containing resource_type_count occurrences of each
        # resource_type.
        resources = Utils.flatten(map(
            lambda resource: [resource] * per_resource_count,
            ResourceType.get_arable_types()
        ))

        # We then allocate leftover tiles according to some priority. In a
        # base Settlers of Catan game, this priority manifests as having only
        # 3 brick and ore tiles, by 4 lumber, wool, and wheat tiles.
        while leftover_count:
            resources.append(
                ResourceType.get_priority_arable_types()[leftover_count - 1])
            leftover_count -= 1

        # Add a single occurrence of ResourceType.FALLOW.
        resources.append(ResourceType.FALLOW)

        # Assign the resource types to the shuffled tiles.
        for tile, resource_type in zip(tiles, resources):
            tile.resource_type = resource_type

    def _randomly_assign_tile_resources(self):
        """Randomly assign resource types to this board's tiles.

        Note that this randomly draws from all ResourceType's, i.e. including
        ResourceType.FALLOW.

        Returns:
            None.
        """

        for tile in self.iter_tiles():
            tile.resource_type = ResourceType.random()

    def assign_tile_chit_values(self, assignment_func=None):
        """Assign chit values to this board's tiles.

        Args:
            assignment_func (func): Chit values will assigned according to this
              function. If not provided, will default to
              self._default_assign_tile_chit_values()

        Returns:
            None.
        """

        if assignment_func is None:
            self._default_assign_tile_chit_values()
        else:
            assignment_func()

    def _randomly_assign_tile_chit_values(self, start=2, end=12,
                                          exclude=Calamity.DEFAULT_ROLL_VALUES):
        """Randomly assign chit values to this board's tiles.

        Args:
            start (int): The set of possible chit values from which values to
              assign will be randomly drawn is defined by the range defined by
              start and end.

            end (int): See above.

            exclude (list): A list of values that lie in the range given by
              start and end that should not be included in the set of possible
              chit values.

        Returns:
            None
        """

        chit_values = frozenset(range(start, end + 1)).intersection(exclude)

        for chit_value, tile in zip(chit_values, self.iter_tiles()):
            tile.chit_value = chit_value

    def _default_assign_tile_chit_values(self, start=2, end=12,
                                         exclude=Calamity.DEFAULT_ROLL_VALUES):
        """Assign chit values in a manner similar to that of the original game.

        Specifically, find out how many times each value would occur if we
        were to distribute them over the board's non-fallow tiles evenly,
        except for the highest and lowest values (presumably the least likely
        to occur), which should only appear on the board half as often.

        Args:
            start (int): Together with end, defines the range of possible
              chit values.

            end (int): See above.

            exclude (list): A list of values that lie in the range defined by
              start and end that should not be included in the set of possible
              chit values.

        Returns:
            None.

        TODO: Consider storing self.tile_count instead of using the length
              of the iterator. For now, however, performance not an issue.
        """

        chit_values = filter(
            lambda value: value not in exclude, range(start, end + 1)
        )

        min_chit_value = chit_values[0]
        max_chit_value = chit_values[-1]

        # We only want to consider arable tiles.
        arable_tiles = list(self.iter_arable_tiles())
        tile_count = len(arable_tiles)

        # Since the lowest and highest chit values will occur half as
        # frequently, we act as if we were only had len(chit_values) - 1 values.
        per_value_count = tile_count / (len(chit_values) - 1)

        # We want the highest and lowest value chits to appear half as often.
        def get_value_occurrence_count(value):
            if value == min_chit_value or value == max_chit_value:
                return per_value_count / 2
            else:
                return per_value_count

        # Get a list of all the chit values we will place e.g. if we expect
        # to place 5 chits of value 3, then 3 should occur 5 times in the list.
        chit_values_to_assign = Utils.flatten(map(
            lambda value: [value] * get_value_occurrence_count(value),
            chit_values
        ))

        # Assign chit values to arable tiles only.
        for tile, chit_value_to_assign in zip(arable_tiles,
                                              chit_values_to_assign):
            tile.chit_value = chit_value_to_assign

    def assign_tile_harbors(self):
        """Assign harbors to this board.

        TODO: Officially, harbors seem to be placed after every
              3rd then 3rd then 4th edge. This is a pain to program given that
              it only _seems_ that way.
        """

        # TODO
        pass

    def iter_arable_tiles(self):
        """Iterate over this board's non-fallow i.e. arable tiles."""

        for tile in self.iter_tiles():
            if tile.resource_type != ResourceType.FALLOW:
                yield tile

    def place_vertex_structure(self, x, y, vertex_dir, structure,
                               must_border_claimed_edge=True, struct_x=None,
                               struct_y=None, struct_vertex_dir=None):
        """Place a structure of the given type on the specified vertex.

        Args:
            See self.update_vertex().

            structure (Structure): Structure to replace the specified vertex
              with.

        Returns:
            None.

        Raises:
            InvalidBaseStructureException. If structure to be placed is an
              upgrade or extension of a structure class that hasn't been
              placed at the defined vertex.
        """

        tile = self.tiles[x][y]
        old_vertex_val = tile.vertices[vertex_dir]

        self.validate_structure_placement(x, y, old_vertex_val, structure,
                                          vertex_dir, must_border_claimed_edge,
                                          struct_x, struct_y, struct_vertex_dir)

        self.update_vertex(x, y, vertex_dir, structure)

    def place_edge_structure(self, x, y, edge_dir, structure,
                             must_border_claimed_edge=True, struct_x=None,
                             struct_y=None, struct_vertex_dir=None):
        tile = self.tiles[x][y]
        vertex_dirs = EdgeVertexMapping.get_vertex_dirs_for_edge_dir(edge_dir)
        old_edge_val = tile.edges[vertex_dirs[0]][vertex_dirs[1]]

        self.validate_structure_placement(x, y, old_edge_val, structure,
                                          edge_dir, must_border_claimed_edge,
                                          struct_x, struct_y, struct_vertex_dir)

        self.update_edge(x, y, edge_dir, structure)

    def validate_structure_placement(self, x, y, old_value, new_value,
                                     placement_dir, must_border_claimed_edge,
                                     struct_x, struct_y, struct_vertex_dir):

        # A structure can only be placed on a vertex if none of the three
        # adjacent vertices are occupied aka the Distance Rule.
        if new_value.position_type == PositionType.VERTEX:

            adjacent_vertex_vals = \
                self.get_adjacent_vertices_for_vertex(x, y, placement_dir)

            adjacent_structures = filter(
                lambda vertex_val: isinstance(vertex_val, Structure),
                adjacent_vertex_vals
            )

            if len(adjacent_structures):
                raise InvalidStructurePlacementException()

        # If the struct_x etc. are provided, they specify a vertex the new
        # edge to place must border e.g. as in initial placement stage.
        if new_value.position_type == PositionType.EDGE and \
                        struct_x is not None:
            allowable_edges = self.get_adjacent_edges(struct_x, struct_y, struct_vertex_dir)
            target_edge = self.get_tile_with_coords(x, y).get_edge(placement_dir)

            if target_edge not in allowable_edges:
                raise InvalidStructurePlacementException()

        # If the player is replacing an existing structure...
        if isinstance(old_value, Structure):

            # The old structure must be owned by the same player.
            if old_value.owning_player != new_value.owning_player:
                raise BoardPositionOccupiedException((x, y), old_value,
                                                     old_value.owning_player)

            # The new value must be an augmenting structure whose base structure
            # matches the existing structure.
            if (not new_value.is_augmenting_structure()) or \
                    (new_value.is_augmenting_structure() and \
                     old_value.name != new_value.augments):
                raise InvalidBaseStructureException(old_value, new_value)

        # If the player is not replacing an existing structure, make sure it's
        # neighboring a road, unless overridden e.g. as during initial
        # structure placement.
        elif must_border_claimed_edge:
            if placement_dir in EdgeDirection:
                edge_vals = self.get_adjacent_edges_for_edge(x, y, placement_dir)
            elif placement_dir in VertexDirection:
                edge_vals = self.get_adjacent_edges_to_vertex(x, y, placement_dir)

            claimed_edge_structs = filter(
                lambda edge_val: isinstance(edge_val, Structure) and
                                 edge_val.owning_player == new_value.owning_player,
                edge_vals
            )

            if not len(claimed_edge_structs):
                raise InvalidStructurePlacementException()

    def distribute_resources_for_roll(self, roll_value):
        """Distribute resources to the players based on the given roll value.

        Resources are distributed as follows: Whenever a value is rolled that
        matches the chit value of a tile, for all structures on that tile,
        distribute the number of resources dictated by the yield of that
        structure of the type of that tile.

        Args:
            roll_value (int): Dice roll value used to determine which tiles
              should yield resources this turn.

        Returns:
            dict. Primary keys are players and secondary keys are resource
              types. Stored values are the number of a given resource that was
              distributed to the player.
        """

        # Find those tiles whose chit value matches the roll value,
        # and whose yield isn't blocked by a calamity.
        resource_tiles = filter(
            lambda tile:
                tile.chit_value == roll_value and
                (CalamityTilePlacementEffect.BLOCK_YIELD not in
                    tile.get_calamity_tile_placement_effects()),
            list(self.iter_tiles())
        )

        distributions = Utils.nested_dict()

        # Create a dictionary that stores per-player resource distributions.
        # i.e. distributions => player => resource_type => (int)
        for resource_tile in resource_tiles:

            # Find any structures built on the vertices of the found tiles.
            adjacent_structures = resource_tile.get_adjacent_vertex_structures()

            for structure in adjacent_structures:
                player = structure.owning_player
                resource_type = resource_tile.resource_type
                resource_yield = structure.base_yield

                if not distributions[player][resource_type]:
                    distributions[player][resource_type] = 0

                distributions[player][resource_type] += resource_yield

        self.distribute_resources(distributions)

        return distributions

    def distribute_resources(self, distributions):

        # Now distribute resources to players, if the bank has enough.
        for resource_type in ResourceType.get_arable_types():

            def get_per_player_production(player):
                resource_count = distributions[player][resource_type]
                return resource_count if resource_count else 0

            total_count = sum(map(get_per_player_production, distributions))

            try:
                self.bank.withdraw_resources(resource_type, total_count)

                for player in distributions:

                    count = distributions[player][resource_type]

                    if count:
                        player.deposit_resources(resource_type, count)

            except NotEnoughResourcesException:
                # Bank didn't have enough of the current resource to distribute
                # to all players, so distribute none of this resource.
                pass

        return distributions

    def find_robber(self):
        """Return the robber we can find."""

        for tile in self.iter_tiles():
            for calamity in tile.calamities:
                if isinstance(calamity, Robber):
                    return calamity

        return None

    def get_tile_of_resource_type(self, resource_type):
        """Returns first found file of specified resource type."""

        for tile in self.iter_tiles():
            if tile.resource_type == resource_type:
                return tile

        return None

    def find_tile_with_calamity(self, calamity):

        for tile in self.iter_tiles():
            if calamity in tile.calamities:
                return tile

        return None

    def place_calamity(self, x, y, calamity):

        tile = self.get_tile_with_coords(x, y)
        tile.add_calamity(calamity)
