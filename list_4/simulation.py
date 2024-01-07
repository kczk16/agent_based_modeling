import numpy as np
from lattice import Lattice
from PIL import Image
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import os
import glob
from cell import cell


def simulate(neigh_layer=1, n_agents=4000, ratio_r=0.5, ratio_b=0.5, gif=False):
    """
    Simulates agents on lattice.
    :param neigh_layer: layer of neighbours
    :type neigh_layer: int
    :param n_agents: number of red and blue agents
    :type n_agents: int
    :param ratio_r: Ratio for happiness for red agents
    :type ratio_r: float
    :param ratio_b: Ratio for happiness for blue agents
    :type ratio_b: float
    :param gif: if true gif will be saved
    :type gif: bool
    :return: number of iterations, number of agents, segregation index in last iteration
    """
    lattice = Lattice()
    lattice.grid = np.array([cell() for _ in range(10000)]).reshape([100, 100])
    lattice.start_simulation(n_red=n_agents, n_blue=n_agents)
    if gif:
        _del_remained_pngs()
    n_iteration, stop = 0, 0
    while not stop:
        if gif:
            plot_grid(lattice.grid, str(n_iteration+1))
        before_grid = _get_occupants_on_array(lattice.grid)
        seg = lattice.change_state(ratio_r=ratio_r, ratio_b=ratio_b, neigh_layer=neigh_layer)
        n_iteration += 1
        stop = any([_check_change(before_grid, _get_occupants_on_array(lattice.grid)), n_iteration == 250])
    return n_iteration, n_agents, seg


def make_and_save_gif(neigh_layer=1):
    """
    Creates a gif of neighbours spread on a lattice over time
    :param size: size of the squared lattice
    :param p: probability for every cell that it will be populated by a tree
    :param edge: edge of lattice where the fire starts
    """
    simulate(neigh_layer=neigh_layer, gif=True)
    _gif()


def plot_grid(grid, name):
    """
    Plots and saves to .png file state of neighbours on the lattice
    :param grid: squared array representing lattice
    :param name: name by which the plot will be saved
    """
    grid = np.vectorize(lambda x: x.occupant)(grid)
    cmap = ListedColormap(['red', 'blue', 'grey'])
    plt.matshow(grid, cmap=cmap, vmin=1, vmax=3)
    plt.title(name)
    plt.savefig(name)


def mc_iterations_vs_agents(MC=50):
    """
    Makes plot of number of iterations in simulation vs number of agents.
    :param MC: number of Monte Cartio repetitions
    :type MC: int
    """
    n_agents = np.arange(250, 4050, 50)
    mc_iterations, agents = [], []
    for n in n_agents:
        iterations = []
        for i in range(MC):
            n_iteration, n_agent, _ = simulate(neigh_layer=1, n_agents=n, gif=False)
            iterations.append(n_iteration)
        agents.append(n_agent * 2)
        mc_iterations.append(sum(iterations)/len(iterations))

    plt.plot(agents, mc_iterations)
    plt.xlabel('number of agents')
    plt.ylabel('number of iterations')
    plt.title('number of iterations vs number of agents')
    plt.savefig('no_iterations_vs_agents')


def MC_segregation_index(ratios_list=np.arange(0.1, 1, 0.1), MC=50):
    """
    Makes plot of segregation index vs happines ratios in simulations.
    :param ratios_list: list of happines ratios
    :type ratios_list: list of floats
    :param MC: number of Monte Cartio repetitions
    :type MC: int
    """
    index_list = []
    for ratio in ratios_list:
        i_ratio = []
        for i in range(MC):
            _, _, index = simulate(neigh_layer=1, ratio_r=ratio, ratio_b=ratio)
            i_ratio.append(index)
        index_list.append(sum(i_ratio)/len(i_ratio))
    plt.plot(ratios_list, index_list)
    plt.xlabel('to-stay ratio')
    plt.ylabel('segregation index')
    plt.title('segregation index vs ratio')
    plt.savefig('segregation_index_vs_ratio')


def MC_segregation_vs_layer(layers_list=np.arange(1, 6, 1), MC=50):
    """
    Makes plot of segregation index vs layer of neighbours.
    :param layers_list: list of layers
    :type layers_list: list of ints
    :param MC: number of Monte Cartio repetitions
    :type MC: int
    """
    index_list = []
    for layer in layers_list:
        i_layer = []
        for i in range(MC):
            _, _, index = simulate(neigh_layer=layer)
            i_layer.append(index)
        index_list.append(sum(i_layer)/len(i_layer))
    plt.plot(layers_list, index_list)
    plt.xlabel('layer number')
    plt.ylabel('segregation index')
    plt.title('segregation index vs layer of neighbours')
    plt.savefig('segregation_index_vs_layer_of_neighbours')


def _del_remained_pngs():
    """
    Deleted png files in working directory.
    """
    path = os.getcwd()
    for file in os.listdir(path):
        if file.endswith('.png'):
            os.remove(file)


def _sort_names(name):
    """
    Sorts names interpreting them as int
    :param name: file name
    :type name: str
    :return: int
    """
    return int(''.join(filter(str.isdigit, name)))


def _sort_pngs():
    """
    Sorts pngs in working directory.
    :return: imgs
    """
    imgs = glob.glob("*.png")
    imgs.sort(key=_sort_names)
    return imgs


def _gif():
    """
    Creates a gif of neighbours changes on a lattice over time from saved pngs
    """
    frames = []
    imgs = _sort_pngs()
    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)
    frames[0].save('simulation.gif', format='GIF', append_images=frames[1:], save_all=True, duration=1000, loop=0)


def _get_occupants_on_array(array):
    """
    Gets occupant attribute value of cells on array.
    :param array: lattice as numpy array
    :type array: numpy array
    :return: array of occupant attribute value for cells on the lattice
    :rtype: numpy array
    """
    return np.array([elem.occupant for _, elem in np.ndenumerate(array)])


def _check_change(before, after):
    """
    Compares two arrays.
    :param before: first array to be compared
    :type before: numpy array
    :param after: second array to be compared
    :type after: numpy array
    :return: True if arrays are the same, false otherwise
    :rtype: bool
    """
    return np.array_equal(before, after)

make_and_save_gif(neigh_layer=4)