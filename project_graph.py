import os

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



    if os.name == "nt":
        mpl.use('TkAgg')  # without it, cannot run my plots (maybe personal)
    elif os.name == "posix":
        print("Sorry bro about you MAC...")
    else:
        print("Unknown operating system.")

    tag = "prod"  # prod or test

    if tag == "test":
        graph = eg.construct_graph_by_file("./dataset/amazon_refined.txt")
        ag.community_library_detection()

    if tag == "test2":
        graph = eg.construct_graph_by_file("./dataset/amazon_refined.txt")
        pg.display_score_by_degree(graph, 100, 10)
        pg.remove_nodes_by_degree(graph, 1)

    elif tag == "staging":
        graph = eg.construct_graph_by_file("./dataset/amazon-meta.txt")
        graph = pg.refined_graph(graph)
        xg.create_dataset(graph)

    elif tag == "prod":
        graph = eg.construct_graph_by_file("./dataset/amazon_refined.txt")
        vg.display_simple_graph(graph, False)
        ag.community_library_detection(graph, "girvanNewman")
        #ag.centrality_betweenness_library(graph)
