# -*- coding: utf-8 -*-
from engine.src.structure.structure import Structure
from engine.src.edge import Edge


class Road(Structure, Edge):

    def __init__(self, owning_player):
        super(Road, self).__init__(owning_player)
        self.point_worth = 0
