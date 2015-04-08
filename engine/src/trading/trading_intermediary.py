# -*- coding: utf-8 -*-
from engine.src.trading.trading_entity import TradingEntity


class TradingIntermediary(object):
    """Represents an entity capable of trading resources on behalf of two other
    TradingEntity's, but incapable of storing resources itself.

    Args:
        supplier (TradingEntity): The entity who owns the resources this
          intermediary is allowed to trade on its behalf.
    """

    def __init__(self, supplier):

        if not isinstance(supplier, TradingEntity):
            message = 'Invalid trading entity given as supplier'
            raise ValueError(message)

        self.supplier = supplier

    def trade(self, other_entity, trade_offer):
        """Attempt to execute the given trade.

        Args:
            other_entity (TradingEntity): Entity that proposed the trade to
              the harbor.

            trade_offer (TradeOffer): Trade offer crafted by the other entity.

        Returns:
            None.
        """

        self.supplier.trade(other_entity, trade_offer)
