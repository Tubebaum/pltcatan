# -*- coding: utf-8 -*-
from engine.src.config.config import Config
from engine.src.lib.utils import Utils


class DevelopmentCard(object):
    """
    Attributes:
        From Config:
            count (int)
            name (str)
            description (str)
            draw_card (func)
            play_card (func)
            cost (int)

        played (bool)
        is_playable (bool)
    """

    def __init__(self, **kwargs):

        # Initialize default values.
        Config.init_from_config(self, 'game.card.development.default')

        # Overwrite default values with custom values.
        Utils.init_from_dict(self, kwargs)

        self.played = False
        self.is_playable = True

    def __str__(self):
        return self.name
        
    def draw_card(self, game, player):
        """Draw this card and activate any effect incurred by holding it.
         
         This method should be called only once when purchased by a player.
         
        Args:
            game (Game): The game this card may possibly affect.
            
            player(Player): The player that bought this development card.
        
        Returns:
            None. Should call functions on game and player.
        """
        pass

    def play_card(self, game, player):
        """Draw this card and activate any relevant effect.
         
         This method should be called only once when played by a player.
         
        Args:
            game (Game): The game this card may possibly affect.
            
            player(Player): The player that played this development card.
        
        Returns:
            None. Should call functions on game and player.
        """

        self.played = True
