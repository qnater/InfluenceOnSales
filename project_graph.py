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
        print("Sorry bro about your MAC...")
    else:
        print("Unknown operating system.")

    tag = "analyse"  # prod or test

    if tag == "test":
        graph = eg.construct_graph_by_file("./dataset/amazon_refined.txt")
        ag.community_library_detection()

    elif tag == "analyse":
        graph = eg.construct_graph_by_file("./dataset/amazon_refined.txt")
        vg.display_simple_graph(graph, False)
        pg.remove_nodes_by_degree(graph, 4)
        ag.community_library_detection(graph, "louvain")
        #ag.centrality_betweenness_library(graph)

    elif tag == "staging":
        graph = eg.construct_graph_by_file("./dataset/amazon-meta.txt")
        graph = pg.refined_graph(graph)
        xg.create_dataset(graph)

    elif tag == "prod":
        graph = nx.Graph()
        graph.add_nodes_from(["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"])
        graph.add_edges_from([("0", "2"),("0", "4"),("0", "3"),("0", "5"),
                              ("1", "2"),("1", "4"),("1", "7"),
                              ("2", "4"), ("2", "5"), ("2", "6"),
                              ("3", "7"),
                              ("4", "10"),
                              ("4", "10"),
                              ("5", "7"),("5", "11"),
                              ("6", "7"),("6", "11"),
                              ("8", "11"), ("8", "9"),("8", "14"),("8", "15"),("8", "10"),
                              ("9", "12"), ("9", "14"),
                              ("10", "14"), ("10", "12"), ("10", "11"), ("10", "13"),
                              ("11", "13")])

        #graph = eg.construct_graph_by_file("./dataset/amazon_refined.txt")
        vg.display_simple_graph(graph, False)
        #pg.remove_nodes_by_degree(graph, 4)
        ag.homemade_community_detection(graph)
