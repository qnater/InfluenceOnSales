import os
import matplotlib as mpl

from explore.exploration_graph import ExploreGraph as eg, ExploreGraph
from persistence.persistence_graph import PersistenceGraph

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

    db, eg= PersistenceGraph(), ExploreGraph()

    graph = eg.construct_graph_by_file(file_name="./dataset/dataset_off_amazon_big.txt")

    communities = db.populate_database(graph=graph, delete_previous=True, communities=set(), compute_community=True)
    db.display_hypernodes_communities(graph=graph, communities=communities, compute_community=False, delete_previous=False)

