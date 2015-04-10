# -*- coding: utf-8 -*-
from engine.src.structure.structure import Structure
from engine.src.edge import Edge


class Road(Structure, Edge):

    def __init__(self, owning_player):
        self.owning_player = owning_player
