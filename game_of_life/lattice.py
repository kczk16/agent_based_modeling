#Authors: Karolina Ostrowska, Aleksandra Sawczuk

import numpy as np
from cell import cell

class Lattice:

    def __init__(self):
        self.grid = None

    def initialize(self, n_rows, n_columns):
        self.grid = np.array([cell() for i in range(n_rows*n_columns)]).reshape([n_rows, n_columns])

    def change_state(self):
        grid = self.grid
        size = grid.shape
        for index, elem in np.ndenumerate(grid):


            neigh = elem.get_neighbours(index[0], index[1], size)
            neighs = [grid.item(cords) for cords in neigh]
            neighs_statuses = [n._status for n in neighs]
            if elem.is_alive():
                elem.handle_when_alive(neighs_statuses)
            else:
                elem.handle_when_dead(neighs_statuses)
