# -*- coding: utf-8 -*-
import random

from engine.src.config.config import Config
from engine.src.trading.trading_entity import TradingEntity
from engine.src.trading.trade_offer import TradeOffer
from engine.src.exceptions import *
from engine.src.card.development_card import DevelopmentCard


class Bank(TradingEntity):
    """Represents the bank of all available resource cards.

    Attributes:
        resources (dict): See TradingEntity.

        development_cards (list): A list of different development card objects.

    Args:
        tile_count (int): Number of tiles for the board this bank will be used
          with.
    """

    def __init__(self, tile_count=None):
        if tile_count is None:
            tile_count = Config.get('game.board.tile_count')

        super(Bank, self).__init__()

        self.development_cards = []

        self._default_init_development_cards()
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

    def _default_init_development_cards(self):
        """Add a configured number of each development card type to the bank."""

        dev_card_dict = Config.get('game.card.development')

        for name, card in dev_card_dict.iteritems():
            for _ in range(card['count']):
                dev_card = DevelopmentCard(**card)
                self.development_cards.append(dev_card)

        random.shuffle(self.development_cards)

    def buy_development_card(self, player):
        """Let the given player purchase a development card from the bank."""

        card = self.development_cards.pop()

        if not card:
            raise NotEnoughDevelopmentCardsException

        # Create a trade offer where there are no requested resources,
        # just offered resources (cost of development card).
        trade_offer = TradeOffer(card.cost, {})

        obstructing_entity, obstructing_resource_type = \
            trade_offer.validate(player, self)

        # If the trade offer is valid, transfer the cost cards and give
        # the player the development card.
        if not obstructing_entity and not obstructing_resource_type:
            trade_offer.execute(player, self)
            player.development_cards.append(card)
            return card
        # Otherwise, return the development card to the deck.
        else:
            self.development_cards.append(card)
            raise NotEnoughResourcesException(obstructing_entity, obstructing_resource_type)
