# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from engine.src.resource_type import ResourceType


class DevelopmentCard(object):
    __metaclass__ = ABCMeta

    def __init__(self):

        self.cost = {ResourceType.GRAIN: 1, ResourceType.ORE: 1,
                     ResourceType.WOOL: 1}

        self.played = False
        self.is_playable = True
        
    @abstractmethod
    def effect_when_held(self, game, player):
        """Activates effect of holding the current card.
         
         This method should be called only once when purchased by a player.
         
        Args:
            game (Game): The game this card may possibly affect.
            
            player(Player): The player that bought this development card.
        
        Returns:
            None. Should call functions on game and player.
        """
        pass

    @abstractmethod
    def effect_when_played(self, game, player):
        """Activates effect of playing the current card.
         
         This method should be called only once when played by a player.
         
        Args:
            game (Game): The game this card may possibly affect.
            
            player(Player): The player that played this development card.
        
        Returns:
            None. Should call functions on game and player.
        """

        self.played = True

