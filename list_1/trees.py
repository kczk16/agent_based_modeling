import numpy as np
import random


class Tree:

    def __init__(self):
        self.place = None
        self.cluster_type = None

    def _get_regular_neighbours(self):
        """
        Gets all 8 neighbours of a tree.
        :return: list of coordinates of neighbours
        :rtype: list of list
        """
        a, b = self.place[0], self.place[1]
        return [[a, b+1], [a, b-1], [a+1, b], [a-1, b], [a-1, b+1],
                [a-1, b-1], [a+1, b-1], [a+1, b+1]]

    def _get_neumann_neighbours(self):
        """
        Gets 4 Neumann's neighbours of a tree.
        :return: list of coordinates of neighbours
        :rtype: list of list
        """
        a, b = self.place[0], self.place[1]
        return [[a, b+1], [a, b-1], [a+1, b], [a-1, b]]

    def _configure(self, place):
        self.place = place

