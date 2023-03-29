import networkx as nx
from explore.exploration_graph import ExploreGraph as eg

myGraph = nx.DiGraph()
myGraph.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8])
myGraph.add_edges_from([(1, 2), (1, 4), (1, 5),
                        (2, 5),
                        (3, 6), (3, 7),
                        (4, 5), (4, 2), (4, 3),
                        (5, 7),
                        (6, 5), (6, 7),
                        ])

nx.draw(myGraph, with_labels=True)



class ExportGraph:

    # Creator : Sophie Caroni
    # reviewed by :
    #
    # graph       : networkX - graph of the dataset
    #
    # Convert (back) int ASIN to original ASIN
    # def convert_int_to_asin(int):
    #     alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    #     if any(char.isalpha() for char in asin): # isalpha() returns True if it detects letters
    #         for char in asin:
    #             if char.isalpha():
    #                 asin = asin.replace(char, str(alphabet.index(char.upper()) + 10))
    #
    #     return int(asin)


    # Creator : Sophie Caroni
    # reviewed by :
    #
    # graph       : networkX - graph of the dataset
    #
    # Create a .txt dataset with the for our analysis meaningful informations only
    def create_dataset(graph):

        # Create new .txt file
        with open("./dataset/amazon_refined.txt", "w", encoding="utf-8") as file:

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

        return




