import os

import matplotlib as mpl
import networkx as nx
import spicy as sp
from matplotlib import pyplot as plt
from networkx.algorithms.community import louvain_communities

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
        print("Choosing a Mac really is the worst thing you've done in life!")
    else:
        print("Unknown operating system.")

    tag = "explore"  # prod or test

    if tag == "test":
        graph = eg.construct_graph_by_file("./dataset/amazon_refined.txt")
        ag.community_library_detection()

    if tag == "explore":
        graphFat = eg.construct_graph_by_file("./dataset/amazon_refined.txt")
        vg.display_simple_graph(graphFat, False)
        pg.remove_nodes_by_degree(graphFat, 5)
        graphFat = pg.refined_graph(graphFat)

        graph = nx.Graph()
        graph.add_nodes_from(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"])
        graph.add_edges_from([("0", "2"), ("0", "4"), ("0", "3"), ("0", "5"),
                              ("1", "2"), ("1", "4"), ("1", "7"),
                              ("2", "4"), ("2", "5"), ("2", "6"),
                              ("3", "7"),
                              ("4", "10"),
                              ("5", "7"), ("5", "11"),
                              ("6", "7"), ("6", "11"),
                              ("8", "11"), ("8", "9"), ("8", "14"), ("8", "15"), ("8", "10"),
                              ("9", "12"), ("9", "14"),
                              ("10", "14"), ("10", "12"), ("10", "11"), ("10", "13"),
                              ("11", "13")])

        #results = ag.deep_analyze(graphFat, [], True)
        #for dic_r in results:
        #    print("\t\t\t\t(ANL) : ", dic_r[0][0], "\t\t\t\t :", dic_r[1][0])

        eg.analytics_exploration(graphFat, False)

        vg.display_simple_graph(graphFat, False)

        communities = ag.homemade_community_detection(graphFat, False)

        for community in communities:
            eg.exploreCommunity(graphFat, community, False)

        popular_nodes = ag.highest_betweenness_centrality_scores(graphFat, communities, False)

        vg.display_communities_graph(graphFat, communities, popular_nodes)

        vg.degree_distribution(graphFat, True)


    elif tag == "analyse":
        graph = eg.construct_graph_by_file("./dataset/amazon_refined.txt")
        vg.display_simple_graph(graph, False)
        pg.remove_nodes_by_degree(graph, 4)
        ag.community_library_detection(graph, "louvain")
        # ag.centrality_betweenness_library(graph)

    elif tag == "staging":
        graph = eg.construct_graph_by_file("./dataset/amazon-meta.txt")
        graph = pg.refined_graph(graph)
        xg.create_dataset(graph)

    elif tag == "prod":
        graph = nx.Graph()
        graph.add_nodes_from(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"])
        graph.add_edges_from([("0", "2"), ("0", "4"), ("0", "3"), ("0", "5"),
                              ("1", "2"), ("1", "4"), ("1", "7"),
                              ("2", "4"), ("2", "5"), ("2", "6"),
                              ("3", "7"),
                              ("4", "10"),
                              ("5", "7"), ("5", "11"),
                              ("6", "7"), ("6", "11"),
                              ("8", "11"), ("8", "9"), ("8", "14"), ("8", "15"), ("8", "10"),
                              ("9", "12"), ("9", "14"),
                              ("10", "14"), ("10", "12"), ("10", "11"), ("10", "13"),
                              ("11", "13")])

        graph2 = nx.Graph()
        graph2.add_nodes_from(["1", "2", "3", "4", "5", "6", "7", "8"])
        graph2.add_edges_from([("1", "2"), ("1", "4"),
                               ("2", "4"),
                               ("1", "3"), ("3", "4"), ("2", "3"),
                               ("3", "5"),
                               ("5", "7"),
                               ("5", "8"), ("5", "6"),
                               ("6", "7"), ("6", "8")])

        graph3 = eg.construct_graph_by_file("./dataset/amazon_refined.txt")
        pg.remove_nodes_by_degree(graph3, 5)

        # vg.display_simple_graph(graph2, display=False)
        # ag.community_library_detection(graph2, library="modularity")

        communities = ag.homemade_community_detection(graph3, True)
        ag.compare_algo_efficiency(graph3, communities)
        # ag.compare_algo_efficiency(graph3, communities)
