import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from random import randint, random, choices


def magnetization(opinions):
    '''
    function that calculates magnetization
    :param opinions: all opinions for each node in the graph
    :type opinions: list
    :return: magnetization
    '''
    return np.mean(opinions)


def _set_initial_opinions(graph):
    '''
    function that sets initial opinions for all nodes
    :param graph: graph class
    :type graph: graph
    :return: networkx graph instance
    '''
    no_of_nodes = len(list(graph.nodes(data=True)))
    for i in range(1, no_of_nodes + 1):
        graph.nodes[i - 1]["opinion"] = 1
    return graph


def init_graph(type_name, q):
    '''
    function that returns graph with certain type
    :param type_name: type of graph
    :type type_name: str
    :param q: number of neighbours for each node
    :type q: int
    :return: networkx graph instance, label
    '''
    if type_name == 'random':
        return nx.random_regular_graph(q, 100), type_name
    elif type_name == 'complete':
        return nx.complete_graph(q + 1), type_name
    elif type_name == 'barabasi_albert':
        return nx.barabasi_albert_graph(100, q), type_name
    elif type_name == 'watts_strogatz_1':
        return nx.watts_strogatz_graph(100, q, 0.01), type_name
    elif type_name == 'watts_strogatz_2':
        return nx.watts_strogatz_graph(100, q, 0.2), type_name


def q_voter(p_independent=0.5, f=0.5, q=4, steps=50):
    '''
    function that returns graph and magnetization value after given number of steps
    :param graph: graph class
    :type graph: graph
    :param p_independent: probability of independence of node
    :type p_independent: float
    :param f: probability of changing the opinion for independent node
    :type f: float
    :param q: number of neighbours for each node
    :type q: int
    :param steps: number of steps
    :type steps: int
    :return: networkx graph instance, list of magnetization values per step
    '''
    type_name = 'complete'
    graph, _ = init_graph(type_name, q)
    no_of_nodes = len(list(graph.nodes(data=True)))
    _set_initial_opinions(graph)
    m_per_time_step = []
    for step in range(steps):
        s = randint(0, no_of_nodes - 1)
        if random() < p_independent:
            if random() < f:
                if graph.nodes[s]["opinion"] == 1:
                    graph.nodes[s]["opinion"] = 0
                else:
                    graph.nodes[s]["opinion"] = 1
        else:
            neighbors = graph.neighbors(s)
            neighbors_list = list(neighbors)
            neighbors_chosen = choices(neighbors_list, k=q)
            sum_of_neigh_opinions = 0
            for neighbor in neighbors_chosen:
                sum_of_neigh_opinions += graph.nodes[neighbor]["opinion"]
            if (sum_of_neigh_opinions != 0) and (sum_of_neigh_opinions % q == 0):
                graph.nodes[s]["opinion"] = (sum_of_neigh_opinions / 4)

        opinions = [graph.nodes[j]['opinion'] for j in list(graph.nodes())]
        m = magnetization(opinions)
        m_per_time_step.append(m)
    return graph, m_per_time_step


# graph = nx.barabasi_albert_graph(100, 4)
# g, m = q_voter(graph)


def monte_carlo(monte_carlo_steps, f, q=4, steps=50):
    '''
    function that applies monte carlo method
    :param monte_carlo_steps: monte carlo steps
    :type monte_carlo_steps: int
    :param q: number of neighbours for each node
    :type q: int
    :param f: probability that dependent node change its opinion
    :type f: float
    :param steps: number of steps
    :type steps: int
    :return: average magnetization, list with all magnetization values
    '''
    p = np.linspace(0, 1, 100)
    avg_m = []
    allall_m = []
    for prob in p:
        all_m = []
        for step in range(monte_carlo_steps):
            _, m = q_voter(p_independent=prob, f=f, q=q, steps=steps)
            all_m.append(m)
        avg = [np.mean(i) for i in zip(*all_m)]
        avg_m.append(avg)
        allall_m.append(all_m)
    return avg_m, allall_m


# avg_m, allall_m = monte_carlo(100, graph, f=0.2, q=4, steps=50)

def final_mag_for_all_topo_mc(q):
    '''
    function that plots average magnetization per p (monte carlo)
    :param q: number of neighbours for each node
    :type q: int
    '''
    f_prob_list = [0.2, 0.3, 0.4, 0.5]
    for f in f_prob_list:
        p = np.linspace(0, 1, 100)
        avg_m_per_p = []
        avg_m, _ = monte_carlo(100, f, q=4, steps=100)
        for i in range(len(avg_m)):
            avg_m_per_p.append(np.mean(avg_m[i]))
        plt.plot(p, avg_m_per_p, 'o', label='f = ' + str(f))
    plt.title('Concentration vs p for different f')
    plt.xlabel('p')
    plt.ylabel('c')
    plt.legend()
    plt.show()


final_mag_for_all_topo_mc(q=4)




