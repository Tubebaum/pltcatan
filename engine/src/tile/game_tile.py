# -*- coding: utf-8 -*-
from engine.src.tile.hex_tile import HexTile
from engine.src.resource_type import ResourceType
from engine.src.vertex.structure.structure import Structure


class GameTile(HexTile):
    """A hex tile as used in a game of Settlers of Catan.

    Args:
        resource (ResourceType): The resource/terrain of this hex.

        chit_value (int): The value of the chit (i.e. the circular number token)
          to be placed on this hex.
    """

    def __init__(self, x, y,
                 resource_type=ResourceType.FALLOW, chit_value=None):

        super(GameTile, self).__init__(x, y)

        self.resource_type = resource_type
        self.chit_value = chit_value

    def __str__(self):
        return "Coordinates: ({0}, {1})\nResource Type: {2}\nChit value: {3}\n"\
            .format(self.x, self.y, self.resource_type, self.chit_value)

    def get_adjacent_structures(self):
        """Return any vertices that are structures."""

        return filter(
            lambda vertex: issubclass(vertex.__class__, Structure),
            list(self.iter_vertices())
        )


