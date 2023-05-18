import datetime
import re

import networkx as nx
from explore.exploration_graph import ExploreGraph as eg, ExploreGraph
import csv


class ExportGraph:

    def create_dataset(graph, name):
        """
        Creator : Sophie Caroni
        reviewed by : Quentin Nater
        Create a .txt dataset with the for our analysis meaningful information only
        :param graph: networkX - Graph networkX of the amazon dataset
        :type graph: networkX
        :param name: string - name inside the dataset file
        :type name: string
        :return: -
        """

        current_time = datetime.datetime.now()
        print(">> You have called the export of your graph, (at", current_time, "), please wait...")

        # Create new .txt file
        with open("./dataset/"+str(name)+".txt", "w", encoding="utf-8") as file:

            # Retrieve ASIN from node
            asin_lst = graph.nodes()

            # For every ASIN, retrieve its similars
            for asin in asin_lst:
                sim_lst = []
                for adj in graph.edges():
                    if asin == adj[0]:
                        sim_lst.append(adj[1])

                # Define the entries of the file for ASIN having similars
                if len(sim_lst) != 0:
                    entries = ["ASIN: "+str(asin), "  similar: " + str(len(sim_lst)) + "  " + "  ".join(str(i) for i in sim_lst)]

                # Define the entries of the file for ASIN not having similars
                elif len(sim_lst) == 0:
                    entries = ["ASIN: " + str(asin), "  similar: " + str(len(sim_lst))]

                # Write the file sticking to the correct (original) nomenclature
                for entry in entries:
                    file.write(entry)
                    file.write('\n')
                file.write('\n')

        current_time = datetime.datetime.now()
        print(">> Job done, the refined graph in this directory './dataset/', (at", current_time, "), thank you...")

        return

    def enrich_graph(graph, dataset_name, enhanced_dataset):
        """
        Creator : Sophie Caroni
        reviewed by : Quentin Nater
        Merge the graph with enriched graph
        :param graph: networkX - Graph networkX of the amazon dataset
        :type graph: networkX
        :param dataset_name: string - Name of the future exported file
        :type dataset_name: string
        :param enhanced_dataset: string - Name of the enhanced dataset made to improve the current graph
        :type enhanced_dataset: string
        :return: -
        """

        current_time = datetime.datetime.now()
        print(">> You have called the enhancement of your graph, (at", current_time, "), please wait...")

        # initialization of the variables
        i, asin_int = 0, 0
        list_asin, list_similars = [], []

        # read every information of the file (dataset)
        with open(enhanced_dataset, "r", encoding='utf-8') as f:
            for line in f:

                i += 1  # inc break

                # read nodes ===============================================
                match = re.search(r'ASIN:\s*(\w+)', line)  # each ASIN
                if match:
                    asin = match.group(1)  # Take the first element matched

                    # add a node to the graph for the ASIN value (INT)
                    asin_int = ExploreGraph.convert_asin_to_int(asin)
                    graph.add_node(asin_int)
                    list_asin.append(asin_int)

                # read edges ===============================================
                match = re.search(r'similar:\s*(\w+)', line)  # each similar
                if match:
                    similars = line.split(sep="  ")  # Create a list of each one of the similars as an element
                    inc = 0

                    for similar in similars:
                        inc += 1

                        if inc > 2:  # skip two initial blank spaces; only if there are more than 0 similars
                            similar_int = ExploreGraph.convert_asin_to_int(similar)  # casting
                            list_similars.append(similar_int)
                            graph.add_edge(*(asin_int, similar_int))  # Add edges between the asin product and each of its similar ones

        nNodes, nEdges = graph.number_of_nodes(), graph.number_of_edges()
        print("\t\tThe graph has been successfully constructed! (nodes:" + str(nNodes) + ", edges:" + str(nEdges) + ")")

        ExportGraph.create_dataset(graph, str(dataset_name) + "_enhanced")

        current_time = datetime.datetime.now()
        print(">> The enhancement of your graph has been made, (at", current_time, "), thank you...")

        return graph


