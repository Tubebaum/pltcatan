# -*- coding: utf-8 -*-
from engine.src.card.development_card.progress_card.progress_card \
    import ProgressCard


class YearOfPlentyCard(ProgressCard):

    DEFAULT_RESOURCE_COUNT = 2

    def __init__(self):
        super(YearOfPlentyCard, self).__init__()

    def effect_when_played(self, game, player):
        """Allow player to take 2 cards of their chosen resource type."""

        game.input_manager.announce_development_card_played(player, self)
        resource_type = game.input_manager.prompt_select_resource_type()

        game.board.bank.transfer_resources(
            player, resource_type, YearOfPlentyCard.DEFAULT_RESOURCE_COUNT)

        self.played = True

