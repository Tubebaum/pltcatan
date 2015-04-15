# -*- coding: utf-8 -*-
from engine.src.card.development_card.development_card import DevelopmentCard


class VictoryPointCard(DevelopmentCard):

    def __init__(self):
        super(VictoryPointCard, self).__init__()
    
    def draw_card(self, game, player):
        player.hidden_points += 1

    def play_card(self, game, player):
        player.hidden_points -= 1
        player.points += 1
