# -*- coding: utf-8 -*-
from engine.src.card.development_card.development_card import DevelopmentCard


class KnightCard(DevelopmentCard):

    def __init__(self):
        super(KnightCard, self).__init__()

    def effect_when_held(self, game, player):
        # No effect when held.
        pass

    def effect_when_played(self, game, player):
        """Move the robber and draw a card from another adjacent player."""

        game.input_manager.announce_development_card_played(player, self)

        robber = game.board.find_robber()

        robber.outside_trigger_effect(game, player)

        self.played = True
