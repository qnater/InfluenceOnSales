import os
import matplotlib as mpl

from analytics.analytics_graph import AnalyticsGraph
from explore.exploration_graph import ExploreGraph as eg, ExploreGraph
from export.export_graph import ExportGraph
from persistence.persistence_graph import PersistenceGraph

if __name__ == '__main__':
    print("\n=========================================================================================")
    print("========================INFLUENCE=OF=POPULARITY=ON=SALES===UNI-FR========================")
    print("==================================UNIT=TEST=CIRCLE_CI====================================\n")

    if os.name == "nt":
        mpl.use('TkAgg')
        print("Windows profile has been loaded.")
    elif os.name == "posix":
        print("Mac profile has been loaded.")
    else:
        print("Unknown operating system.")

    db, eg, ag, ex = PersistenceGraph(), ExploreGraph(), AnalyticsGraph(), ExportGraph()

    graph, run_time = eg.construct_graph_by_file(file_name="./dataset/dataset_off_amazon_big.txt")

    algorithms = ["louvain", "modularities", "girvanNewman"]

    for algo in algorithms:
        communities, run_time = ag.community_library_detection(graph=graph, library=algo, display=False)
        silhouette = ag.silhouette_score(graph=graph, communities=communities, metric="euclidean", sample_size=1000)
        ex.export_communities_results(run_time, communities, [], 0, 0, 0, 0, silhouette, "compare_algo_"+algo, "x")



