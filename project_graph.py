import matplotlib as mpl
import networkx as nx
import spicy as sp

from explore.exploration_graph import ExploreGraph as eg
from visualization.visualization_graph import VisualizationGraph as vg
from analytics.analytics_graph import AnalyticsGraph as ag
from export.export_graph import ExportGraph as xg

# QUENTIN NATER - 01.03.2023 - ASS 1 - EX 2
if __name__ == '__main__':
    print("\n=========================================================================================")
    print("========================INFLUENCE=OF=POPULARITY=ON=SALES===UNI-FR========================")
    print("=========================================================================================\n")

    # mpl.use('TkAgg')  # without it, cannot run my plots (maybe personal)

    tag = "prod"  # prod or test

    if tag == "test":
        test = "test \n ciao"
        result = test.strip("\n")
        print(result)
        # myGraph = nx.DiGraph()
        # myGraph.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8])
        # myGraph.add_edges_from([(1, 2), (1, 4), (1, 5),
        #                         (2, 5),
        #                         (3, 6), (3, 7),
        #                         (4, 5), (4, 2), (4, 3),
        #                         (5, 7),
        #                         (6, 5), (6, 7),
        #                         ])
        # vg.display_simple_graph(myGraph, False)
        # xg.create_dataset(myGraph)
    elif tag == "prod":
        graph = eg.construct_graph_by_file("./dataset/small_amazon.txt") # limit=20000
        xg.create_dataset(graph)
        graph = eg.construct_graph_by_file("./dataset/amazon_refined.txt") # limit=20000
        vg.display_simple_graph(graph, True)
        ag.centrality_betweenness_library(graph)
