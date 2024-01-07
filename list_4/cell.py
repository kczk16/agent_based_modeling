#Authors: Karolina Ostrowska, Aleksandra Sawczuk
from itertools import product, starmap
import numpy as np


class cell:
    def __init__(self):
        self._occupant = 3

    @property
    def occupant(self):
        """
        Occupant attribute property.
        :return: occupant attribute value
        :rtype: int
        """
        return self._occupant

    @occupant.setter
    def occupant(self, occupant):
        """
        Sets occupant attribute.
        :param occupant: occupant attribute value that will be set
        :type occupant: int
        """
        self._occupant = occupant

    def get_neighbours(self, a, b, size=[100, 100]):
        """
        Gets neighbours of cell.
        :param a: first coordinate of element
        :type a: int
        :param b: second coordinate of element
        :type b: int
        :param size: size of array
        :type size: list of int
        :return: list of neighbours
        :rtype: list of lists
        """
        neighs = self._get_all_neighbours(a, b)
        n_list = []
        for n in neighs:
            if 0 <= n[0] < size[0] and 0 <= n[1] < size[1]:
                n_list.append(n)
        return n_list

    def get_periodic_neighbours(self, a, b, layer=1, size=[100, 100]):
        """
        Gets periodic neighbours on array of element.
        :param a: first coordinate of element
        :type a: int
        :param b: second coordinate of element
        :type b: int
        :param layer: layer of neighbours
        :type layer: int
        :param size: size of array
        :type size: list of int
        :return: list of neighbours
        :rtype: list of tuples
        """
        neighs = self.get_layered_neighbours(a, b, layer)
        n_list = []
        for n in neighs:
            n_cords = []
            if 0 <= n[0] < size[0]:
                n_cords.append(n[0])
            if n[0] < 0:
                n_cords.append(size[0] + n[0])
            if n[0] >= size[0]:
                n_cords.append(abs(size[0] - n[0]))
            if 0 <= n[1] < size[1]:
                n_cords.append(n[1])
            if n[1] >= size[1]:
                n_cords.append(abs(size[1] - n[1]))
            if n[1] < 0:
                n_cords.append(size[1] + n[1])
            n_list.append(tuple(n_cords))

        return n_list

    @staticmethod
    def get_layered_neighbours(x, y, layer):
        """
        Gets layered neighbours without taking into account grid size.
        :param x: first coordinate of element
        :type x: int
        :param y: second coordinate of element
        :type y: int
        :param layer: layer of neighbours
        :type layer: int
        :return: list of neighbours
        :rtype: list of tuples
        """
        p = range(-layer, layer + 1)
        cells = starmap(lambda a, b: (x + a, y + b), product(p, p))
        return [i for i in cells if i != (x, y)]

    @staticmethod
    def _get_all_neighbours(x, y):
        """
        Gets all 8 neighbours of element.
        :type x: int
        :param y: second coordinate of element
        :type y: int
        :return: list of neighbours
        :rtype: list of tuples
        """
        cells = starmap(lambda a, b: (x + a, y + b), product((0, -1, +1), (0, -1, +1)))
        return [i for i in cells if i != (x, y)]
