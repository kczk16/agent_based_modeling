#Authors: Karolina Ostrowska, Aleksandra Sawczuk

class cell:
    def __init__(self):
        self._status = 0

    def set_dead(self):
        self._status = 0

    def set_alive(self):
        self._status = 1

    def is_alive(self):
        return self._status

    def get_neighbours(self, a, b, size):
        neighs = self._get_all_neighbours(a, b)
        n_list = []
        for n in neighs:
            if n[0] >= 0 and n[0] < size[0] and n[1] >= 0 and n[1] < size[1]:
                n_list.append(n)
        return n_list

    @staticmethod
    def _get_all_neighbours(a, b):
        return [(a, b + 1), (a, b - 1), (a + 1, b), (a - 1, b), (a - 1, b + 1),
                (a - 1, b - 1), (a + 1, b - 1), (a + 1, b + 1)]

    def handle_when_alive(self, neigh_list):
        if sum(neigh_list) in [2, 3]:
            pass
        else:
            self.set_dead()

    def handle_when_dead(self, neigh_list):
        if sum(neigh_list) == 3:
            self.set_alive()
        else:
            pass
