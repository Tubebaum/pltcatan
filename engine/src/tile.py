# -*- coding: utf-8 -*-

from enum import Enum
from vertex import Vertex
from edge import Edge


class Tile(object):
    """A hexagonal tile, with 6 edges and 6 vertices.

    Attributes:
        vertices: A dictionary indexed by VertexDirection of the vertices of
          this tile.
        edges: A dictionary of the edges of this tile, indexed by a pair of
          vertices.
          Note that edges are undirected so edges[src][dst] = edges[dst][src].

    Args:
        x: The x-coordinate of this tile in the axial coordinate system used
          by the board to which this tile belongs.

        y: The y-coordinate of this tile in the axial coordinate system used
          by the board to which this tile belongs.

    TODO: x and y are mostly here for testing purposes.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.vertices = {}
        self.edges = {}
        self._create_vertices_and_edges()

    # FIXME: doesn't connect last and first edges
    # TODO: consider getting vertices by their directions, not object pointers
    def _create_vertices_and_edges(self):
        """Create brand new vertices and edges for this tile."""

        self.vertices = {}
        self.edges = {}

        # Keep track of the start/end vertices for when we create a new edge.
        start_vertex = end_vertex = None

        for direction in VertexDirection:

            # Create a new vertex in the given direction.
            end_vertex = Vertex()
            self.vertices[direction] = end_vertex

            # If we have a start vertex as well, create a new edge.
            if start_vertex is not None:
                self.add_edge(start_vertex, end_vertex, Edge())

            # Our current end_vertex will be our start_vertex for the next edge.
            start_vertex = end_vertex

    def add_edge(self, start_vertex, end_vertex, edge):
        """Add an edge to this tile connecting these two vertices.

        Since edges aren't directed, edges[src][dst] = edges[dst][src].

        TODO: enforce that these are adjacent vertices.
        """

        self.edges[start_vertex][end_vertex] = edge
        self.edges[end_vertex][start_vertex] = edge

    def update_edge_and_vertex_pair(self, start_vertex_direction,
                                    end_vertex_direction, start_vertex,
                                    end_vertex, edge):
        """Update the given pair of vertices and the edge that connects them.

        Replace the vertex at the given direction in self.vertices, and
        update the edge entry for those vertices in self.edges
        """

        self.vertices[start_vertex_direction] = start_vertex
        self.vertices[end_vertex_direction] = end_vertex

        self.add_edge(start_vertex, end_vertex, edge)

    def __repr__(self):
        return "({0}, {1})".format(self.x, self.y)


"""EdgeDirection 'enum'.

Each edge direction is a direction we can follow from the center of a
hextile to a point on one of its edges.

Since each edge in a tile borders another tile, each edge direction
also corresponds to a unit vector that we can follow from a given
point in a hex axial coordinate system to get to another tile.
"""
EdgeDirection = Enum({
    'NORTH_WEST': (-1, 1, 0),
    'NORTH_EAST': (0, 1, -1),
    'WEST': (-1, 0, 1),
    'EAST': (1, 0, -1),
    'SOUTH_WEST': (0, -1, 1),
    'SOUTH_EAST': (1, -1, 0)
})

"""VertexDirection 'enum'.

Each vertex direction is a direction we can follow from the center of a
tile to one of its vertexes.

TODO: I think these might be related to cube coordinates.
"""
VertexDirection = Enum({
    'TOP': (0, 1),
    'TOP_RIGHT': (1, 1),
    'BOTTOM_RIGHT': (1, -1),
    'BOTTOM': (0, -1),
    'BOTTOM_LEFT': (-1, -1),
    'TOP_LEFT': (-1, 1)
})

