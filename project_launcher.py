import datetime
import os

import matplotlib as mpl
import networkx as nx
import spicy as sp
from matplotlib import pyplot as plt
from networkx.algorithms.community import louvain_communities

from explore.exploration_graph import ExploreGraph as eg, ExploreGraph
from persistence.persistence_graph import PersistenceGraph
from visualization.visualization_graph import VisualizationGraph as vg
from analytics.analytics_graph import AnalyticsGraph as ag, AnalyticsGraph
from preprocessing.pre_processing_graph import PreProcessGraph as pg, PreProcessGraph
from export.export_graph import ExportGraph as xg


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

    # It exisits 5 scenario to test the project:
    # scenario = 1 - Display all information and steps of the pre-processing of the dataset
    # scenario = 2 - Display all information and steps of the community detection
    # scenario = 3 - Display all information and steps of the visualization of our graph
    # scenario = 4 - Display all information and steps of the exploration of our graph
    # scenario = 5 - Display all information and steps of all our project
    scenario = 1

    if scenario == 1:
        print(">>Display all information and steps of the pre-processing of the dataset **************************\n\n")
        eg = ExploreGraph()
        #pg = PreProcessGraph()

        print("\nConstruction of the graph_original and display of its efficiency :")
        graph_original = eg.construct_graph_by_file(file_name="./dataset/origine_dataset/amazon-meta.txt")
        pg.display_efficiency_of_graph(graph=graph_original)

        print("\nConstruction of the graph_sampled_big and display of its efficiency :")
        graph_sampled_big = eg.construct_graph_by_file(file_name="./dataset/dataset_off_amazon_big.txt")
        pg.display_efficiency_of_graph(graph=graph_sampled_big)

        print("\nConstruction of the graph_sampled_small and display of its efficiency :")
        graph_sampled_small = eg.construct_graph_by_file(file_name="./dataset/dataset_off_amazon_small.txt")
        pg.display_efficiency_of_graph(graph=graph_sampled_small)


        print("\nConstruction of the graph_sampled_enhanced and display of its efficiency :")
        #graph_sampled_enhanced = eg.construct_graph_by_file("./dataset/dataset_off_amazon_enhanced.txt")
        #pg.display_efficiency_of_graph(graph=graph_sampled_enhanced)


    elif scenario == 2:
        print(">>Display all information and steps of the community detection ************************************\n\n")
        eg = ExploreGraph()
        #pg = PreProcessGraph()
        #ag = AnalyticsGraph()

        # CONSTRUCTION OF THE GRAPHS ===================================================================================
        print("\nConstruction of the graph_sampled_big and display of its efficiency :")
        graph_sampled_big = eg.construct_graph_by_file(file_name="./dataset/dataset_off_amazon_big.txt")
        pg.display_efficiency_of_graph(graph=graph_sampled_big)

        print("\nConstruction of the graph_sampled_enhanced and display of its efficiency :")
        #graph_sampled_enhanced = eg.construct_graph_by_file("./dataset/dataset_off_amazon_enhanced.txt")
        #pg.display_efficiency_of_graph(graph=graph_sampled_enhanced)

        # COMMUNITY DETECTION SIMPLE==================================================================================
        communities_homemade_big_simple = ag.homemade_community_detection(graph=graph_sampled_big, display=False)
        # communities_homemade_big_simple = ag.homemade_community_detection(graph=graph_sampled_enhanced, display=False)

        # COMMUNITY DETECTION HOMEMADE==================================================================================
        communities_homemade_big_homemade = ag.amazon_community_detection(graph_sampled_big, tag="graph_sampled_big", run_silhouette=False, display=False)
        #communities_homemade_enhanced_homemade = ag.amazon_community_detection(graph_sampled_enhanced, tag="display_efficiency_of_graph", run_silhouette=False, display=False)

        # COMMUNITY DETECTION LIBRARY==================================================================================
        communities_library_big = louvain_communities(graph_sampled_big, seed=127)
        #communities_library_enhanced = louvain_communities(graph_sampled_enhanced, seed=127)

        # QUALITY=======================================================================================================
        accuracy, precision, recall, jaccard = ag.accuracy_precision_recall_jaccard(communities_library_big, communities_homemade_big_simple, display=False)
        accuracy, precision, recall, jaccard = ag.accuracy_precision_recall_jaccard(communities_library_big, communities_homemade_big_homemade, display=False)
        #accuracy, precision, recall, jaccard = ag.accuracy_precision_recall_jaccard(communities_library_enhanced, communities_homemade_big_simple, display=False)
        #accuracy, precision, recall, jaccard = ag.accuracy_precision_recall_jaccard(communities_library_enhanced, communities_homemade_enhanced_homemade, display=False)


    elif scenario == 3:
        print(">>Display all information and steps of the visualization of our graph *****************************\n\n")
    elif scenario == 4:
        print(">>Display all information and steps of the exploration of our graph *******************************\n\n")
    else:
        print(">>Display all information and steps of all our project ********************************************\n\n")
