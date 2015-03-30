# -*- coding: utf-8 -*-

from .hex_tile import HexTile


class GameTile(HexTile):
    """A hex tile as used in a game of Settlers of Catan.

    Args:
        resource (ResourceType): The resource/terrain of this hex.

        chit_value (int): The value of the chit (i.e. the circular number token)
          to be placed on this hex.
    """

    def __init__(self, x, y, resource=None, chit_value=None):

        super(GameTile, self).__init__(x, y)

        self.resource = resource
        self.chit_value = chit_value
