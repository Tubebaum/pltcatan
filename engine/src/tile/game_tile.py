# -*- coding: utf-8 -*-
from engine.src.tile.hex_tile import HexTile
from engine.src.resource_type import ResourceType
from engine.src.structure.structure import Structure


class GameTile(HexTile):
    """A hex tile as used in a game of Settlers of Catan.

    Args:
        resource (ResourceType): The resource/terrain of this hex.

        chit_value (int): The value of the chit (i.e. the circular number token)
          to be placed on this hex.

        calamities (list): A list of calamity objects placed on this tile i.e.
          whose passive effects currently affect this tile.
    """

    def __init__(self, x, y,
                 resource_type=ResourceType.FALLOW, chit_value=0):

        super(GameTile, self).__init__(x, y)

        self.resource_type = resource_type
        self.chit_value = chit_value
        self.calamities = []

    def __str__(self):
        return '({0}, {1}) {2} {3}'.format(self.x, self.y,
                                           self.resource_type, self.chit_value)

    def __repr__(self):
        return self.__str__()

    def get_adjacent_vertex_structures(self):
        """Return any vertices that are structures."""

        return filter(
            lambda vertex: issubclass(vertex.__class__, Structure),
            list(self.iter_vertices())
        )

    def remove_calamity(self, calamity):
        """Remove a calamity from this tile.

        Args:
            calamity (Calamity): A calamity currently positioned on, and
              affecting, this tile, that will be removed.
        """

        self.calamities = filter(
            lambda existing_calamity: calamity != existing_calamity,
            self.calamities
        )

    def add_calamity(self, calamity):
        """Add a calamity to this tile.

        Args:
            calamity (Calamity): A calamity that, after calling this method,
              will be positioned on, and affect, this tile. The calamity to be
              added.

        Returns:
            boolean. Whether or not calamity was successfully added. Won't be
              successfully added if had already been placed on this tile.
        """

        if calamity in self.calamities:
            return False
        else:
            self.calamities.append(calamity)
            return True

    def get_calamity_tile_placement_effects(self):
        """Get a list of tile placement effects for this tile's calamities."""

        return filter(
            lambda effect: effect is not None,
            map(lambda calamity: calamity.tile_placement_effect,
                self.calamities)
        )
