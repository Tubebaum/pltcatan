# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod, abstractproperty
from enum import Enum


class Calamity(object):
    """
    TODO: Consider breaking Calamity subclasses based on their latent effect,
          i.e. when not rolled, but on the board. So robbers block tile yield.
          Other calamities might block structure construction.
    """
    __metaclass__ = ABCMeta

    DEFAULT_ROLL_VALUES = [7]

    @abstractproperty
    def roll_value(self):
        """The dice roll value that should trigger this calamity's effect."""
        pass

    @abstractmethod
    def trigger_effect(self, game, player):
        """Activates this calamity's effect.

        Args:
            game (Game): The game this calamity will affect.

            player (Player): Player who rolled the triggering roll.
        """
        pass


class CalamityTilePlacementEffect(Enum):
    BLOCK_YIELD = 1
