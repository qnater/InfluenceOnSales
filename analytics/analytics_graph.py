import networkx as nx
from networkx.algorithms.clique import find_cliques
from networkx.algorithms.community import girvan_newman, louvain_communities, k_clique_communities, \
    greedy_modularity_communities, modularity


class AnalyticsGraph:


    def centrality_betweenness_library(graph):
        """
        Creator : Quentin Nater
        reviewed by :
        Calculate the betweenness centrality of a graph using the networkx library
        :param graph: networkX - Graph networkX of the amazon dataset
        :type graph: networkX
        :return: nodes with the betweenness centrality
        """

        print(">> You have called the betweenness centrality library for your graph.")

        nodes = nx.betweenness_centrality(
            graph)  # Centrality dictionary: node as key and its betweenness centrality as value

        for node in nodes.keys():
            if round(nodes[node], 2) > 0.0:
                print("\t\t\t\t" + str(node) + " : " + str(round(nodes[node], 3)))
        else:
            print("\t\t\t\t Result: There are no central nodes.")

        return nodes




    def community_library_detection(graph, library="Default"):
        """
        Creator : Quentin Nater
        reviewed by :
        Detect communities with a specific library
        :param graph: networkX - Graph networkX of the amazon dataset
        :type graph: networkX
        :param library: String - Library chosen (girvanNewman;louvain)
        :type graph: String
        :return: The display of the result
        """
        print(">> You have called the community detection with ", library, " settings")

        # Library: community.girvan_newman
        if library == "girvanNewman":
            communitiesGirvanNewman = girvan_newman(graph, seed=123)
            for c in communitiesGirvanNewman:
                print("Cliques results", c)

        # Library: louvain_communities
        if library == "louvain":
            communitiesLouvain = louvain_communities(graph, seed=123)
            for c in communitiesLouvain:
                print("Cliques results" , c)

        # Library: greedy_modularity_communities
        if library == "louvain":
            communities = greedy_modularity_communities(graph)
            modularity_score = modularity(graph, communities)
            print("Modularity score:", modularity_score)


        return ""
