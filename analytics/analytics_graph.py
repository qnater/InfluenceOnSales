import networkx as nx


class AnalyticsGraph:

    # Creator : Quentin Nater
    # reviewed by : Sophie Caroni
    #
    # graph       : networkX - graph of the dataset
    #
    # Calculate the betweenness centrality of a graph using the networkx library
    def centrality_betweenness_library(graph):
        print(">> You have called the betweenness centrality library for your graph.")

        nodes = nx.betweenness_centrality(graph) # Centrality dictionary: node as key and its betweenness centrality as value

        for node in nodes.keys():
            if round(nodes[node], 2) > 0.0:
                print("\t\t\t\t" + str(node) + " : " + str(round(nodes[node], 3)))
        else:
            print("\t\t\t\t Result: There are no central nodes.")

        return nodes