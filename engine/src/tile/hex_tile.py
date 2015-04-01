# -*- coding: utf-8 -*-

from .tile import Tile
from engine.src.vertex.vertex import Vertex
from engine.src.edge.edge import Edge
from engine.src.direction.vertex_direction import VertexDirection
from engine.src.direction.edge_vertex_mapping import EdgeVertexMapping


class HexTile(Tile):
    """A hexagonal tile, with 6 edges and 6 vertices.

    Attributes:
        vertices (dict): The 6 vertices of this tile, indexed by the
          VertexDirection of the vertex i.e. the tuple of the direction,
          not its string name.

        edges (dict): The edges of this tile, indexed by a pair of vertex
          directions.
          Note that edges are undirected so edges[src][dst] = edges[dst][src].

    Args:
        x (int): The x-coordinate of this tile in the axial coordinate system
          used by the board to which this tile belongs.

        y (int): The y-coordinate of this tile in the axial coordinate system
          used by the board to which this tile belongs.

    TODO: x and y are mostly here for testing purposes. Removable.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.vertices = {}
        self.edges = {}
        self._create_vertices_and_edges()

    def __repr__(self):
        return "({0}, {1})".format(self.x, self.y)

    def _create_vertices_and_edges(self):
        """Create brand new vertices and edges for this tile."""

        self.vertices = {}
        self.edges = {}

        for (start_vertex_dir, end_vertex_dir) in VertexDirection.pairs():

            end_vertex = Vertex()
            self.vertices[end_vertex_dir] = end_vertex

            self.add_edge(start_vertex_dir, end_vertex_dir)

    def add_edge(self, start_vertex_dir, end_vertex_dir, edge=Edge()):
        """Add an edge connecting vertices at given directions to this tile.

        Since edges aren't directed, edges[src][dst] = edges[dst][src].

        Args:
            start_vertex_dir (VertexDirection): Direction relative to
              this tile to the vertex that comprises one end of the edge to add.

            end_vertex_dir (VertexDirection): Direction relative to
              this tile of the edge-to-add's endpoint vertex.

        Returns:
            None.

        TODO: enforce that these are adjacent vertex directions.
        """

        if start_vertex_dir not in self.edges:
            self.edges[start_vertex_dir] = {}

        if end_vertex_dir not in self.edges:
            self.edges[end_vertex_dir] = {}

        self.edges[start_vertex_dir][end_vertex_dir] = edge
        self.edges[end_vertex_dir][start_vertex_dir] = edge

    def update_common_edge_and_vertices(self, edge_direction,
                                        neighboring_tile):
        """Update vertices and edges this tile shares with the neighboring tile.

        Args:
            edge_direction (EdgeDirection): The given neighboring tile
              should share an edge at the given direction relative to this tile.

            neighboring_tile (Tile): The tile whose relevant vertices and
              edges we should use to overwrite those of this tile.

        Returns:
            None.
        """
        # Get the directions of the vertices comprising the endpoints of the
        # edge in the given edge_direction i.e. the edge shared between this
        # tile and the neighbor tile.
        start_vertex_dir, end_vertex_dir = \
            EdgeVertexMapping.get_vertex_dirs_for_edge_dir(edge_direction)

        # Get the symmetric directions for the neighbor tile.
        neighbor_start_vertex_dir, neighbor_end_vertex_dir = \
            EdgeVertexMapping.get_vertex_dirs_for_edge_dir(
                edge_direction.get_opposite_direction())

        # Get the vertices belonging to the neighboring tile at the found
        # directions.
        start_vertex = neighboring_tile.vertices[neighbor_start_vertex_dir]
        end_vertex = neighboring_tile.vertices[neighbor_end_vertex_dir]

        # Replace this tile's vertices with the neighbor's vertices.
        self.vertices[start_vertex_dir] = start_vertex
        self.vertices[end_vertex_dir] = end_vertex

        # print "Given tile: {0}\nEdges: {1}\n".format(self, self.edges)
        # print "Neighbor tile: {0}\nEdges: {1}\n".format(
        #     neighboring_tile, neighboring_tile.edges)

        # Replace this tile's edge with the neighbor's edge.
        self.add_edge(start_vertex_dir, end_vertex_dir,
                      neighboring_tile.edges[start_vertex_dir][end_vertex_dir])

    def iter_edges(self):
        """Iterate over the edges of this tile."""

        for (start_vertex_dir, end_vertex_dir) in VertexDirection.pairs():
            yield self.vertices[start_vertex_dir][end_vertex_dir]

    def iter_vertices(self):
        """Iterate over the vertices of this tile."""

        for vertex_direction in VertexDirection:
            yield self.vertices[vertex_direction]

    def update_vertex(self, vertex_direction, vertex_value):
        """Update the vertex defined by the given vertex direction."""

        self.vertices[vertex_direction] = vertex_value

    @classmethod
    def get_opposite_vertex_dir(cls, vertex_dir, edge_dir):
        """Get the direction of the vertex opposite to the one given.

        Consider two adjacent tiles, one of which we will think of as the
        base_tile, relative to which vertex_dir and edge_dir are defined,
        and its neighboring adj_tile. If we know the direction of a vertex
        relative to base_tile, and we want to find the direction to the same
        vertex relative to adj_tile, we should use this method.

        Args:
            vertex_dir (VertexDirection): See above.

            edge_dir (EdgeDirection): Edge direction of the shared edge,
              relative to the given tile, of the edge shared by base_tile and
              adj_tile, as described above.

        Returns
            VertexDirection.
        """

        opposite_edge_vertices = \
            EdgeVertexMapping.get_vertex_dirs_for_edge_dir(
                edge_dir.get_opposite_direction())

        vertex = next(vertex for vertex in opposite_edge_vertices if
                      vertex != vertex_dir.get_opposite_direction())

        return vertex
