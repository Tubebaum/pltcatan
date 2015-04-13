# -*- coding: utf-8 -*-
from engine.src.calamity.calamity import Calamity
from engine.src.calamity.calamity import CalamityTilePlacementEffect


class Robber(Calamity):

    MIN_ROBBER_ACTIVATING_RESOURCE_COUNT_THRESHOLD = 8

    def __init__(self):
        # TODO: Not sure if this is the best way to represent these effects.
        self.tile_placement_effect = CalamityTilePlacementEffect.BLOCK_YIELD

    def roll_value(self):
        # TODO: Move to config?
        return 7

    def trigger_effect(self, game, player):
        """Halve players resources, move the robber, draw a resource card.

        Triggering the robber effect elicits the following behavior:
            (1) All players who have more than some threshold of resource cards
                must discard half of their resource hand, floored.
            (2) See self.outside_trigger_effect().

        Args:
            See Calamity.
        """

        threshold = Robber.MIN_ROBBER_ACTIVATING_RESOURCE_COUNT_THRESHOLD

        # Have players discard half their hand if they have too many cards.
        for game_player in game.players:

            resource_count = game_player.count_resources()

            if resource_count > threshold:
                cards_to_discard = int(resource_count / 2)
                resources = game_player.get_resource_list()

                resource_indices = game.input_manager.prompt_discard_resources(
                    game, player, resources, cards_to_discard)

                for index in resource_indices:
                    game_player.withdraw_resources(resources[index], 1)

        self.outside_trigger_effect(game, player)

    def outside_trigger_effect(self, game, player):
        """When the robber is activated not by a dice roll, call this method.

        Execute the following behavior:
            (1) The robber should be moved to a different tile.
            (2) A resource card must be drawn from one of the players with
                structures built adjacent to the tile.
        """

        robber_successfully_moved = True
        previous_tile = game.board.find_tile_with_calamity(self)
        previous_tile.remove_calamity(self)

        while not robber_successfully_moved:
            x, y = game.input_manager.prompt_tile_coordinates(game)

            # Move robber to new tile.
            tile = game.board.get_tile_with_coords(x, y)

            if tile != previous_tile:
                tile.add_calamity(self)
                robber_successfully_moved = True

        # Draw card from player that has a structure built adjacent to the tile.
        # The player can not draw from herself or from a player with no cards.
        eligible_players = filter(
            lambda owning_player:
                owning_player != player and
                owning_player.count_resources() != 0,
            map(lambda structure: structure.owning_player,
                tile.get_adjacent_vertex_structures())
        )

        if eligible_players:

            chosen_player = game.input_manager.prompt_select_player(
                game, eligible_players)

            resource_type = chosen_player.withdraw_random_resource()
            player.deposit_resources(resource_type, 1)

        # TODO: else announce to player
