# -*- coding: utf-8 -*-
from engine.src.card.development_card.development_card import DevelopmentCard


class KnightCard(DevelopmentCard):

    def __init__(self):
        super(KnightCard, self).__init__()

    def draw_card(self, game, player):
        # No effect when drawn/held.
        pass

    def play_card(self, game, player):
        """Move the robber and draw a card from another adjacent player."""

        game.input_manager.announce_development_card_played(player, self)

        robber = game.board.find_robber()

        robber.outside_trigger_effect(game, player)

        player.knights += 1

        self.played = True
