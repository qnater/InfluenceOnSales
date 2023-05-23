import os
import matplotlib as mpl
from enrichment.enrichment_graph import EnrichmentGraph
from explore.exploration_graph import ExploreGraph
from export.export_graph import ExportGraph

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

    er, eg, ex = EnrichmentGraph(), ExploreGraph(), ExportGraph()
    graph = eg.construct_graph_by_file(file_name="./dataset/dataset_off_amazon_big.txt")
    merged = er.merge_for_enrichment(original_graph=graph, enrichment_file="formatted_amazon_meta.txt")
    ex.create_dataset(graph=merged, name="dataset_off_amazon_enrichment_3")
