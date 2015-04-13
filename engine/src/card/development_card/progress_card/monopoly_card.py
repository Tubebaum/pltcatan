# -*- coding: utf-8 -*-
from engine.src.card.development_card.development_card import DevelopmentCard
from engine.src.card.development_card.progress_card.progress_card import ProgressCard


class MonopolyCard(ProgressCard):

    def __init__(self):
        self.played = False

    def effect_when_played(self, game, player):
        """Allow player to take all carried cards of selected resource type."""

        game.input_manager.announce_development_card_played(player, self)
        resource_type = game.input_manager.prompt_select_resource_type()

        for game_player in game.players:
            if player != game_player:
                game_player.transfer_resources(player, resource_type,
                                               player.resources[resource_type])

        self.played = True
