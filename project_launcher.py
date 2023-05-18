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

    eg = ExploreGraph()

    # It exists 5 scenario to test the project:
    # scenario = 1 - Display all information and steps of the pre-processing of the dataset
    # scenario = 2 - Display all information and steps of the community detection
    # scenario = 3 - Display all information and steps of the visualization of our graph
    # scenario = 4 - Display all information and steps of the exploration of our graph
    # scenario = 5 - Display all information and steps of all our project
    scenario = 5

    if scenario == 1:
        print(">>Display all information and steps of the pre-processing of the dataset **************************\n\n")

        print("\nConstruction of the graph_original and display of its efficiency :")
        # CONSTRUCTION OF THE GRAPH ====================================================================================
        graph_original = eg.construct_graph_by_file(file_name="./dataset/origine_dataset/amazon-meta.txt")
        # QUALITY OF THE GRAPH =========================================================================================
        pg.display_efficiency_of_graph(graph=graph_original)

        print("\nConstruction of the graph_sampled_big and display of its efficiency :")
        # CONSTRUCTION OF THE GRAPH ====================================================================================
        graph_sampled = eg.construct_graph_by_file(file_name="./dataset/dataset_off_amazon_big.txt")
        # QUALITY OF THE GRAPH =========================================================================================
        pg.display_efficiency_of_graph(graph=graph_sampled)

        print("\nConstruction of the graph_sampled_small and display of its efficiency :")
        # CONSTRUCTION OF THE GRAPH ====================================================================================
        graph_sampled_small = eg.construct_graph_by_file(file_name="./dataset/dataset_off_amazon_small.txt")
        # QUALITY OF THE GRAPH =========================================================================================
        pg.display_efficiency_of_graph(graph=graph_sampled_small)


    elif scenario == 2:
        print(">>Display all information and steps of the community detection ************************************\n\n")

        # CONSTRUCTION OF THE GRAPH ====================================================================================
        graph_sampled = eg.construct_graph_by_file(file_name="./dataset/dataset_off_amazon_big.txt")

        # QUALITY OF THE GRAPH =========================================================================================
        pg.display_efficiency_of_graph(graph=graph_sampled)

        # COMMUNITY DETECTION===========================================================================================
        # simple function homemade for community detection (bad)________________________________________________________
        communities_simple = ag.homemade_community_detection(graph=graph_sampled, display=False)

        # homemade community detection with research (weight) optimal __________________________________________________
        communities_homemade = ag.amazon_community_detection(graph=graph_sampled, tag="community_detection_scenario", run_silhouette=False, display=False)

        # networkX community detection louvain _________________________________________________________________________
        communities_library = ag.community_library_detection(graph=graph_sampled, library="louvain", display=False)

        # POPULAR ======================================================================================================
        popular_nodes_simple = ag.highest_betweenness_centrality_scores(graph=graph_sampled, communities=communities_simple, display=False)
        popular_nodes_homemade = ag.highest_betweenness_centrality_scores(graph=graph_sampled, communities=communities_homemade, display=False)
        popular_nodes_library = ag.highest_betweenness_centrality_scores(graph=graph_sampled, communities=communities_library, display=False)

        # QUALITY=====ACCURACY=PRECISION=RECALL=JACCARD=================================================================
        acc_simple, pre_simple, rec_simple, jac_simple = ag.accuracy_precision_recall_jaccard(communities_library=communities_library, community_homemade=communities_simple, display=False)
        acc_homemade, pre_homemade, rec_homemade, jac_homemade = ag.accuracy_precision_recall_jaccard(communities_library=communities_library, community_homemade=communities_homemade, display=False)

        # QUALITY=====SILHOUETTE========================================================================================
        silhouette_simple = ag.silhouette_score(graph=graph_sampled, community_detection=communities_simple, metric="euclidean", sample_size=1000)
        silhouette_homemade = ag.silhouette_score(graph=graph_sampled, community_detection=communities_homemade, metric="euclidean", sample_size=1000)
        silhouette_library = ag.silhouette_score(graph=graph_sampled, community_detection=communities_library, metric="euclidean", sample_size=1000)



    elif scenario == 3:
        print(">>Display all information and steps of the visualization of our graph *****************************\n\n")

        # CONSTRUCTION OF THE SMALLEST GRAPH SAMPLE ====================================================================
        graph_sampled_small = eg.construct_graph_by_file(file_name="./dataset/dataset_off_amazon_test.txt")

        # COMMUNITY DETECTION===========================================================================================
        communities = ag.amazon_community_detection(graph=graph_sampled_small, tag="visualization_scenario", run_silhouette=False, display=False)

        # POPULAR ======================================================================================================
        popular_nodes = ag.highest_betweenness_centrality_scores(graph=graph_sampled_small, communities=communities, display=False)

        # DISPLAY ALL COMMUNITY IN DIFFERENT COLOR WITH POPULAR NODE (CENTROID) IN GOLD COLOR ==========================
        vg.display_communities_graph(graph=graph_sampled_small, communities=communities, populars=popular_nodes, display=True, tag="visualization_scenario_plot")

        # DISPLAY THE DEGREE DISTRIBUTION OF THE EDGES IN THE GRAPH ====================================================
        vg.degree_distribution(graph=graph_sampled_small, display=True, tag="visualization_scenario_distribution")

        # DISPLAY EACH COMMUNITY (FOR SAKE OF TIME ONLY 10) ============================================================
        limit, number_to_display = 0, 10
        for community in communities:
            if limit >= number_to_display:
                break
            eg.explore_community(graph=graph_sampled_small, community=community, display=True)
            limit += 1

    elif scenario == 4:
        print(">>Display all information and steps of the exploration of our graph *******************************\n\n")

        # CONSTRUCTION OF THE SMALLEST GRAPH SAMPLE ====================================================================
        graph_sampled_small = eg.construct_graph_by_file(file_name="./dataset/dataset_off_amazon_test.txt")

        # EXPLORATION OF THE GRAPH =====================================================================================
        eg.analytics_exploration(graph=graph_sampled_small, display=True)


    else:
        print(">>Display all information and steps of all our project ********************************************\n\n")

        # CONSTRUCTION OF THE GRAPH ====================================================================================
        graph_sampled_small = eg.construct_graph_by_file(file_name="./dataset/dataset_off_amazon_big.txt")

        # QUALITY OF THE GRAPH =========================================================================================
        pg.display_efficiency_of_graph(graph=graph_sampled_small)

        print(">>Display all information and steps of the community detection ************************************\n\n")

        # COMMUNITY DETECTION===========================================================================================
        communities = ag.amazon_community_detection(graph=graph_sampled_small, tag="overall_scenario", run_silhouette=False, display=False)
        communities_library = ag.community_library_detection(graph=graph_sampled_small, library="louvain", display=False)

        # POPULAR ======================================================================================================
        popular_nodes = ag.highest_betweenness_centrality_scores(graph=graph_sampled_small, communities=communities, display=False)

        # QUALITY=====ACCURACY=PRECISION=RECALL=JACCARD=================================================================
        acc, pre, rec, jac = ag.accuracy_precision_recall_jaccard(communities_library=communities_library, community_homemade=communities, display=False)

        # QUALITY=====SILHOUETTE========================================================================================
        silhouette_homemade = ag.silhouette_score(graph=graph_sampled_small, community_detection=communities, metric="euclidean", sample_size=1000)

        # EXPLORATION OF THE GRAPH =====================================================================================
        eg.analytics_exploration(graph=graph_sampled_small, display=False)

        # DISPLAY ALL COMMUNITY IN DIFFERENT COLOR WITH POPULAR NODE (CENTROID) IN GOLD COLOR ==========================
        vg.display_communities_graph(graph=graph_sampled_small, communities=communities, populars=popular_nodes, display=True, tag="overall_scenario_plot")

        # DISPLAY THE DEGREE DISTRIBUTION OF THE EDGES IN THE GRAPH ====================================================
        vg.degree_distribution(graph=graph_sampled_small, display=True, tag="overall_scenario_distribution")

        # DISPLAY EACH COMMUNITY (FOR SAKE OF TIME ONLY 3) ============================================================
        limit, number_to_display = 0, 3
        for community in communities:
            if limit >= number_to_display:
                break
            eg.explore_community(graph=graph_sampled_small, community=community, display=True)
            limit += 1