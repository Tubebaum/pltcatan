def draw_card(self, game, player):
    pass


def play_card(self, game, player):
    """Allow player to take all carried cards of selected resource type."""

    game.input_manager.announce_development_card_played(player, self)

    for _ in range(2):
        x, y, edge_dir = game.input_manager.prompt_edge_placement(game)
        game.board.place_edge_structure(x, y, edge_dir,
                                        player.get_structure('road'))

    self.played = True
