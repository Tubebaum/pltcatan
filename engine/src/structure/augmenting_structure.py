# -*- coding: utf-8 -*-
from engine.src.structure.structure import Structure


class AugmentingStructure(Structure):
    """Represents a board structure that augments another structure in some way.

    Attributes:
        base_structure_cls (class): The class of structure this structure
          augments; should inherit the Structure class.

    Args:
        base_structure_cls (class): See above.
    """

    def __init__(self, base_structure_cls):
        self.base_structure_cls = base_structure_cls


