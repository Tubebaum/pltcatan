# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from engine.src.card.development_card.development_card import DevelopmentCard


class ProgressCard(DevelopmentCard):
    __metaclass__ = ABCMeta

    def __init__(self):
        super(ProgressCard, self).__init__()

    def draw_card(self, game, player):
        # Progress cards have no effect when drawn/held.
        pass

    @abstractmethod
    def play_card(self, game, player):
        pass
