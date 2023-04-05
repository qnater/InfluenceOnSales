import networkx as nx
from explore.exploration_graph import ExploreGraph as eg


class ExportGraph:

    def create_dataset(graph):
        """
        Creator : Sophie Caroni
        reviewed by :
        Create a .txt dataset with the for our analysis meaningful information only
        :param graph: networkX - Graph networkX of the amazon dataset
        :type graph: networkX
        :return: -
        """

        print(">> You have called the export of your graph, please wait :)")

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

        print(">> You can find your refined graph in this directory './dataset/', please enjoy ;)")

        return