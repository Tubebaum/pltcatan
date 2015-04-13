# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod, abstractproperty
from engine.src.card.development_card.development_card import DevelopmentCard


class ProgressCard(DevelopmentCard):
    __metaclass__ = ABCMeta

    def is_playable(self):
        return True

    def effect_when_held(self, game, player):
        # Progress cards have no effect when held.
        pass

    @abstractmethod
    def effect_when_played(self, game, player):
        pass
