# -*- coding: utf-8 -*-
from engine.src.trading.trading_intermediary import TradingIntermediary


class Harbor(TradingIntermediary):
    """Represents a trading harbor in Settlers of Catan.

    Attributes:
        supplier (TradingEntity): See TradingIntermediary.

        trade_criteria (TradeCriteria): A rule that must be followed for a
          trade conducted through this harbor to be considered valid.
    """

    def __init__(self, supplier, trade_criteria):

        super(Harbor, self).__init__(supplier)
        self.trade_criteria = trade_criteria

    def trade(self, other_entity, trade_offer):
        """Attempt to execute the trade only if it follows the trade criteria.

        Args:
            See TradingIntermediary for:
                other_entity (TradingEntity)
                trade_offer (TradeOffer)

        Returns:
            None.
        """

        if self.trade_criteria.permits(trade_offer):
            super(Harbor, self).trade(other_entity, trade_offer)
