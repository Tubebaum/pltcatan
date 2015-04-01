# -*- coding: utf-8 -*-
from engine.src.direction.edge_direction import EdgeDirection
from engine.src.direction.vertex_direction import VertexDirection


class EdgeVertexMapping(object):

    @classmethod
    def get_edge_dirs_for_vertex_dir(cls, vertex_dir):
        """Returns directions of edges that share this vertex direction.

        E.g. VertexDirection.TOP is the direction of the vertex that is an
        endpoint of both EdgeDirection.NORTH_WEST and EdgeDirection.NORTH_EAST.

        Returns:
            tuple. A tuple of two directions, each of which has this vertex as
              an endpoint.
        """

        vertex_edge_mapping = {
            VertexDirection.TOP:
                (EdgeDirection.NORTH_WEST, EdgeDirection.NORTH_EAST),
            VertexDirection.TOP_RIGHT:
                (EdgeDirection.NORTH_EAST, EdgeDirection.EAST),
            VertexDirection.BOTTOM_RIGHT:
                (EdgeDirection.EAST, EdgeDirection.SOUTH_EAST),
            VertexDirection.BOTTOM:
                (EdgeDirection.SOUTH_EAST, EdgeDirection.SOUTH_WEST),
            VertexDirection.BOTTOM_LEFT:
                (EdgeDirection.SOUTH_WEST, EdgeDirection.WEST),
            VertexDirection.TOP_LEFT:
                (EdgeDirection.WEST, EdgeDirection.NORTH_WEST)
        }

        return vertex_edge_mapping[vertex_dir]

    @classmethod
    def get_vertex_dirs_for_edge_dir(cls, edge_dir):
        """Get the vertex directions of endpoints of the given edge.

        Returns:
            tuple. A tuple of 2 tuples, each of which is a value in
              VertexDirection that represents the endpoints of the given edge.
        """

        edge_vertex_mapping = {
            EdgeDirection.NORTH_WEST:
                (VertexDirection.TOP_LEFT, VertexDirection.TOP),
            EdgeDirection.NORTH_EAST:
                (VertexDirection.TOP, VertexDirection.TOP_RIGHT),
            EdgeDirection.EAST:
                (VertexDirection.TOP_RIGHT, VertexDirection.BOTTOM_RIGHT),
            EdgeDirection.SOUTH_EAST:
                (VertexDirection.BOTTOM_RIGHT, VertexDirection.BOTTOM),
            EdgeDirection.SOUTH_WEST:
                (VertexDirection.BOTTOM, VertexDirection.BOTTOM_LEFT),
            EdgeDirection.WEST:
                (VertexDirection.BOTTOM_LEFT, VertexDirection.TOP_LEFT)
        }

        return edge_vertex_mapping[edge_dir]
