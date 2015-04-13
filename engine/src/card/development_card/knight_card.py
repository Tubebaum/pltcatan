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

        x, y = game.input_manager.prompt_tile_coordinates(game)

        # TODO: Robber.

        self.played = True
