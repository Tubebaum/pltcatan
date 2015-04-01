# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from engine.src.vertex.vertex import Vertex


class Structure(Vertex):
    """Abstract vertex structure class.

    All structures that can be built on tile corners in a Settlers of Catan
    game must implement the specified methods.

    TODO: Look into actual Python interface.
    TODO: Extension to structures.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def base_yield(self):
        """Structures sit on tile corners and yield resources of that tile.

        Returns:
            int. Number of resource cards of the same resource type of one of
              the tiles this structure sits on.
        """

        raise NotImplementedError

    @abstractmethod
    def cost(self):
        """Structures cost resources to build.

        Returns:
            tuple. Each element of the tuple is a ResourceType and count pair.
              So e.g. a city in the base Catan game should return
              ((ResourceType.ORE, 3), (ResourceType.WHEAT, 2))
        """

        raise NotImplementedError

# TODO: Programatically import and register all classes in vertex/structure
from engine.src.vertex.structure.city import City
from engine.src.vertex.structure.settlement import Settlement
Structure.register(City)
Structure.register(Settlement)