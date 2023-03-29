import matplotlib as mpl
import networkx as nx
import spicy as sp
from matplotlib import pyplot as plt

from explore.exploration_graph import ExploreGraph as eg
from visualization.visualization_graph import VisualizationGraph as vg
from analytics.analytics_graph import AnalyticsGraph as ag
from preprocessing.pre_processing_graph import PreProcessGraph as pg

# QUENTIN NATER - 01.03.2023
if __name__ == '__main__':
    print("\n=========================================================================================")
    print("========================INFLUENCE=OF=POPULARITY=ON=SALES===UNI-FR========================")
    print("=========================================================================================\n")

    mpl.use('TkAgg')  # without it, cannot run my plots (maybe personal)

    tag = "prod"  # prod or test

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
        vg.display_simple_graph(graph, False)

        nodes = nx.betweenness_centrality(graph)

        print(nodes)


    elif tag == "prod":
        graph = eg.construct_graph_by_file("./dataset/amazon-meta.txt")
        graph = pg.refined_graph(graph)
        vg.display_simple_graph(graph, False)
        ag.centrality_betweenness_library(graph)
