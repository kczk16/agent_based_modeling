import numpy as np
from cell import cell
from random import random


class Road:

    def __init__(self):
        self._grid = np.array([cell() for _ in range(100)]).reshape([1, 100])

    @property
    def grid(self):
        """
        Grid attribute property.
        :return: grid
        :rtype: None or setted value - numpy array
        """
        return self._grid

    @grid.setter
    def grid(self, val):
        """
        Grid attribute setter.
        :param val: value that will be assigned to grid attribute
        """
        self._grid = val

    def start_simulation(self, rho=0.1):
        """
        Gets road into starting state.
        :param rho: probability of car on cell on the road
        :type rho: float
        """
        for index, elem in np.ndenumerate(self.grid):
            if random() <= rho:
                self.grid[index].occupant = 1

    def change_state(self, p, max_v):
        """
        Changes state of cars on the road.
        :param p: probability for randomization
        :type p: float
        :param max_v: maximum velocity of cars
        :type max_v: int
        :return: average velocity of cars on the road
        :rtype: int or float
        """
        grid = self.grid.copy()
        cars_to_move, velocities = [], []
        for index, elem in np.ndenumerate(grid):

            distance = elem._check_distance_to_closest_car(index, grid, max_v)
            self._adjust_velocity_of_car(elem, max_v, distance, p, index, cars_to_move)

            if elem.occupant:
                velocities.append(elem.velocity)

        for car in cars_to_move:
            self._move_car(car[0], car[1])

        return sum(velocities)/len(velocities)

    def _adjust_velocity_of_car(self, elem, max_v, distance, p, index, cars_to_move):
        """
        Adjusts velocity of car
        :param elem: cell instance
        :param max_v: maximum velocity
        :param distance: distance to closest car
        :param p: probability for randomization
        :param index: coordinates of car on the road
        :param cars_to_move: list of cars to be moved
        """
        if elem.occupant and elem.velocity < max_v and elem.velocity < distance - 1:
            elem.velocity += 1
        if elem.velocity:
            self._randomize(p, elem)
        if elem.occupant and elem.velocity:
            if elem.velocity < distance:
                cars_to_move.append([index, elem])
            else:
                elem.velocity = distance - 1

    @staticmethod
    def _randomize(p, elem):
        """
        Decreases car velocity by one with probability p
        :param p: probability
        :type p: float
        :param elem: cell instance
        :type elem: cell class instance
        """
        if random() < p and elem.velocity:
            elem.velocity -= 1

    def _move_car(self, index, elem, length=100):
        """
        Moves car on the road
        :param index: coordinates of car on the road
        :type index: tuple
        :param elem: cell instance
        :type elem: cell class instance
        :param length: length of the road
        :type length: int
        """
        if index[1]+elem.velocity < length:
            self.grid[(index[0], index[1]+elem.velocity)] = elem
        else:
            self.grid[(index[0], abs(length - (index[1] + elem.velocity)))] = elem
        self.grid[index] = cell()
