def draw_card(self, game, player):
    pass


def play_card(self, game, player):
    """Allow player to take all carried cards of selected resource type."""

    game.input_manager.announce_development_card_played(player, self)
    resource_type = game.input_manager.prompt_select_resource_type()

    for game_player in game.players:
        if player != game_player:
            count = player.resources[resource_type]

            game_player.transfer_resources(player, resource_type, count)

            msg = '{0} received {1} {2} from {3}'.format(
                player.name, count, resource_type, game_player.name)

            game.input_manager.input_default(msg, None, False)

    # Announce finished collecting resources.
    msg = 'Done monopolizing resources.'
    game.input_manager.input_default(msg, None, False)

    self.played = True
