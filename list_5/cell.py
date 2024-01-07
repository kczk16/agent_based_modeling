#Authors: Karolina Ostrowska, Aleksandra Sawczuk

class cell:
    def __init__(self):
        self._occupant = 0
        self._velocity = 0

    @property
    def occupant(self):
        """
        Occupant attribute property - 1 if car is present, 0 otherwise.
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
        if not occupant:
            self._velocity = 0
        self._occupant = occupant

    @property
    def velocity(self):
        """
        Velocity attribute property.
        :return: velocity attribute value
        :rtype: int
        """
        return self._velocity

    @velocity.setter
    def velocity(self, velocity):
        """
        Sets velocity attribute.
        :param velocity: velocity attribute value that will be set
        :type velocity: int
        """
        self._velocity = velocity

    def get_neighbours(self, a, size=[100, 1]):
        """
        Gets neighbours of cell.
        :param a: first coordinate of element
        :type a: int
        :param size: size of array
        :type size: list of int
        :return: list of neighbours
        :rtype: list of lists
        """
        neighs = self._get_front_neighbour(a)
        n_list = []
        for n in neighs:
            if 0 <= n[0] < size[0] and 0 <= n[1] < size[1]:
                n_list.append(n)
        return n_list

    def get_periodic_neighbours(self, a, size=[100, 1]):
        """
        Gets periodic neighbours on road of element.
        :param a: first coordinate of element
        :type a: int
        :param size: size of road
        :type size: list of int
        :return: neighbour
        :rtype: tuple
        """
        n = self._get_front_neighbour(a)
        if 0 <= n[1] < size[1]:
            return n[0], n[1]
        if n[1] >= size[1]:
            return n[0], (abs(size[1] - n[1]))

    @staticmethod
    def _get_front_neighbour(x):
        """
        Gets one neighbour in front of element.
        :param x: car coordinate
        :type x: int
        :return: list of neighbours
        :rtype: list
        """
        return [0, x + 1]

    def _check_distance_to_closest_car(self, index, road, max_v):
        """
        Checks distance to closest car in front of element
        :param index: place of element on the road
        :type index: tuple
        :param road: array representing road
        :type road: numpy array
        :param max_v: maximum velocity
        :type max_v: int
        :return: maximum velocity
        :rtype: int
        """
        for place in range(index[1]+1, index[1]+max_v):
            n = self.get_periodic_neighbours(place-1, size=[1, 100])
            if road[n].occupant:
                return abs(index[1] - place)
        return max_v
