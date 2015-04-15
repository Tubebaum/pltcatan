# -*- coding: utf-8 -*-
from engine.src.structure.augmenting_structure import AugmentingStructure


class UpgradeStructure(AugmentingStructure):
    """Represents a board structure that is an upgrade of another structure.

    An upgrade structure completely replaces the structure it upgraded.
    """

    def __init__(self, owning_player, base_structure_cls):
        super(UpgradeStructure, self).__init__(owning_player,
                                               base_structure_cls)
