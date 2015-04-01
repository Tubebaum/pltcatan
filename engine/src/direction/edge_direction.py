# -*- coding: utf-8 -*-
from .direction import Direction
from .vertex_direction import VertexDirection


class EdgeDirection(Direction):
    """The 6 directions of a hexagon's edges with axial coordinates.

    Each edge direction is a direction we can follow from the center of a
    hextile to a point on one of its edges.

    Since each edge in a tile borders another tile, each edge direction
    also corresponds to a unit vector that we can follow from a given
    point in a hex axial coordinate system to get to another tile.

    See more on axial coordinates here:
        http://www.redblobgames.com/grids/hexagons/#coordinates
    """

    NORTH_WEST = (-1, 1, 0)
    NORTH_EAST = (0, 1, -1)
    WEST = (-1, 0, 1)
    EAST = (1, 0, -1)
    SOUTH_WEST = (0, -1, 1)
    SOUTH_EAST = (1, -1, 0)

    def get_opposite_direction(self):
        """Get the direction of the opposite edge."""

        coordinates = self.value

        x = -coordinates[0]
        y = -coordinates[1]
        z = -(x + y)

        return EdgeDirection.find_by_value((x, y, z))

    def get_vertex_directions(self):
        """Get the vertex directions of endpoints of edge of this direction.

        Returns:
            tuple. A tuple of 2 tuples, each of which is a value in
              VertexDirection that represents the endpoints of this edge.
        """

        edge_vertex_mapping = {
            EdgeDirection.NORTH_WEST:
                (VertexDirection.TOP_LEFT, VertexDirection.TOP),
            EdgeDirection.NORTH_EAST:
                (VertexDirection.TOP, VertexDirection.TOP_RIGHT),
            EdgeDirection.WEST:
                (VertexDirection.TOP_RIGHT, VertexDirection.BOTTOM_RIGHT),
            EdgeDirection.SOUTH_WEST:
                (VertexDirection.BOTTOM_RIGHT, VertexDirection.BOTTOM),
            EdgeDirection.SOUTH_EAST:
                (VertexDirection.BOTTOM, VertexDirection.BOTTOM_LEFT),
            EdgeDirection.EAST:
                (VertexDirection.BOTTOM_LEFT, VertexDirection.TOP_LEFT)
        }

        return edge_vertex_mapping[self]

