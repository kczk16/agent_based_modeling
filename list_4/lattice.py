import numpy as np
import random
from collections import Counter


class Lattice:

    def __init__(self):
        self._grid = None

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

    def start_simulation(self, n_red=250, n_blue=250):
        """
        Makes the starting state on grid. Blue and red agents are set in random places on the lattice.
        :param n_red: number of red agents
        :type n_red: int
        :param n_blue: number of blue agents
        :type n_blue: int
        """
        n_of_ragents, n_of_bagents = 0, 0
        stop = False
        while not stop:
            x_r, y_r = random.choice(self._get_empty_spaces())
            x_b, y_b = random.choice(self._get_empty_spaces())
            if self.grid[x_r, y_r].occupant == 3 and n_of_ragents < n_red:
                self.grid[x_r, y_r].occupant = 1
                n_of_ragents += 1
            if self.grid[x_b, y_b].occupant == 3 and n_of_bagents < n_blue:
                self.grid[x_b, y_b].occupant = 2
                n_of_bagents += 1

            stop = all([n_of_ragents == n_red, n_of_bagents == n_blue])

    def change_state(self, ratio_r=0.5, ratio_b=0.5, neigh_layer=1):
        """
        Changes state on the grid in one iteration.
        :param ratio_r: Ratio for happiness for red agents
        :type ratio_r: float
        :param ratio_b: Ratio for happiness for blue agents
        :type ratio_b: float
        :param neigh_layer: layer of neighbours that should be taken into account
        :type neigh_layer: int
        :return: segregation index for one iteration
        :rtype: int or float
        """
        grid = np.copy(self.grid)
        segregation = []
        unhappy_list = []
        for index, elem in np.ndenumerate(grid):
            neighs = elem.get_periodic_neighbours(index[0], index[1], neigh_layer, list(grid.shape))
            n_statuses = Counter([grid[n].occupant for n in neighs])
            ratio = self._get_ratio(elem, ratio_r, ratio_b)
            other = self._get_oppsite_occupant(elem)
            current_ratio = self._get_current_ratio(elem, other, n_statuses)
            segregation.append(current_ratio)
            if 0 <= current_ratio < ratio:
                unhappy_list.append([index, elem])

        possible_locations = self._get_empty_spaces() + [place[0] for place in unhappy_list]
        self._shuffle_unhappy_agents(unhappy_list, possible_locations)
        return sum(segregation)/len(segregation)

    def get_random_location(self, choice, exclude):
        """
        Gets random location from available locations with exclusion of "exclude".
        :param choice: list of possible locations
        :type choice: list of tuples
        :param exclude: element that should be excluded from draw
        :type exclude: tuple
        :return: random element chosen from "choice"
        :rtype: tuple
        """
        place = random.choice(choice)
        return self.get_random_location(choice, exclude) if place in exclude else place

    def _shuffle_unhappy_agents(self, unhappy_list, possible_locations):
        """
        Shuffles unhappy angents on the grid.
        :param unhappy_list: list of unhappy agents
        :type unhappy_list: list of lists, [[location of agent, agent instance]]
        :param possible_locations: list of possible locations on the grid
        :type possible_locations: list of tuples
        """
        empty_instances = self._get_empty_spaces_instances()
        for unhappy_agent in unhappy_list:
            new_location = self.get_random_location(possible_locations, unhappy_agent[0])
            possible_locations.remove(new_location)
            self.grid[new_location] = unhappy_agent[1]
        for left_place in range(len(possible_locations)):
            self.grid[possible_locations[left_place]] = empty_instances[left_place]

    @staticmethod
    def _get_current_ratio(elem, other, n_statuses):
        """
        Gets current ratio for agent.
        :param elem: cell instance representing agent
        :type elem: cell instance
        :param other: cell instance representing different type agent
        :type other: cell instance with different value for occupant attribute than elem
        :param n_statuses: dictionary with countent occupant types in neighbours of elem
        :type n_statuses: dict
        :return: ratio
        """
        colored_cells = n_statuses[other] + n_statuses[elem.occupant]
        return n_statuses[elem.occupant]/colored_cells if colored_cells != 0 else 0

    @staticmethod
    def _get_oppsite_occupant(elem):
        """
        Gets cell instance with different (but not empty) occupant attribute than elem.
        :param elem: cell instance representing agent
        :type elem: cell instance
        :return: value of occupant attribute for different color (red if blue, blue if red)
        :rtype: int
        """
        return 1 if elem.occupant == 2 else 2

    @staticmethod
    def _get_ratio(elem, ratio_r, ratio_b):
        """
        Gets ratio for happiness for agent.
        :param elem: cell instance representing agent
        :type elem: cell instance
        :param ratio_r: Ratio for happiness for red agents
        :type ratio_r: float
        :param ratio_b: Ratio for happiness for blue agents
        :type ratio_b: float
        :return: ratio for happiness for elem
        """
        return ratio_r if elem.occupant == 1 else ratio_b if elem.occupant == 2 else -1

    def _get_empty_spaces(self):
        """
        Gets empty spaces on grid.
        :return: list of empty spaces
        :rtype list of tuples
        """
        return [index for index, loc in np.ndenumerate(self.grid) if loc.occupant == 3]

    def _get_empty_spaces_instances(self):
        """
        Gets instances of empty cells on grid.
        :return: list of cell instances that represent empty places
        :rtype: list of cell instances
        """
        return [loc for index, loc in np.ndenumerate(self.grid) if loc.occupant == 3]
