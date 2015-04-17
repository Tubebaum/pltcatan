def draw_card(self, game, player):
    pass


def play_card(self, game, player):
    """Allow player to take 2 cards of their chosen resource type."""

    game.input_manager.announce_development_card_played(player, self)
    resource_type = game.input_manager.prompt_select_resource_type()

    game.board.bank.transfer_resources(player, resource_type, 2)

    self.played = True
