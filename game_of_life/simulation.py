#Authors: Karolina Ostrowska, Aleksandra Sawczuk
from lattice import Lattice
from random import random
from PIL import Image
import glob
import os
import numpy as np
import matplotlib.pyplot as plt


def simulate_game(n_rows, n_columns, probability, max_iteration=50):
    lattice = get_starting_state(n_rows, n_columns, probability)
    stop, iteration = False, 1
    while not stop:
        lattice.change_state()
        iteration += 1
        statuses = []
        for row in lattice.grid:
            statuses = statuses + [i.is_alive() for i in row]
        stop = any([sum(statuses) == 0, max_iteration==iteration])
        plot_frame(lattice.grid, str(iteration))


def get_starting_state(n_rows, n_columns, probability):
    lattice = Lattice()
    lattice.initialize(n_rows, n_columns)
    grid = lattice.grid
    for cell_list in grid:
        for cell in cell_list:
            if random() < probability:
                cell.set_alive()
    plot_frame(lattice.grid, "1")
    return lattice


def plot_frame(grid, name):
    frame = []
    for cell_list in grid:
        row = []
        for cell in cell_list:
            row.append(cell.is_alive())
        frame.append(row)
    plt.matshow(np.array(frame))
    plt.savefig(name)


def make_and_save_gif(n_rows, n_columns, probability):
    _del_remained_pngs()
    simulate_game(n_rows, n_columns, probability)
    _gif()


def _gif():
    frames = []
    imgs = _sort_pngs()
    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)
    frames[0].save('game.gif', format='GIF', append_images=frames[1:], save_all=True, duration=500, loop=0)


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

#make_and_save_gif(n_rows=100, n_columns=75, probability=0.1)