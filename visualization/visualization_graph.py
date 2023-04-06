import random

import matplotlib.pyplot as plt
import networkx as nx


class VisualizationGraph:

    def display_simple_graph(graph, display=True):
        """
        Creator : Quentin Nater
        reviewed by :
        Display a simple graph
        :param graph: networkX - graph of the dataset
        :param display: bool - display the plot
        :return: the display of the graph
        """
        if display:
            nx.draw(graph, with_labels=True)
            plt.show()

        return graph


    def display_sampled_graph(myGraph, display=True):
        """
        Creator : Quentin Nater
        reviewed by :
        Display a sample of a graph
        :param graph: networkX - graph of the dataset
        :param display: bool - display the plot
        :return: the display of the sampled graph
        """
        # number of nodes to sample
        num_nodes = 1000

        # randomly sample nodes
        nodes_list = list(myGraph.nodes())
        sampled_nodes = random.sample(nodes_list, num_nodes)

        # create a subgraph with the sampled nodes and all their edges
        sampled_graph = myGraph.subgraph(sampled_nodes)

        if display:
            # draw the sampled graph
            nx.draw(sampled_graph, with_labels=True)
            plt.show()
