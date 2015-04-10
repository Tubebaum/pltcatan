# -*- coding: utf-8 -*-
from engine.src.config import Config
from engine.src.trading.trading_entity import TradingEntity


class Bank(TradingEntity):
    """Represents the bank of all available resource cards.

    Attributes:
        resources (dict): See TradingEntity.

    Args:
        tile_count (int): Number of tiles for the board this bank will be used
          with.
    """

    def __init__(self, tile_count=Config.DEFAULT_TILE_COUNT):

        super(Bank, self).__init__()
        self._default_init_resources(tile_count)

    def _default_init_resources(self, tile_count):
        """Determine the initial resources for the bank.

        Though not officially a rule, one notices that the default card
        allocation for the base game is such that there is, for each resource
        type, the same number of cards as there are tiles on the board. In
        order to make this function work for different size boards, this is
        the rule used to default allocate resource types.

        Args:
            tile_count (int): Number of tiles on the playing board.

        Returns:
            None. Modifies self.resources.
        """

        super(Bank, self)._default_init_resources(tile_count)



