from road import Road
import numpy as np
from PIL import Image
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import os
import glob


def simulate(rho=0.1, p=0.2, max_v=5, gif=False):
    """
    Simulates movement of cars on the road.
    :param rho: probability of car on cell on the road
    :param p: probability for randomization
    :param max_v: maximum velocity of car
    :param gif: boolean if gif should be made
    :return: average velocity of cars
    """
    if gif:
        _del_remained_pngs()
    road = Road()
    road.start_simulation(rho=rho)
    vel = []
    for i in range(100):
        if gif:
            plot_grid(road.grid, str(i+1), rho, p)
        avg_v = road.change_state(p, max_v)
        vel.append(avg_v)
    return sum(vel)/len(vel)


def make_and_save_gif(rho=0.1, p=0.2, max_v=5):
    """
    Creates a gif of cars on road over time
    :param rho: probability of car on cell on the road
    :param p: probability for randomization
    :param max_v: maximum velocity
    """
    simulate(rho=rho, p=p, max_v=max_v, gif=True)
    _gif()


def plot_grid(grid, name, rho, p):
    """
    Plots and saves to .png file state of cars on the road
    :param grid: array representing road
    :param name: name by which the plot will be saved
    :param rho: probability of car on cell on the road
    :param p: probability for randomization
    """
    grid = np.vectorize(lambda x: x.occupant)(grid)
    cmap = ListedColormap(['black', 'red'])
    plt.matshow(grid, cmap=cmap, vmin=0, vmax=1)
    plt.title("simulation for rho: {} and p: {} ".format(rho, p))
    plt.savefig(name)


def plot_avg_v_vs_rho():
    """
    Plots average velocity over rho
    """
    rho = np.arange(0.05, 1, 0.05)
    ps = [0.2, 0.5, 0.7]
    avg_v_vs_rho = []
    for p in range(len(ps)):
        v_vs_rho = []
        for r in rho:
            v_vs_rho.append(simulate(r, ps[p]))
        avg_v_vs_rho.append(v_vs_rho)
        plt.plot(rho, avg_v_vs_rho[p], label="p={}".format(ps[p]))

    plt.title("average velocity vs rho")
    plt.xlabel("rho")
    plt.ylabel("average velocity")
    plt.legend()
    plt.show()


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
    Creates a gif of cars' position changes on road over time from saved pngs
    """
    frames = []
    imgs = _sort_pngs()
    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)
    frames[0].save('simulation.gif', format='GIF', append_images=frames[1:], save_all=True, duration=1000, loop=0)


plot_avg_v_vs_rho()