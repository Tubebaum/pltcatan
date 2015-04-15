# -*- coding: utf-8 -*-
from engine.src.card.development_card.progress_card.progress_card \
    import ProgressCard
from engine.src.structure.edge_structure.road import Road


class RoadBuildingCard(ProgressCard):

    DEFAULT_ROAD_COUNT = 2

    def __init__(self):
        super(RoadBuildingCard, self).__init__()

    def play_card(self, game, player):
        """Allow player to take all carried cards of selected resource type."""

        game.input_manager.announce_development_card_played(player, self)

        for _ in range(RoadBuildingCard.DEFAULT_ROAD_COUNT):
            x, y, edge_dir = game.input_manager.prompt_edge_placement(game)
            game.board.place_edge_structure(x, y, edge_dir,
                                            player.get_structure(Road))

        self.played = True
