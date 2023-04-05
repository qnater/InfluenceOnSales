import networkx as nx
from networkx.algorithms.clique import find_cliques
from networkx.algorithms.community import girvan_newman, louvain_communities, k_clique_communities


class AnalyticsGraph:

    # Creator : Quentin Nater
    # reviewed by : Sophie Caroni
    #
    # myGraph       : networkX - graph of the dataset
    #
    # Calculate the betweenness centrality of a graph using the networkx library
    def centrality_betweenness_library(graph):
        print(">> You have called the betweenness centrality library for your graph.")

        nodes = nx.betweenness_centrality(
            graph)  # Centrality dictionary: node as key and its betweenness centrality as value

        for node in nodes.keys():
            if round(nodes[node], 2) > 0.0:
                print("\t\t\t\t" + str(node) + " : " + str(round(nodes[node], 3)))
        else:
            print("\t\t\t\t Result: There are no central nodes.")

        return nodes




    # Creator : Quentin Nater
    # reviewed by :
    #
    # myGraph       : networkX - graph of the dataset
    # library       : Library choosen
    #
    # Detect communities with a specific library
    def community_library_detection(graph, library="Default"):
        print(">> You have called the community detection with ", library, " settings")

        # Library: community.girvan_newman
        if library == "girvanNewman":
            communitiesGirvanNewman = girvan_newman(graph)
            for c in communitiesGirvanNewman:
                print("Cliques results", c)

        # Library: louvain_communities
        if library == "louvain":
            communitiesLouvain = louvain_communities(graph, seed=123)
            for c in communitiesLouvain:
                print("Cliques results" , c)

        return ""
