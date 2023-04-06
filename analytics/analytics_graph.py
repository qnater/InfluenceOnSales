import datetime

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
        current_time = datetime.datetime.now()
        print(">> You have called the betweenness centrality library for your graph (at", current_time, ").")

        nodes = nx.betweenness_centrality(graph)  # Centrality dictionary: node as key and its betweenness centrality as value

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
        :param library: String - Library chosen (girvanNewman;louvain;modularity)
        :type graph: String
        :return: Communities found
        """
        current_time = datetime.datetime.now()
        print(">> You have called the community detection with ", library, " (at", current_time, ")")

        communities = []

        # Library: community.girvan_newman
        if library == "girvanNewman":
            communities = girvan_newman(graph)
            for i, c in enumerate(communities):
                print("(girvanNewman) > community ", i, " : ", c)

            modularity_score = modularity(graph, communities)
            print("Modularity score:", modularity_score)


        # Library: louvain_communities
        if library == "louvain":
            communities = louvain_communities(graph, seed=123)
            for i, c in enumerate(communities):
                print("(louvain) > community ", i, " : ", c)

            modularity_score = modularity(graph, communities)
            print("Modularity score:", modularity_score)


        # Library: greedy_modularity_communities
        if library == "modularity":
            communities = greedy_modularity_communities(graph)

            for i, c in enumerate(communities):
                print("(greedy_modularity_communities) > community ", i, " : ", c)

            modularity_score = modularity(graph, communities)
            print("Modularity score:", modularity_score)

        return communities

    def homemade_modularity_gain(graph, first_community, second_community):
        """
        Creator : Sophie Caroni
        reviewed by :
        Compute modularity gain between two communities
        :param graph: networkX - Graph networkX of the amazon dataset (rafined)
        :type graph: networkX
        :param first_community: list of nodes belonging to the first community
        :type first_community: list
        :param second_community: list of nodes belonging to the first community
        :type second_community: list
        :return: modularity gain with first and second communities
        """
        n_edges = nx.number_of_edges(graph)

        # find number of neighbors of each node inside the first community
        d_i = 0
        for n in first_community:
            d_i += len(list(graph.neighbors(n)))

        # find number of neighbors of each node inside the second community
        d_j = 0
        for n in second_community:
            d_j += len(list(graph.neighbors(n)))

        # find number of shared links between first and second community
        d_ij = 0
        for n in first_community:
            for ni in graph.neighbors(n):
                if ni in second_community:
                    d_ij += 1

        for m in second_community:
            for mi in graph.neighbors(m):
                if mi in first_community:
                    d_ij += 1

        # compute modularity gain
        modularity_gain = 1 / (2 * n_edges) * (d_ij - (d_i * d_j / n_edges))

        return [modularity_gain, first_community, second_community]

    def homemade_community_detection(graph):
        """
        Creator : Quentin Nater
        reviewed by :
        Detect communities with a specific algo
        :param graph: networkX - Graph networkX of the amazon dataset (rafined)
        :type graph: networkX
        :return: Communities found
        """
        current_time = datetime.datetime.now()
        print(">> You've called the homemade (good choice) community detection (at", current_time, "), please wait <3")

        # phase 1 =====================================================================================================
        print("\n\tPhase 1 of the algo <3")
        node_0 = list(graph.nodes())[0]
        print("\t\tAlpha Node :\t\t", node_0, "(degrees->", graph.degree(node_0),")")

        community_0 = list(graph.neighbors(node_0))
        print("\t\tAlpha Community :\t", community_0)



        # phase 2 =====================================================================================================
        print("\n\tPhase 2 of the algo <3")
        print("\t\tAlpha Community :\t", community_0)

        # phase 3 =====================================================================================================
        print("\n\tPhase 3 of the algo <3")

        maxResults = []
        for node in community_0:
            maxResults.append(AnalyticsGraph.homemade_modularity_gain(graph, [node_0], [node]))

        maxValue = max(maxResults[n][0] for n in range(len(maxResults)))

        for i, values in enumerate(maxResults):
            if maxResults[i][0] == maxValue:
                newCommunity = maxResults[i][2]

        print("\t\tMax value :", maxValue, " (for ", maxResults, ")")
        print("\t\tNew Community :", newCommunity)

        newCommunity.append(node_0)



        # phase 4 =====================================================================================================
        print("\n\tPhase 4 of the algo <3")