import pdb
from engine.src.lib.utils import Utils
from engine.src.direction.edge_direction import EdgeDirection
from engine.src.direction.edge_vertex_mapping import EdgeVertexMapping
from engine.src.structure.structure import Structure
from engine.src.tile.hex_tile import HexTile


vertices = Utils.nested_dict()
edges = Utils.nested_dict()


def find_edge_meta(board, x, y, edge_dir):
    edge = edges[x][y][edge_dir]

    if not edge:
        tile = board.get_tile_with_coords(x, y)
        if tile:
            edge = EdgeMeta(board, x, y, edge_dir)
        else:
            edge = None

    return edge


def find_vertex_meta(board, x, y, vertex_dir):
    vertex = vertices[x][y][vertex_dir]

    if not vertex:
        tile = board.get_tile_with_coords(x, y)
        if tile:
            vertex = VertexMeta(board, x, y, vertex_dir)
        else:
            vertex = None

    return vertex


class VertexMeta(object):

    def __init__(self, board, x, y, vertex_dir):

        vertices[x][y][vertex_dir] = self

        self.board = board

        self.x = x
        self.y = y
        self.tile = self.board.get_tile_with_coords(self.x, self.y)

        self.vertex_dir = vertex_dir

        self.neighbors = []

        self.neighbors = self.find_neighbor_equivalents()

    def find_neighbor_equivalents(self):

        neighbors = []

        # Get the two edges of the found tile that have as an endpoint
        # a vertex of the given vertex direction.
        vertex_adj_edge_dirs = EdgeVertexMapping.get_edge_dirs_for_vertex_dir(
            self.vertex_dir)

        for vertex_adj_edge_dir in vertex_adj_edge_dirs:
            neighbor_x = self.tile.x + vertex_adj_edge_dir[0]
            neighbor_y = self.tile.y + vertex_adj_edge_dir[1]
            neighbor_tile = self.board.get_neighboring_tile(self.tile, vertex_adj_edge_dir)

            # Edge tiles may not have neighboring tiles in the given direction.
            if neighbor_tile:
                neighbor_vertex_dir = HexTile.get_equivalent_vertex_dir(
                    self.vertex_dir, vertex_adj_edge_dir)

                neighbor = find_vertex_meta(self.board, neighbor_x, neighbor_y, neighbor_vertex_dir)

                neighbors.append(neighbor)

        return neighbors

    def __str__(self):
        return '({}, {}) {}'.format(self.x, self.y, self.vertex_dir)

    def __eq__(self, other):

        matches = self.x == other.x and \
                  self.y == other.y and \
                  self.vertex_dir == other.vertex_dir

        for neighbor in self.neighbors:
            matches = matches or \
                      neighbor.x == other.x and \
                      neighbor.y == other.y and \
                      neighbor.vertex_dir == other.vertex_dir

        return matches


class EdgeMeta(object):

    def __init__(self, board, x, y, edge_dir):

        edges[x][y][edge_dir] = self


        self.board = board

        self.x = x
        self.y = y
        self.tile = self.board.get_tile_with_coords(self.x, self.y)

        self.edge_dir = edge_dir
        self.edge_val = self.tile.get_edge(self.edge_dir)

        # Neighbor equivalent edge meta of same edge.
        self.neighbor = self.find_neighbor()

    def find_neighbor(self):

        neighbor_x = self.tile.x + self.edge_dir[0]
        neighbor_y = self.tile.y + self.edge_dir[1]
        neighbor_edge_dir = self.edge_dir.get_opposite_direction()

        return find_edge_meta(self.board, neighbor_x, neighbor_y, neighbor_edge_dir)

    def __str__(self):
        return '({}, {}) {}'.format(self.x, self.y, self.edge_dir)

    def __eq__(self, other):

        matches_this = self.x == other.x and \
                       self.y == other.y and \
                       self.edge_dir == other.edge_dir

        matches_neighbor = self.neighbor.x == other.x and \
                           self.neighbor.y == other.y and \
                           self.neighbor.edge_dir == other.edge_dir

        return matches_this or matches_neighbor


