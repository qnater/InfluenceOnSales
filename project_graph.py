from sys import platform

import matplotlib as mpl
import networkx as nx
import spicy as sp
from matplotlib import pyplot as plt

from explore.exploration_graph import ExploreGraph as eg
from visualization.visualization_graph import VisualizationGraph as vg
from analytics.analytics_graph import AnalyticsGraph as ag
from preprocessing.pre_processing_graph import PreProcessGraph as pg
from export.export_graph import ExportGraph as xg

# QUENTIN NATER - 01.03.2023
if __name__ == '__main__':
    print("\n=========================================================================================")
    print("========================INFLUENCE=OF=POPULARITY=ON=SALES===UNI-FR========================")
    print("=========================================================================================\n")

    if platform.system() == "Windows":
        mpl.use('TkAgg')  # without it, cannot run my plots (maybe personal)
    elif platform.system() == "Darwin":
        print("Sorry, my bro...")
    else:
        print("Unknown operating system.")

    mpl.use('TkAgg')  # without it, cannot run my plots (maybe personal)

    tag = "staging"  # prod or test

    if tag == "test":
        graph = nx.DiGraph()
        graph.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8])
        graph.add_edges_from([(1, 2), (1, 4), (1, 5),
                                (2, 5),
                                (3, 6), (3, 7),
                                (4, 5), (4, 2), (4, 3),
                                (5, 7),
                                (6, 5), (6, 7),
                                ])

        graph = pg.refined_graph(graph)

        xg.create_dataset(graph)

        graph = eg.construct_graph_by_file("./dataset/amazon_refined.txt")

        vg.display_simple_graph(graph, True)

        ag.centrality_betweenness_library(graph)

    elif tag == "staging":
        graph = eg.construct_graph_by_file("./dataset/amazon-meta.txt")
        graph = pg.refined_graph(graph)
        xg.create_dataset(graph)

    elif tag == "prod":
        graph = eg.construct_graph_by_file("./dataset/amazon_refined.txt")
        vg.display_simple_graph(graph, True)
        ag.centrality_betweenness_library(graph)
