import numpy as np
from trees import Tree


class Lattice:

    def __init__(self):
        self.grid = None

    def change_state(self):
        """
        Changes state of the lattice: burning trees get burnt, neighbours of burning trees catch fire,
        :return: list of burning trees
        """
        trees, burning = self._check_state()
        trees = trees.tolist()
        for cord in burning:
            self.grid[cord[0], cord[1]] = 3
            tree = Tree()
            tree._configure(place=cord)
            neigh = tree._get_regular_neighbours()
            for neighbour in neigh:
                if neighbour in trees:
                    self.grid[neighbour[0], neighbour[1]] = 2
        return burning

    def start_fire(self, edge):
        """
        Starts fire on the given edge of the lattice
        :param edge: edge of the lattice where fire should start
        """
        cords = self._edge_to_cord(edge)
        for c in cords:
            if self.grid[c[0], c[1]] == 1:
                self.grid[c[0], c[1]] = 2

    def get_opposite_edge(self, edge):
        """
        Gets coordinates of points on the opposite edge.
        :param edge: edge to which the opposite coordinates should be returned
        :return: list of coordinates
        """
        if edge == 'left':
            return self._edge_to_cord(edge='right')
        if edge == 'right':
            return self._edge_to_cord(edge='left')
        if edge == 'top':
            return self._edge_to_cord(edge='bottom')
        if edge == 'bottom':
            return self._edge_to_cord(edge='top')

    def check_if_burnt(self, edge_cord):
        """
        Checks if any tree on the given edge has been burnt.
        :param edge_cord: list of coordinates for points on the edge
        :return: True if any tree on the given edge has been burnt, else false
        """
        trees = np.argwhere(self.grid == 3).tolist()
        return True if any((cord in trees for cord in edge_cord)) else False

    def hoshen_kopelman(self):
        """
        Performs clustering using hashen kopelman alghoritm
        :return: distionary with trees and clusters to which they have been assigned
        """
        burnt, trees = self._get_burnt_trees()
        c = 0
        for tree in trees.keys():
            neighs = tree._get_neumann_neighbours()
            if tree.cluster_type != None:
                self._handle_when_cluster_not_none(neighs, trees, tree)
            else:
                clusters_neigh = self._get_clusters_of_neighbours(neighs, trees)

                if len(set(clusters_neigh)) > 1:
                    self._handle_when_cluster_none_and_diff_neighbours(trees, tree, clusters_neigh)

                elif len(set(clusters_neigh)) == 1:
                    tree.cluster_type = clusters_neigh[0]

                elif len(set(clusters_neigh)) == 0:
                    tree.cluster_type = c
                    c += 1

        return trees

    def _get_burnt_trees(self):
        burnt = np.argwhere(self.grid == 3).tolist()
        trees = {}
        for i in range(len(burnt)):
            tree = Tree()
            tree._configure(place=burnt[i])
            trees[tree] = burnt[i]
        return burnt, trees

    @staticmethod
    def _handle_when_cluster_none_and_diff_neighbours(trees, tree, clusters_neigh):
        tree.cluster_type = clusters_neigh[0]
        cluster_set = set(clusters_neigh)
        cluster_set.remove(tree.cluster_type)
        for k, v in trees.items():
            for cl_t in cluster_set:
                if k.cluster_type == cl_t:
                    k.cluster_type = tree.cluster_type

    @staticmethod
    def _get_clusters_of_neighbours(neighs, trees):
        clusters_neigh = []
        for n in neighs:
            try:
                neigh = [k for k, v in trees.items() if v == n][0]
                if neigh.cluster_type != None:
                    clusters_neigh.append(neigh.cluster_type)
            except IndexError:
                neigh = None
        return clusters_neigh

    @staticmethod
    def _handle_when_cluster_not_none(neighs, trees, tree):
        for n in neighs:
            try:
                neigh = [k for k, v in trees.items() if v == n][0]
                if neigh.cluster_type != tree.cluster_type:
                    neigh.cluster_type = tree.cluster_type
                    cluster_group = [k for k, v in trees.items() if k.cluster_type == neigh.cluster_type]
                    for elem in cluster_group:
                        elem.cluster_type = tree.cluster_type
            except IndexError:
                neigh = None

    def _check_state(self):
        return np.argwhere(self.grid == 1), np.argwhere(self.grid == 2)

    def _edge_to_cord(self, edge):
        if edge == 'left':
            return [[i, 0] for i in range(len(self.grid))]
        if edge == 'right':
            return [[i, len(self.grid) - 1] for i in range(len(self.grid))]
        if edge == 'bottom':
            return [[len(self.grid) - 1, i] for i in range(len(self.grid))]
        if edge == 'top':
            return [[0, i] for i in range(len(self.grid))]

    def _configure(self, size):
        self.grid = np.zeros(shape=[size, size])
