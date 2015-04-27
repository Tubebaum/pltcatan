# -*- coding: utf-8 -*-
import pdb

from engine.src.board.board import Board
from engine.src.tile.hex_tile import HexTile
from engine.src.vertex import Vertex
from engine.src.edge import Edge
from engine.src.direction.edge_direction import EdgeDirection
from engine.src.direction.vertex_direction import VertexDirection
from engine.src.direction.edge_vertex_mapping import EdgeVertexMapping


class HexBoard(Board):
    """A horizontal hextile board, such as that used in Settlers of Catan.

    Hextiles are referred to using axial coordinates.
        See below for more on axial hex coordinates.
            http://devmag.org.za/2013/08/31/geometry-with-hex-coordinates/
            www.redblobgames.com/grids/hexagons

    Attributes:
        radius (int): The number of tiles between the center tile and the edge
          of the board, including the center tile itself. Should be >= 1.

        tiles (dict): A dictionary of tiles, indexed using axial coordinates

        tile_cls (class): Class of the tiles to be generated during board
          initialization.
        
    Args:
        radius (int): The number of tiles between the center tile and the edge
          of the board, including the center tile itself. Should be >= 1.
    """

    MIN_BOARD_RADIUS = 1

    def __init__(self, radius, tile_cls=HexTile):

        if radius < HexBoard.MIN_BOARD_RADIUS:
            message = ("Specified radius does not meet the minimum board "
                       "tile radius {0}").format(HexBoard.MIN_BOARD_RADIUS)
            raise ValueError(message)

        self.radius = radius

        self.tile_cls = tile_cls

        self.tiles = {}
        self._create_tiles()

    def _create_tiles(self):
        """Generates a dictionary of tiles, indexed by axial coordinates.

        See how coordinates are generated in _add_new_tile_with_coords()

        Returns:
            None.
        """

        for x, y in self.iter_tile_coords():
            self._add_new_tile_with_coords(x, y)

        self._sync_tile_vertices_and_edges()


    def _add_new_tile_with_coords(self, x, y):
        """Add a brand new tile to the board at the given axial coordinates."""

        if x not in self.tiles:
            self.tiles[x] = {}

        tile = self.tile_cls(x, y)
        self.tiles[x][y] = tile

    def _sync_tile_vertices_and_edges(self):
        """Synchronize shared vertices and edges across tiles.

        New tile objects will create their own vertices and edges. When tiles
        share edges and vertices with existing tiles on the board, however,
        we want them to point to the same shared vertex or edge objects,
        instead of each having their own. This method enforces this for the
        given tile.
        """

        for x, y in self.iter_tile_coords():
            tile = self.get_tile_with_coords(x, y)

            for vertex_dir in VertexDirection:
                new_vertex = Vertex()
                self.update_vertex(x, y, vertex_dir, new_vertex)

            for edge_dir in EdgeDirection:
                new_edge = Edge()
                self.update_edge(x, y, edge_dir, new_edge)

    def get_tile_with_coords(self, x, y):
        """Get the tile at the given coordinates, or None if no tile exists."""

        if x in self.tiles and y in self.tiles[x]:
            return self.tiles[x][y]

        return None

    def get_vertex(self, x, y, vertex_dir):
        """Get the vertex defined by the given params."""
        tile = self.get_tile_with_coords(x, y)

        if tile:
            return tile.vertices[vertex_dir]
        else:
            return None

    def valid_tile_coords(self, x, y):
        """Return whether or not these params specify a valid tile."""

        return bool(self.get_tile_with_coords(x, y))

    def valid_vertex(self, x, y, vertex_dir):
        """Return whether or not these params specify a valid vertex."""

        return bool(self.get_vertex(x, y, vertex_dir))

    def get_neighboring_tile(self, tile, edge_direction):
        """Get the tile neighboring the given tile in the given direction.

        Args:
            tile (Tile): The tile for which we'd like to find the neighbor.

            edge_direction (EdgeDirection): Hextiles have 6 edges and thus
              neighbors in 6 different directions. Should be relative to the
              given tile.

        Returns:
            Tile. None if the tile has no valid neighbor in that direction.

        TODO: enforce that direction is actually in EdgeDirection
        """

        x = tile.x + edge_direction[0]
        y = tile.y + edge_direction[1]

        return self.get_tile_with_coords(x, y)

    def get_neighboring_tiles(self, tile):
        """Get all six neighboring tiles for the given hextile.

        Args:
            tile (Tile): The tile whose neighbors we want to return.

        Returns:
            dict. Keys are directions and values are tiles that neighbor the
              given tile in that direction.
        """

        neighboring_tiles = {}

        for direction in EdgeDirection:
            neighbor_tile = self.get_neighboring_tile(tile, direction)

            if neighbor_tile:
                neighboring_tiles[direction] = neighbor_tile

        return neighboring_tiles

    def iter_tiles(self):
        """Iterate over the tiles in this board.

        The order is that described in iter_tile_coords.

        Yields:
            Tile. Each tile of the board.
        """

        for x, y in self.iter_tile_coords():
            yield self.get_tile_with_coords(x, y)

    def iter_perimeter_tiles(self):
        """Iterate over the tiles along the outermost edge of the board."""
        for x, y in HexBoard.iter_tile_ring_coords(self.radius - 1):
            yield self.get_tile_with_coords(x, y)

    def iter_tile_coords(self):
        """Iterate over axial coordinates for each tile in the board.

        This is a generator function that will yield the coordinates to the
        caller each time after they are computed.

        We can consider a hextile board a series of concentric rings where the
        radius counts the number of concentric rings that compose the board.
        When generating coordinates, we traverse each such ring one at a time,
        using the pattern specified in iter_tile_ring_coords().

        Yields:
            tuple. The axial (x, y) coordinates of each tile on the board.
        """

        for ring_index in range(self.radius):
            for x, y in HexBoard.iter_tile_ring_coords(ring_index):
                yield x, y

    @staticmethod
    def iter_tile_ring_coords(ring_index):
        """Iterate clockwise over coordinates of the board's perimeter tiles.

        We can consider a hextile board a series of concentric rings where the
        radius counts the number of concentric rings that compose the board.
        Thus, ring_index 0 corresponds to the center tile and ring_index =
        self.radius - 1 corresponds to perimeter tiles.

        Here we generate the coordinates for all tiles of a single ring,
        designated by ring_index, traversing the ring one tile at a time,
        starting from the westernmost tile and continuing around the ring in a
        clockwise fashion.

        Args:
            ring_index (int): Defines which tile ring to iterate over.
              Should be a value between 0 and self.radius - 1.

        Yields:
            tuple. The axial (x, y) coordinates of each tile in the given ring.
        """

        # We start yielding coordinates from the westernmost tile.
        x = -1 * ring_index
        y = 0

        if x == 0 and y == 0:
            yield x, y

        # First we scale the northwest side of the ring.
        # This is equivalent to moving along the y-axis of the board.
        while y != ring_index:
            yield x, y
            y += 1

        # Then we scale the northern side of the ring.
        # This is equivalent to moving along the x-axis of the board.
        while x != 0:
            yield x, y
            x += 1

        # Then we scale the northeast side of the ring.
        # This is equivalent to moving along the z-axis of the board.
        while x != ring_index or y != 0:
            yield x, y
            x += 1
            y -= 1

        # Then we scale the southeast side of the ring.
        while y != -ring_index:
            yield x, y
            y -= 1

        # Then the south side of the ring.
        while x != 0:
            yield x, y
            x -= 1

        # And finally the south west side of the ring.
        while x != -ring_index:
            yield x, y
            x -= 1
            y += 1

    def update_edge(self, x, y, edge_dir, edge_val):
        """Update the specified edge.

        Also updates equivalent edge for neighboring tile.

        Args:
            x (int): Axial x-coordinate of the tile, one of whose vertices
              we will update.

            y (int): Axial y-coordinate of the tile, one of whose vertices
              we will update.

            edge_dir (EdgeDirection): Direction of edge to update relevant to
              tile given by x, y coordinates.

            edge_val (Structure): Value to replace old edge values.

        Returns:
            None
        """
        tile = self.get_tile_with_coords(x, y)
        vertex_dirs = EdgeVertexMapping.get_vertex_dirs_for_edge_dir(edge_dir)

        neighbor_tile = self.get_neighboring_tile(tile, edge_dir)

        tile.add_edge(vertex_dirs[0], vertex_dirs[1], edge_val)

        # Perimeter tiles will not have neighbors along certain edges.
        if neighbor_tile:
            neighbor_tile.add_edge(vertex_dirs[0], vertex_dirs[1], edge_val)

    def update_vertex(self, x, y, vertex_dir, vertex_val):
        """Update the value at the specified vertex location.

        Also updates vertex for neighboring tiles.

        Args:
            x (int): Axial x-coordinate of the tile, one of whose vertices
              we will update.

            y (int): Axial y-coordinate of the tile, one of whose vertices
              we will update.

            vertex_dir (VertexDirection): Vertex direction, relative to the
              tile specified by the x and y coordinates, of the vertex to
              update.

            vertex_val (Structure): Value to replace old vertex values.

        Returns:
            None.
        """

        tile = self.get_tile_with_coords(x, y)
        old_vertex_val = self.get_vertex(x, y, vertex_dir)

        tile.vertices[vertex_dir] = vertex_val

        # Get the two edges of the found tile that have as an endpoint
        # a vertex of the given vertex direction.
        vertex_adj_edge_dirs = EdgeVertexMapping.get_edge_dirs_for_vertex_dir(
            vertex_dir)

        for vertex_adj_edge_dir in vertex_adj_edge_dirs:
            neighbor_tile = self.get_neighboring_tile(tile, vertex_adj_edge_dir)

            # Edge tiles may not have neighboring tiles in the given direction.
            if neighbor_tile:
                neighbor_vertex_dir = HexTile.get_equivalent_vertex_dir(
                    vertex_dir, vertex_adj_edge_dir)

                neighbor_tile.update_vertex(neighbor_vertex_dir, vertex_val)

    def get_adjacent_tiles_to_vertex(self, x, y, vertex_dir):
        """Get the three tiles that converge at the specified vertex.

        Args:
            x (int): Axial x-coordinate of the tile, one of whose vertices
              we will update.

            y (int): Axial y-coordinate of the tile, one of whose vertices
              we will update.

            vertex_dir (VertexDirection): Vertex direction, relative to the
              tile specified by the x and y coordinates, of the vertex to
              find the adjacent tiles of.

        Returns:
            list of Tiles. The tiles that converge at the specified vertex.
        """

        tile = self.get_tile_with_coords(x, y)

        adjacent_tiles = map(
            lambda edge_dir: self.get_neighboring_tile(tile, edge_dir),
            EdgeVertexMapping.get_edge_dirs_for_vertex_dir(vertex_dir)
        )

        adjacent_tiles.append(tile)

        return adjacent_tiles

    def get_common_vertex_edges(self, x, y, vert_or_edge_dir):
        if vert_or_edge_dir in EdgeDirection:
            vertex_dirs = EdgeVertexMapping.get_vertex_dirs_for_edge_dir(dir)

            return self.get_adjacent_edges_to_vertex(x, y, vertex_dirs[0]) + \
                self.get_adjacent_edges_to_vertex(x, y, vertex_dirs[1])

        elif vert_or_edge_dir in VertexDirection:
            return self.get_adjacent_edges_to_vertex(x, y, vert_or_edge_dir)

    def get_adjacent_edges_to_vertex(self, x, y, vertex_dir):

        tile = self.get_tile_with_coords(x, y)

        # Get the directions of edges that both have vertex_dir as an endpoint.
        edge_dirs = EdgeVertexMapping.get_edge_dirs_for_vertex_dir(vertex_dir)

        # Get the edge values relative to the found tile using edge_dirs.
        edge_vals = map(lambda edge_dir: tile.get_edge(edge_dir), edge_dirs)

        # The last edge value won't be available via the current tile's edges,
        # but must be found on its neighbor.
        neighboring_tile = self.get_neighboring_tile(tile, edge_dirs[0])
        opp_vert_dir = HexTile.get_equivalent_vertex_dir(vertex_dir, edge_dirs[0])

        neighbor_edge_dirs = EdgeVertexMapping.get_edge_dirs_for_vertex_dir(opp_vert_dir)
        neighbor_edge_dir = next(d for d in neighbor_edge_dirs if d != edge_dirs[0])

        neighbor_edge_val = neighboring_tile.get_edge(neighbor_edge_dir)

        edge_vals.append(neighbor_edge_val)

        return edge_vals

    def get_adjacent_vertices_for_vertex(self, x, y, vertex_dir):

        tile = self.get_tile_with_coords(x, y)

        vertex_dirs = VertexDirection.get_neighboring_vertex_dirs(vertex_dir)

        vertex_vals = map(lambda v_dir: tile.get_vertex(v_dir), vertex_dirs)

        # The last vertex value won't be available via the current tile's
        # vertices, but must be found on its neighbor.

        # Get the directions of edges that both have vertex_dir as an endpoint.
        edge_dirs = EdgeVertexMapping.get_edge_dirs_for_vertex_dir(vertex_dir)

        neighboring_tile = self.get_neighboring_tile(tile, edge_dirs[0])
        opp_vert_dir = HexTile.get_equivalent_vertex_dir(vertex_dir, edge_dirs[0])

        neighbor_vertex_dirs = VertexDirection.get_neighboring_vertex_dirs(opp_vert_dir)
        neighbor_vertex_vals = filter(
            lambda v_val: v_val not in vertex_vals,
            map(lambda v_dir: neighboring_tile.get_vertex(v_dir), neighbor_vertex_dirs)
        )

        vertex_vals.extend(neighbor_vertex_vals)

        return vertex_vals
