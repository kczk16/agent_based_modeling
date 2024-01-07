import random
import os
import glob
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from collections import Counter
from trees import Tree
from lattice import Lattice


def simulate(size, p, edge='left', gif=False, clusters=False):
    """
    Simulates fire on lattice.
    :param size: size of the squared lattice
    :param p: probability for every cell that it will be populated by a tree
    :param edge: edge of lattice where the fire starts
    :param gif: boolean value if gif of the simulation should be made
    :param clusters: boolean value if clustering using hoshen kopelman algorithm should be made
    :return: boolean if the fire got to the opposite edge
    """
    lattice = _generate_start_state_of_trees(size, p, gif)
    opposite = lattice.get_opposite_edge(edge=edge)
    lattice.start_fire(edge=edge)
    if gif:
        _del_remained_pngs()
        plot_fire(lattice.grid, '1')
    burning = lattice.change_state()
    i = 2
    while len(burning):
        if gif:
            plot_fire(lattice.grid, str(i))
        burning = lattice.change_state()
        i += 1
    if clusters:
        trees = lattice.hoshen_kopelman()
        cord, cluster = [], []
        for tree in trees:
            cord.append(tree.place)
            cluster.append(tree.cluster_type)
        return lattice.check_if_burnt(edge_cord=opposite), cluster

    return lattice.check_if_burnt(edge_cord=opposite)


def simulate_monte_carlo(size=20, edge='left', N=100):
    """
    Simulates fire in a loop for different p
    :param size: size of the squared lattice
    :param edge: edge of lattice where the fire starts
    :param N: number of monte carlo iterations
    :return: list of p, list of boolean values where every value says whether fire got to the opposite edge
    """
    burnt_per_p = []
    p_list = np.linspace(0, 1, 100)
    for p in p_list:
        if_burnt = []
        for n in range(N):
            burnt = simulate(size=size, p=p, edge=edge)
            if_burnt.append(burnt)
        burnt_per_p.append(sum(if_burnt)/N)

    return p_list, burnt_per_p


def draw_mc_per_p(size=20, edge='left', N=100):
    """
    Makes plot of probability of the fire getting to the opposite edge for different p and marks threshold
    :param size: size of the squared lattice
    :param edge: edge of lattice where the fire starts
    :param N: number of monte carlo iterations
    """
    p_list, burnt_per_p = simulate_monte_carlo(size=size, edge=edge, N=N)
    p_threshold = _get_p_threshold(burnt_per_p)
    plt.plot(p_list, burnt_per_p)
    plt.plot((p_threshold+1)/100, 0, marker='o', label='p threshold')
    plt.title('p vs probability of the fire getting to the other end')
    plt.xlabel('p')
    plt.ylabel('q')
    plt.legend()
    plt.show()


def make_and_save_gif(size=20, p=0.5, edge='left'):
    """
    Creates a gif of fire spread on a lattice over time
    :param size: size of the squared lattice
    :param p: probability for every cell that it will be populated by a tree
    :param edge: edge of lattice where the fire starts
    """
    simulate(size=size, p=p, edge=edge, gif=True)
    _gif()


def _gif():
    """
    Creates a gif of fire spread on a lattice over time from saved pngs
    """
    frames = []
    imgs = _sort_pngs()
    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)
    frames[0].save('fire.gif', format='GIF', append_images=frames[1:], save_all=True, duration=500, loop=0)


def plot_fire(grid, name):
    """
    Plots and saves to .png file state of fire on the lattice
    :param grid: squared array representing lattice
    :param name: name by which the plot will be saved
    """
    cmap = ListedColormap(['tan', 'green', 'red', 'grey'])
    plt.matshow(grid, cmap=cmap, vmin=0, vmax=3)
    plt.savefig(name)


def biggest_cluster_vs_p_MC(size=20, edge='left', N=100):
    """
    Calculates size of the biggest cluster in burnt trees on the lattice.
    :param size: size of the squared lattice
    :param edge: edge of lattice where the fire starts
    :param N: number of monte carlo iterations
    :return: list of p, list of cbiggest clusters per p
    """
    p_list = np.linspace(0, 1, 100)
    sizes_per_p = []
    for p in p_list:
        sizes_for_one_p = []
        for n in range(N):
            _, clusters = simulate(size=size, p=p, edge=edge, clusters=True)
            num_per_cluster = Counter(clusters).values()
            if num_per_cluster:
                sizes_for_one_p.append(max(num_per_cluster))
            else:
                sizes_for_one_p.append(0)

        sizes_per_p.append(sum(sizes_for_one_p)/N)

    return p_list, sizes_per_p


def plot_cluster_size_vs_p(size=20, edge='left', N=100):
    """
    Plots cluster size vs p
    :param size: size of the squared lattice
    :param edge: edge of lattice where the fire starts
    :param N: number of monte carlo iterations
    """
    p_list, size_per_p = biggest_cluster_vs_p_MC(size=size, edge=edge, N=N)
    plt.plot(p_list, size_per_p)
    plt.title('p vs size of the biggest cluster')
    plt.xlabel('p')
    plt.ylabel('size')
    plt.show()


def _generate_start_state_of_trees(size, p, gif=False):
    """
    Generates starting state of trees on the lattice.
    :param size: size of the square lattice
    :type size: int
    :param p: probability that a cell of the lattice is populated by a tree
    :param p: float
    """
    lattice = Lattice()
    lattice._configure(size=size)

    for (x, y), value in np.ndenumerate(lattice.grid):
        if random.random() < p:
            lattice.grid[x, y] = 1
    if gif:
        plot_fire(lattice.grid, '0')

    return lattice


def _del_remained_pngs():
    path = os.getcwd()
    for file in os.listdir(path):
        if file.endswith('.png'):
            os.remove(file)


def _sort_names(name):
    return int(''.join(filter(str.isdigit, name)))


def _sort_pngs():
    imgs = glob.glob("*.png")
    imgs.sort(key=_sort_names)
    return imgs


def _get_p_threshold(p_list):
    th = np.diff(p_list)
    return np.argmax(th)

#make_and_save_gif(size=100)
# simulate(size=15, p=0.5)
# gif()
#draw_mc_per_p(size=50, edge='left', N=50)
#draw_mc_per_p(size=20, edge='left', N=100)