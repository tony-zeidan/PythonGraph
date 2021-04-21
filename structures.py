from typing import List, Dict
from shapely.geometry import Point
import pandas as pd
from util import dist_to_spherical
import os
import sys
from pathlib import Path


class GraphNode:
    """An implementation of a graph node.
    """

    def __init__(self, label='', **kwargs):
        self.label = label
        self.contains = kwargs
        self.heuristic = 0

    def __str__(self):
        return f'Node ({self.label}, {self.contains})'


class Graph:
    """A Graph implementation.
    """

    def __init__(self):
        self._node_len = 0
        self._nodes = []
        self._edges = []

    def add_vertex(self, v: GraphNode):
        """Adds a vertex to the graph

        :param v: The vertex to add
        :type v: GraphNode
        """
        if v in self._nodes:
            raise AttributeError()

        for i in range(self._node_len):
            self._edges[i].append(0)

        self._node_len += 1
        self._nodes.append(v)

        self._edges.append([0 for _ in range(self._node_len)])

    def add_edge(self, v1, v2, e: float = 1, directional=False):
        """Adds an edge to the graph.

        :param v1: The first vertex
        :type v1: GraphNode
        :param v2: The second vertex
        :type v2: GraphNode
        :param e: The edge weight
        :type e: float
        :param directional: Whether this edge is directional or not  
        :type directional: bool
        """
        vertices = self._nodes
        index1 = vertices.index(v1)
        index2 = vertices.index(v2)

        self._edges[index1][index2] = e
        if not directional:
            self._edges[index2][index1] = e

    def get_vertex(self, index: int) -> GraphNode:
        """Retrieves a vertex from the graph with the given index.

        :param index: The position of this node in the graph
        :type index: int
        :return: The node at the specified location
        :rtype: GraphNode
        """
        return self._nodes[index]

    def get_adj_list(self) -> Dict[GraphNode, List[float]]:
        """Gets an adjacency list form of the graph.

        :return: An adjacency list
        :rtype: Dict[GraphNode, List[float]]
        """
        adj_list = {}
        for i in range(self._node_len):
            adj_list[self._nodes[i]] = self._edges[i]
        return adj_list

    def __str__(self):
        adj_list = self.get_adj_list()
        adj_list2 = {}

        for k, v in adj_list.items():
            adj_list2[str(k)] = v

        return str(adj_list2)

    def __len__(self):
        return self._node_len


def parse_coords_node(node: GraphNode):
    try:
        coords = node.contains['coords']
    except KeyError:
        try:
            coords = node.contains['coord1'], node.contains['coord2']
            try:
                coords += tuple(node.contains['coord3'])
            except KeyError:
                pass
        except KeyError:
            raise AttributeError("The node must contain a field called 'coords', or fields 'coord1','coord2','coord3'.")
    return Point(coords)


def graph_from_geodata_csv(filepath: str) -> Graph:
    """Gets a graph from a file containing lat long coordinates.

    This function assumes the necessary columns in the
    file are labelled 'lat','long', and 'label'.
    It also assumes each node has been properly initialized with
    kwargs containing 'lat','long',or 'pos'.
    
    :param filepath: The path to the file
    :type filepath: str
    :return: A connected graph
    :rtype: Graph
    """
    gdf = pd.read_csv(filepath)
    graph = Graph()

    gdf['coord1'] = gdf['coord1'].astype(float)
    gdf['coord2'] = gdf['coord2'].astype(float)
    gdf['label'] = gdf['label'].astype(str)

    for i, row in gdf.iterrows():

        node = GraphNode(coord1=row['coord1'], coord2=row['coord2'], label=row['label'])
        graph.add_vertex(node)
        coords = parse_coords_node(node)

        for j in range(len(graph)):
            other = graph.get_vertex(j)
            ocoords = parse_coords_node(other)
            graph.add_edge(node, other, dist_to_spherical(coords, ocoords))

    return graph
