import datetime
import os

import matplotlib as mpl
import networkx as nx
import spicy as sp
from matplotlib import pyplot as plt
from networkx.algorithms.community import louvain_communities

from explore.exploration_graph import ExploreGraph as eg, ExploreGraph
from persistence.persistence_graph import PersistenceGraph
from visualization.visualization_graph import VisualizationGraph as vg, VisualizationGraph
from analytics.analytics_graph import AnalyticsGraph as ag, AnalyticsGraph
from preprocessing.pre_processing_graph import PreProcessGraph as pg, PreProcessGraph
from export.export_graph import ExportGraph as xg


if __name__ == '__main__':
    print("\n=========================================================================================")
    print("========================INFLUENCE=OF=POPULARITY=ON=SALES===UNI-FR========================")
    print("==================================UNIT=TEST=CIRCLE_CI====================================\n")

    if os.name == "nt":
        mpl.use('TkAgg')  # without it, cannot run my plots (maybe personal)
    elif os.name == "posix":
        print("Choosing a Mac really is the best thing you've done in life!")
    else:
        print("Unknown operating system.")

    eg, pg, ag, vg = ExploreGraph(), PreProcessGraph(), AnalyticsGraph(), VisualizationGraph()
    print(">>Display all information and steps of all our project ********************************************\n\n")

    # CONSTRUCTION OF THE GRAPH ====================================================================================
    graph_sampled_small = eg.construct_graph_by_file(file_name="./dataset/dataset_off_amazon_test.txt")

    # QUALITY OF THE GRAPH =========================================================================================
    pg.display_efficiency_of_graph(graph=graph_sampled_small)

    print(">>Display all information and steps of the community detection ************************************\n\n")

    # COMMUNITY DETECTION===========================================================================================
    communities = ag.amazon_community_detection(graph=graph_sampled_small, tag="overall_scenario", run_silhouette=False, display=False)
    communities_library = ag.community_library_detection(graph=graph_sampled_small, library="louvain", display=False)

    # POPULAR ======================================================================================================
    popular_nodes = ag.highest_betweenness_centralities(graph=graph_sampled_small, communities=communities, display=False)

    # QUALITY=====ACCURACY=PRECISION=RECALL=JACCARD=================================================================
    acc, pre, rec, jac = ag.accuracy_precision_recall_jaccard(communities_library=communities_library, community_homemade=communities, display=False)

    # QUALITY=====SILHOUETTE========================================================================================
    silhouette_homemade = ag.silhouette_score(graph=graph_sampled_small, communities=communities, metric="euclidean", sample_size=100)

    # EXPLORATION OF THE GRAPH =====================================================================================
    eg.analytics_exploration(graph=graph_sampled_small, display=False)

    # DISPLAY ALL COMMUNITY IN DIFFERENT COLOR WITH POPULAR NODE (CENTROID) IN GOLD COLOR ==========================
    vg.display_communities_graph(graph=graph_sampled_small, communities=communities, populars=popular_nodes, display=False, tag="overall_scenario_plot")

    # DISPLAY THE DEGREE DISTRIBUTION OF THE EDGES IN THE GRAPH ====================================================
    vg.degree_distribution(graph=graph_sampled_small, display=False, tag="overall_scenario_distribution")

    # DISPLAY EACH COMMUNITY (FOR SAKE OF TIME ONLY 3) ============================================================
    limit, number_to_display = 0, 3
    for community in communities:
        if limit >= number_to_display:
            break
        eg.explore_community(graph=graph_sampled_small, community=community, display=False)
        limit += 1