class LongestRoadSearch(object):

    def __init__(self, board):
        self.board = board

    def execute(self):

        player_claimed_edges_dict = self.find_per_player_claimed_edges()
        player_road_len_dict = self.find_per_player_max_road_lengths(player_claimed_edges_dict)

        return player_road_len_dict

    def find_per_player_claimed_edges(self):

        player_claimed_edges_dict = Utils.nested_dict()
        checked_edges = Utils.nested_dict()

        for x, y in self.board.iter_tile_coords():
            for edge_dir in EdgeDirection:
                if not checked_edges[x][y][edge_dir]:
                    self.add_edge_to_dicts(x, y, edge_dir, player_claimed_edges_dict, checked_edges)

        return player_claimed_edges_dict

    def add_edge_to_dicts(self, x, y, edge_dir, player_claimed_edges_dict, checked_edges):

        edge_meta = find_edge_meta(self.board, x, y, edge_dir)

        if not edge_meta:
            checked_edges[x][y][edge_dir] = True
            return

        checked_edges[edge_meta.x][edge_meta.y][edge_meta.edge_dir] = True
        if edge_meta.neighbor:
            checked_edges[edge_meta.neighbor.x][edge_meta.neighbor.y][edge_meta.neighbor.edge_dir] = True

        if isinstance(edge_meta.edge_val, Structure):
            player = edge_meta.edge_val.owning_player

            if not player_claimed_edges_dict[player]:
                player_claimed_edges_dict[player] = []

            player_claimed_edges_dict[player].append(edge_meta)
            # player_claimed_edges_dict[player].append(edge_meta.neighbor)

    def find_per_player_max_road_lengths(self, player_claimed_edges_dict):

        player_road_len_dict = {}

        for player, player_claimed_edges in player_claimed_edges_dict.iteritems():
            player_road_len_dict[player] = self.find_max_road_len(player_claimed_edges)

        return player_road_len_dict

    def find_max_road_len(self, player_claimed_edges):
        """
        Args:
            player_claimed_edges (list): List of EdgeMetas.
        """

        max_road_len = 0

        for edge_meta in player_claimed_edges:
            edge_dir = edge_meta.edge_dir

            vertex_dirs = EdgeVertexMapping.get_vertex_dirs_for_edge_dir(edge_dir)

            remaining_edges = [e for e in player_claimed_edges if e != edge_meta]

            start_vertex = find_vertex_meta(self.board, edge_meta.x, edge_meta.y, vertex_dirs[0])
            end_vertex = find_vertex_meta(self.board, edge_meta.x, edge_meta.y, vertex_dirs[1])

            road_len = 1 + self.find_max_path_len(remaining_edges, end_vertex, edge_meta) \
                         + self.find_max_path_len(remaining_edges, start_vertex, edge_meta)

            if road_len > max_road_len:
                max_road_len = road_len

        return max_road_len

    # TODO
    def find_max_path_len(self, remaining_edges, end_vertex, edge_meta):

        neighbor_edge_metas = map(
            lambda edge_tuple: find_edge_meta(self.board, *edge_tuple),
            self.board.get_adjacent_edges(edge_meta.x, edge_meta.y, end_vertex.vertex_dir, False)
        )

        claimed_neighbors = [i for i in neighbor_edge_metas if i in remaining_edges]

        # msg = '{} has claimed neighbors: \n'.format(edge_meta)
        # for claimed_neighbor in claimed_neighbors:
        #     msg += '\t{}\n'.format(claimed_neighbor)
        #
        # print msg

        if claimed_neighbors:
            max_path_len = 0

            for claimed_neighbor in claimed_neighbors:
                remaining_edge_metas = [x for x in remaining_edges if (x != claimed_neighbor and x != edge_meta)]

                vertices = EdgeVertexMapping.get_vertex_dirs_for_edge_dir(claimed_neighbor.edge_dir)

                vertex_metas = map(
                    lambda vertex_dir: find_vertex_meta(self.board, claimed_neighbor.x, claimed_neighbor.y, vertex_dir),
                    vertices
                )

                next_end_vertex = next(d for d in vertex_metas if d != end_vertex)

                # print 'claimed_neighbor: {}'.format(claimed_neighbor)
                # print 'remaining_edge_metas {}'.format(remaining_edge_metas)
                # print 'next_end_vertex {}'.format(next_end_vertex)
                #
                # pdb.set_trace()

                path_len = 1 + self.find_max_path_len(remaining_edge_metas, next_end_vertex, claimed_neighbor)

                if path_len > max_path_len:
                    max_path_len = path_len

            return max_path_len
        else:
            return 0
