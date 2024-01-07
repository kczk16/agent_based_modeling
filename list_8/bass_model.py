import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from random import random, sample
from itertools import zip_longest


def init_graph(type_name, q, n_of_agents):
    '''
    function that returns graph with certain type
    :param type_name: type of graph
    :type type_name: str
    :param q: number of neighbours for each node
    :type q: int
    :param n_of_agents: number of agents
    :type n_of_agents: int
    :return: networkx graph instance, label
    '''
    if type_name == 'random':
        return nx.random_regular_graph(q, n_of_agents), type_name
    elif type_name == 'complete':
        return nx.complete_graph(q + 1), type_name
    elif type_name == 'barabasi_albert':
        return nx.barabasi_albert_graph(n_of_agents, q), type_name
    elif type_name == 'watts_strogatz_1':
        return nx.watts_strogatz_graph(n_of_agents, q, 0.01), type_name
    elif type_name == 'watts_strogatz_2':
        return nx.watts_strogatz_graph(n_of_agents, q, 0.2), type_name


def bass_model(p=0.7, q=0.5, k=8, type_name='barabasi_albert', no_of_innovators=80, n_of_agents=500):
    '''
    function that returns graph and magnetization value after given number of steps
    :param p: probability coef of buying the product for innovator
    :type p: float
    :param q: probability coef of buying the product for imitator
    :type q: float
    :param k: number of neighbours for each node
    :type k: int
    :param type_name: type of graph
    :type type_name: str
    :param no_of_innovators: number of innovators
    :type no_of_innovators: int
    :param n_of_agents: number of agents
    :type n_of_agents: int
    :return: networkx graph instance, list of magnetization values per step
    '''
    graph, _ = init_graph(type_name, k, n_of_agents)
    no_of_nodes = len(list(graph.nodes(data=True)))
    graph = _split_community_to_innovators_and_imitators(graph, no_of_innovators)
    n_per_time_step, n = [], 0
    while n < n_of_agents:
        gr = graph
        m = 0
        for node in range(0, no_of_nodes):
            if random() < p*(1 - n/n_of_agents) and gr.nodes[node]["type"] and not gr.nodes[node]["bought"]:
                graph.nodes[node]["bought"] = 1
                m += 1
            elif random() < q*n/n_of_agents:
                neighbors_list = [gr.nodes[i]["bought"] for i in list(gr.neighbors(node))]
                if all(
                        (
                                any(
                                    (
                                            sum(neighbors_list) > int(0.22*len(neighbors_list)),
                                            n > 0.5*n_of_agents)),
                                not gr.nodes[node]["bought"], n
                        )
                ):

                    graph.nodes[node]["bought"] = 1
                    m += 1
        n += m
        n_per_time_step.append(_get_sales_in_groups(graph))

    return graph, n_per_time_step


def plot_sales(n_per_time_step):
    """
    Plots number of sales
    :param n_per_time_step: number of sales in time
    :type n_per_time_step: list
    """
    plt.plot([sum(x.values()) for x in n_per_time_step])
    plt.show()


def plot_new_sales_per_group(n_per_time_step):
    in_sales = [n_per_time_step[x]["innovators"] - n_per_time_step[x - 1]["innovators"] if x > 0
                else n_per_time_step[x]["innovators"] for x in range(len(n_per_time_step))]
    im_sales = [n_per_time_step[x]["imitators"] - n_per_time_step[x - 1]["imitators"] if x > 0
                 else n_per_time_step[x]["imitators"] for x in range(len(n_per_time_step))]
    plt.plot(in_sales)
    plt.plot(im_sales)
    plt.show()


def mc_new_sales_per_group(MC=50):
    """
    Plots new adopters in monte carlo
    :param MC: number of Monte Carlo repetitions
    :type MC: int
    """
    in_sales_all, im_sales_all, all = [], [], []
    for i in range(MC):
        graph, n_per_time_step = \
            bass_model(p=0.35, q=0.4, k=8, type_name='barabasi_albert', no_of_innovators=130, n_of_agents=700)
        in_sales = [n_per_time_step[x]["innovators"] - n_per_time_step[x - 1]["innovators"] if x > 0
                    else n_per_time_step[x]["innovators"] for x in range(len(n_per_time_step))]
        im_sales = [n_per_time_step[x]["imitators"] - n_per_time_step[x - 1]["imitators"] if x > 0
                    else n_per_time_step[x]["imitators"] for x in range(len(n_per_time_step))]

        in_sales_all.append(in_sales)
        im_sales_all.append(im_sales)

    plt.plot(_column_wise_avg(in_sales_all))
    plt.plot(_column_wise_avg(im_sales_all))
    plt.plot(np.add(_column_wise_avg(in_sales_all), _column_wise_avg(im_sales_all)))
    plt.legend(['innovators', 'imitators', 'all'])
    plt.xlabel('time steps')
    plt.ylabel('new adopters')
    plt.title('new adopters in time')
    plt.show()


def _split_community_to_innovators_and_imitators(graph, no_of_innovators):
    '''
    function that sets attributes for all nodes regarding whether they are imitators or innovators
    :param graph: graph class
    :type graph: graph
    :param no_of_innovators: number of innovators
    :type no_of_innovators: int
    :return: networkx graph instance
    '''
    no_of_nodes = len(list(graph.nodes(data=True)))
    innovators = sample(range(1, no_of_nodes+1), k=no_of_innovators)
    for i in range(1, no_of_nodes + 1):
        if i in innovators:
            graph.nodes[i - 1]["type"] = 1
        else:
            graph.nodes[i - 1]["type"] = 0
        graph.nodes[i - 1]["bought"] = 0

    return graph


def _get_sales_in_groups(graph):
    """
    Counts sales for innovator agents and imitators.
    :param graph: networkx graph object
    :type graph: networkx graph object instance
    :return: dictionary with numbers of sales per group
    :rtype: dict
    """
    sales = {"innovators": 0, "imitators": 0}
    for n in range(len(list(graph.nodes(data=True)))):
        if graph.nodes[n]["type"] and graph.nodes[n]["bought"]:
            sales["innovators"] += 1
        elif not graph.nodes[n]["type"] and graph.nodes[n]["bought"]:
            sales["imitators"] += 1
    return sales


def _column_wise_avg(rows):
    columns = zip_longest(*rows, fillvalue=0)
    return [sum(col) / len(rows) for col in columns]
