import datetime

import networkx as nx
import numpy as mynp
import numpy as np
from networkx.algorithms.clique import find_cliques
from networkx.algorithms.community import girvan_newman, louvain_communities, k_clique_communities, \
    greedy_modularity_communities, modularity, label_propagation_communities
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from sklearn.metrics.cluster import normalized_mutual_info_score as NMI3

from networkx.algorithms.community.quality import modularity


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

    def homemade_community_detection(graph, display=False):
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
        communities = [[community] for community in graph.nodes()]
        best_modularity = modularity(nx.Graph(graph), communities)
        original_modularity = best_modularity

        if display:
            print("\tOriginal community list : ", communities)
            print("\tBest_modularity : ", best_modularity)

        inc, limit, deltaQ, oldValue, oldDeltaQ = 0, len(communities), 0, 0, 0

        while limit > inc:
            # phase 2 =====================================================================================================
            community_vi = communities.pop(0)

            if display:
                print("\t\tcommunity_vi :\t", community_vi)

            # phase 3 =====================================================================================================
            allResult, neighbors, communityNeighbors = [], [], []

            for node in community_vi:
                for n in graph.neighbors(node):
                    neighbors.append(n)

            for n in neighbors:
                for community in communities:
                    if n in community:
                        if community not in communityNeighbors:
                            communityNeighbors.append(community)

            communityNeighbors = sorted(communityNeighbors, reverse=True)

            if len(communityNeighbors) == 0:
                communities.append(community_vi)
                inc += 1
                continue

            for community in communityNeighbors:
                allResult.append(AnalyticsGraph.homemade_modularity_gain(graph, community_vi, community))

            maxValue = max(allResult[n][0] for n in range(len(allResult)))

            for i, values in enumerate(allResult):
                if allResult[i][0] == maxValue:
                    winningCommunity = allResult[i][2]

            if maxValue > 0:
                for community in communities:
                    if community == winningCommunity:
                        for c in community_vi:
                            community.append(c)
            else:
                communities.append(community_vi)

            current_modularity = modularity(graph, communities)

            if display:
                print("\t\tMax value :", maxValue, " (for ", allResult, ")")
                print("\t\tWinning Community :", winningCommunity)
                print("\t\tdeltaQ :", deltaQ, )
                print("\t\tUpdated community list : ", communities)
                print("\t\tscore : ", current_modularity)
                print("\t\thigh score : ", best_modularity)

            if current_modularity < best_modularity > 0:
                break
            else:
                best_modularity = current_modularity

            final_modularity = modularity(graph, communities)
            inc += 1

            if display:
                print("\t\tnew score : ", best_modularity)
                print("======= LOOP ===============================================")

                print("\toriginal modularity :", original_modularity)
                print("\tfinal modularity :", final_modularity)

        if display:
            for i, community in enumerate(communities):
                print("\t\t\t\t\t\t\t\t", i, " : ", community)

        print("\n\tCommunities result : ", communities, " \n\n")

        return communities

    def compare_algo_efficiency(graph, communities_algo_homemade):
        print(">> You've called the comparator of algorithm, please wait :)")

        communities_algo_library = louvain_communities(graph, seed=123)

        modularity_homemade = modularity(graph, communities_algo_homemade)
        modularity_library = modularity(graph, communities_algo_library)

        print("\t\tmodularity 1st algorithm :", modularity_homemade)
        print("\t\tmodularity 2nd algorithm :", modularity_library)

        try:
            labels_true = [0] * len(communities_algo_homemade[0]) + [1] * len(communities_algo_homemade[1])
            labels_pred = [0] * len(communities_algo_library[0]) + [1] * len(communities_algo_library[1])

            nmi = NMI3(labels_true, labels_pred)
            print("\t\tNMI3 score :", round((nmi * 100), 2), "%")
        except:
            nmi = -1
            print("\t\tCannot get score if the number communities are not the same...")

        return nmi
