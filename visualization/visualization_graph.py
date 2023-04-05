import random
import time
from tqdm import tqdm

import matplotlib.pyplot as plt
import networkx as nx


class VisualizationGraph:

    # Creator : Quentin Nater
    # reviewed by :
    #
    # myGraph       : networkX - graph of the dataset
    # display       : bool - display the plot
    #
    # Display a simple graph
    def display_simple_graph(myGraph, display=True):

        if display:
            nx.draw(myGraph, with_labels=True)
            plt.show()

        return myGraph

    # Creator : Quentin Nater
    # reviewed by :
    #
    # myGraph       : networkX - graph of the dataset
    # display       : bool - display the plot
    #
    # Display a sampled graph
    def display_sampled_graph(myGraph, display=True):
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

    def display_progress(self):
        total_seconds = 10
        progress_bar = tqdm(total=total_seconds)

        for i in range(total_seconds):
            time.sleep(1)  # Wait for one second
            progress_bar.update(1)  # Update the progress bar

        progress_bar.close()
