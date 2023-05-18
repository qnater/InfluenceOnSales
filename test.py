import datetime
import os

import matplotlib as mpl
import networkx as nx
import spicy as sp
from matplotlib import pyplot as plt
from networkx.algorithms.community import louvain_communities

from enrichment.enrichment_graph import EnrichmentGraph
from explore.exploration_graph import ExploreGraph as eg, ExploreGraph
from persistence.persistence_graph import PersistenceGraph
from visualization.visualization_graph import VisualizationGraph as vg
from analytics.analytics_graph import AnalyticsGraph as ag, AnalyticsGraph
from preprocessing.pre_processing_graph import PreProcessGraph as pg, PreProcessGraph
from export.export_graph import ExportGraph as xg, ExportGraph

if __name__ == '__main__':
    print("\n=========================================================================================")
    print("========================INFLUENCE=OF=POPULARITY=ON=SALES===UNI-FR========================")
    print("==================================UNIT=TEST=CIRCLE_CI====================================\n")

    if os.name == "nt":
        mpl.use('TkAgg')  # without it, cannot run my plots (maybe personal)
    elif os.name == "posix":
        print("Choosing a Mac really is the worst thing you've done in life!")
    else:
        print("Unknown operating system.")

    er, eg = EnrichmentGraph(), ExploreGraph()
    graph = eg.construct_graph_by_file(file_name="./dataset/dataset_off_amazon_big.txt")

    merged = er.merge_for_enchirment(original_graph=graph, enchriment_file="formatted_amazon_meta.txt")

    ExportGraph.create_dataset(graph=merged, name="dataset_off_amazon_enrichment")




