# -*- coding: utf-8 -*-
from engine.src.config.config import Config
from engine.src.lib.utils import Utils

class Structure(object):
    """
    Attributes:
        owning_player
        name
        cost
        point_value
        extends
        upgrades
    """

    def __init__(self, owning_player, **kwargs):

        # Initialize default values.
        Config.init_from_config(self, 'structure.player_built.default')

        # Overwrite default values with custom values.
        Utils.init_from_dict(self, kwargs)

        self.owning_player = owning_player

    def augments(self):
        if self.is_augmenting_structure():
            return self.upgrades if self.upgrades else self.extends
        return None

    def is_augmenting_structure(self):
        return self.extends or self.upgrades

    def __str__(self):
        return '{} owned by {}'.format(self.name, self.owning_player)
