import datetime
import random

import networkx as nx
import numpy as np
from networkx.algorithms.community import girvan_newman, louvain_communities, greedy_modularity_communities
from sklearn.metrics import silhouette_score
from sklearn.metrics.cluster import normalized_mutual_info_score as NMI3
from networkx.algorithms.community.quality import modularity
from collections import defaultdict

from visualization.visualization_graph import VisualizationGraph


class AnalyticsGraph:

    def centrality_betweenness_library(graph):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Calculate the betweenness centrality of a graph using the networkX library
        :param graph: networkX - Graph networkX (of the amazon dataset refined)
        :type graph: networkX
        :return: Each node with its betweenness centrality value (if above 0.0)
        """
        current_time = datetime.datetime.now()
        print(">> You have called the betweenness centrality library for your graph (at", current_time, ").")

        nodes = nx.betweenness_centrality(
            graph)  # Centrality dictionary: node as key and its betweenness centrality as value

        non_central_nodes = 0
        for node in nodes.keys():
            if round(nodes[node], 2) > 0.0:
                print("\t\t\t\t" + str(node) + " : " + str(round(nodes[node], 3)))
            else:
                non_central_nodes += 1

        if non_central_nodes == len(nodes.keys()):
            print("\t\t\t\tResult: There are no nodes having a betweenness centrality above 0.0.")

        return nodes

    def community_library_detection(graph, library="Default"):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Detect communities with a specific library
        :param graph: networkX - Graph networkX (of the amazon dataset refined)
        :type graph: networkX
        :param library: string - Library chosen (girvanNewman;louvain;modularity)
        :type graph: string
        :return: Communities found by the chosen library
        """
        current_time = datetime.datetime.now()
        print(">> You have called the community detection with ", library, " (at", current_time, ")")

        communities = []

        # Library: community.girvan_newman
        if library == "girvanNewman":
            communities = girvan_newman(graph)
            print(communities)
            for i, c in enumerate(communities):
                print("(girvanNewman) > community ", i, " : ", c)

            ### throws an error (using flag = prod and graph=graph) - Sophie
            modularity_score = modularity(graph, communities)
            print("Modularity score:", modularity_score)

        # Library: louvain_communities
        if library == "louvain":
            communities = louvain_communities(graph, seed=127)
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
        reviewed by : Sophie Caroni
        Compute modularity gain between two communities
        :param graph: networkX - Graph networkX (of the amazon dataset refined)
        :type graph: networkX
        :param first_community: list of nodes belonging to the first community
        :type first_community: list
        :param second_community: list of nodes belonging to the first community
        :type second_community: list
        :return: Modularity gain, first community and second community
        """
        n_edges = nx.number_of_edges(graph)

        # Find number of neighbors of each node inside the first community
        d_i = 0
        for n in first_community:
            d_i += len(list(graph.neighbors(n)))

        # Find number of neighbors of each node inside the second community
        d_j = 0
        for n in second_community:
            d_j += len(list(graph.neighbors(n)))

        # Find number of shared links between first and second community
        d_ij = 0
        for n in first_community:
            for ni in graph.neighbors(n):
                if ni in second_community:
                    d_ij += 1

        for m in second_community:
            for mi in graph.neighbors(m):
                if mi in first_community:
                    d_ij += 1

        # Compute modularity gain between the two communities
        modularity_gain = 1 / (2 * n_edges) * (d_ij - (d_i * d_j / n_edges))

        return [modularity_gain, first_community, second_community]

    def homemade_community_detection(graph, display=False):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Detect communities with a specific algorithm
        :param graph: networkX - Graph networkX (of the amazon dataset refined)
        :type graph: networkX
        :return: Communities found based on the best modularity gain
        """
        current_time = datetime.datetime.now()
        print(">> You've called the homemade (good choice) community detection (at", current_time, "), please wait <3")

        # phase 1 =====================================================================================================
        # Set initial communities as one node each and compute the initial modularity
        communities = [[community] for community in graph.nodes()]
        original_modularity = modularity(nx.Graph(graph), communities)
        best_modularity = original_modularity

        if display:
            print("\t(ANL) : Original community list : ", communities)
            print("\t(ANL) : Best_modularity : ", best_modularity)

        inc, limit, deltaQ, oldValue, oldDeltaQ = 0, len(communities), 0, 0, 0

        while limit > inc:
            # phase 2 =====================================================================================================
            # Retrieve the first community
            community_vi = communities.pop(0)

            if display:
                print("\t\t(ANL) : community_vi :\t", community_vi)

            # phase 3 =====================================================================================================
            allResult, nodeNeighbors, communityNeighbors = [], [], []

            # Retrieve all neighbors of the treated community (i.e. of each node of the community)
            for node in community_vi:
                for n in graph.neighbors(node):
                    nodeNeighbors.append(n)

            # Retrieve all communities that are neighbored to all nodes of the treated community
            for n in nodeNeighbors:
                for community in communities:
                    if n in community:
                        if community not in communityNeighbors:
                            communityNeighbors.append(community)

            communityNeighbors = sorted(communityNeighbors, reverse=True)

            # Skip the treated community if it currently hasn't any neighbor
            if len(communityNeighbors) == 0:
                communities.append(community_vi)
                inc += 1
                continue

            # Compute modularity gain for each of the communities born by adding community_vi to each of them
            for community in communityNeighbors:
                allResult.append(AnalyticsGraph.homemade_modularity_gain(graph, community_vi, community))

            # Save as "maxValue" the highest modularity gain brought by the adding of community_vi
            bestDeltaQ = max(allResult[n][0] for n in range(len(allResult)))

            # Save as "winningCommunity" the one getting the highest modularity gain from the adding of community_vi
            for i, values in enumerate(allResult):
                if allResult[i][0] == bestDeltaQ:
                    winningCommunity = allResult[i][2]

            # If the new community score is increasing the total modularity score
            if bestDeltaQ > 0:
                for community in communities:
                    if community == winningCommunity:
                        for c in community_vi:
                            community.append(c)
            else:
                communities.append(community_vi)

            current_modularity = modularity(graph, communities)

            if display:
                print("\t\t(ANL) : Max Delta Q :", bestDeltaQ, " (for ", allResult, ")")
                print("\t\t(ANL) : Winning Community :", winningCommunity)
                print("\t\t(ANL) : deltaQ :", deltaQ, )
                print("\t\t(ANL) : Updated community list : ", communities)
                print("\t\t(ANL) : score : ", current_modularity)
                print("\t\t(ANL) : high score : ", best_modularity)

            # Stop if the total modularity is not improving anymore
            if current_modularity < best_modularity > 0:
                break
            else:
                best_modularity = current_modularity

            final_modularity = modularity(graph, communities)
            inc += 1

            if display:
                print("\t\t(ANL) : new score : ", best_modularity)
                print("======= LOOP ===============================================")

                print("\t(ANL) : original modularity :", original_modularity)
                print("\t(ANL) : final modularity :", final_modularity)

        if display:
            for i, community in enumerate(communities):
                print("\t\t\t\t\t\t\t\t", i, " : ", community)

        print("\n\t(ANL) : Communities result : ", communities, " \n\n")

        current_time = datetime.datetime.now()
        print("<< the louvain detection homemade has finished (at", current_time, "), arigato <3")

        return communities

    def compare_algo_efficiency(graph, communities_algo_homemade):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Compare communities found using homemade algorithm with those found using louvain_communities library
        :param graph: networkX - Graph networkX (of the amazon dataset refined)
        :type graph: networkX
        :param communities_algo_homemade: list of communities, which are list of nodes
        :type communities_algo_homemade: list of list
        :return: Normalized Mutual Information between the two communities
        """
        print(">> You've called the comparator of algorithm, please wait :)")

        # Compute the communities of the graph using louvain_community library
        communities_algo_library = louvain_communities(graph, seed=123)

        # Compute modularities of the graph for homemade versus with library fund communities
        modularity_homemade = modularity(graph, communities_algo_homemade)
        modularity_library = modularity(graph, communities_algo_library)

        print("\t\t(ANL) : modularity 1st algorithm :", modularity_homemade)
        print("\t\t(ANL) : modularity 2nd algorithm :", modularity_library)

        # Compare the communities, if they are the same number
        try:
            labels_true = [0] * len(communities_algo_homemade[0]) + [1] * len(communities_algo_homemade[1])
            labels_pred = [0] * len(communities_algo_library[0]) + [1] * len(communities_algo_library[1])

            nmi = NMI3(labels_true, labels_pred)
            print("\t\t(ANL) : NMI3 score :", round((nmi * 100), 2), "%")
        except:
            nmi = -1
            print("\t\t(ANL) : Cannot get a NMI score if the number communities are not the same...")

        return nmi

    def deep_analyze(graph, listOfCommands, allChecked=True):
        """
        Creator : Emmanuel
        reviewed by :
        Compare communities found using homemade algorithm with those found using louvain_communities library
        :param graph: networkX - Graph networkX (of the amazon dataset refined)
        :type graph: networkX
        :param listOfCommands: list of String of command
        (simple_information / degree_distribution / connected_components / diameters / clustering_coefficient /
        betweenness_centrality / degree_centrality / eigenvector_centrality / pagerank_centrality /
        closeness_centrality / adamicadar_score / jaccard_score)
        Jaccard and Adamic-Adar algorith does not work with directed graph no unprocessed
        :type listOfCommands: String
        :return: list of all results
        """

        listOfResult = []

        if "degree_distribution" in listOfCommands or allChecked:
            listOfResult.append([["degree_distribution"], [AnalyticsGraph.degree_distribution(graph)]])

        if "diameters" in listOfCommands or allChecked:
            listOfResult.append([["diameters"], [AnalyticsGraph.degree_centrality_scores(graph)]])

        if "clustering_coefficient" in listOfCommands or allChecked:
            listOfResult.append([["clustering_coefficient"], [AnalyticsGraph.clustering_coefficient(graph)]])

        if "betweenness_centrality" in listOfCommands or allChecked:
            listOfResult.append([["betweenness_centrality"], [AnalyticsGraph.betweenness_centrality_scores(graph)]])

        if "degree_centrality" in listOfCommands or allChecked:
            listOfResult.append([["degree_centrality"], [AnalyticsGraph.degree_centrality_scores(graph)]])

        if "eigenvector_centrality" in listOfCommands or allChecked:
            listOfResult.append([["eigenvector_centrality"], [AnalyticsGraph.eigenvector_centrality_scores(graph)]])

        if "pagerank_centrality" in listOfCommands or allChecked:
            listOfResult.append([["pagerank_centrality"], [AnalyticsGraph.pagerank_centrality_scores(graph)]])

        if "closeness_centrality" in listOfCommands or allChecked:
            listOfResult.append([["closeness_centrality"], [AnalyticsGraph.closeness_centrality_scores(graph)]])

        return listOfResult

    def closeness_centrality_scores(graph, display=False):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater
        Get the score for centrality analytics in the context of exploration analysis
        :param graph: networkX - Graph networkX (of the amazon dataset refined)
        :type graph: networkX
        :param display: Boolean - Display or not the plots and prints
        :type display: Boolean
        :return: list of the results
        """
        # Closeness centrality measure
        cc_scores = nx.closeness_centrality(graph)
        if display:
            print("Closeness centrality:")
            for node, score in cc_scores.items():
                print(f"{node}: {score}")
        return cc_scores

    def pagerank_centrality_scores(graph, display=False):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater
        Get the score for centrality analytics in the context of exploration analysis
        :param graph: networkX - Graph networkX (of the amazon dataset refined)
        :type graph: networkX
        :param display: Boolean - Display or not the plots and prints
        :type display: Boolean
        :return: list of the results
        """
        # PageRank's centrality measure
        pr_scores = nx.pagerank(graph)
        if display:
            print("PageRank:")
            for node, score in pr_scores.items():
                print(f"{node}: {score}")
        return pr_scores

    def eigenvector_centrality_scores(graph, display=False):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater
        Get the score for centrality analytics in the context of exploration analysis
        :param graph: networkX - Graph networkX (of the amazon dataset refined)
        :type graph: networkX
        :param display: Boolean - Display or not the plots and prints
        :type display: Boolean
        :return: list of the results
        """
        # Eigenvector centrality measure
        ec_scores = nx.eigenvector_centrality(graph)

        if display:
            print("Eigenvector centrality:")
            for node, score in ec_scores.items():
                print(f"{node}: {score}")
        return ec_scores

    def degree_centrality_scores(graph, display=False):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater
        Get the score for centrality analytics in the context of exploration analysis
        :param graph: networkX - Graph networkX (of the amazon dataset refined)
        :type graph: networkX
        :param display: Boolean - Display or not the plots and prints
        :type display: Boolean
        :return: Result of the degree centrality
        """
        # Degree centrality measure
        dc_scores = nx.degree_centrality(graph)

        if display:
            print("\t\t\t (ANL) : Degree centrality:")
            for node, score in dc_scores.items():
                print(f"{node}: {score}")
        return dc_scores

    def betweenness_centrality_scores(graph, display=False):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater
        Get the betweenness centrality of the nodes in the graph (a measure of the importance of a node in connecting different parts of the graph)
        :param graph: networkX - Graph networkX (of the amazon dataset refined)
        :type graph: networkX
        :param display: Boolean - Display or not the plots and prints
        :type display: Boolean
        :return: list of the results
        """
        bc_scores = nx.betweenness_centrality(graph)

        if display:
            print("\t\t\t (ANL) : Betweenness centrality:")
            for node, score in bc_scores.items():
                print(f"{node}: {score}")
        return bc_scores

    def highest_betweenness_centrality_score(graph, community, display=False):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater
        Get the betweenness centrality of the nodes in the graph (a measure of the importance of a node in connecting different parts of the graph)
        :param graph: networkX - Graph networkX (of the amazon dataset refined)
        :type graph: networkX
        :param community: List of String - All nodes of a community
        :type community: List of String
        :param display: Boolean - Display or not the plots and prints
        :type display: Boolean
        :return: list of the results
        """
        subgraph = graph.subgraph(community)  # create subgraph with only those nodes

        bc_scores = nx.betweenness_centrality(subgraph)

        high_score = 0
        high_node = ""

        if display:
            print("\t\t\t (ANL) : Betweenness centrality:")
        for node, score in bc_scores.items():
            if display:
                print(f"\t\t\t (ANL) : {node}: {score}")
            if score > high_score:
                high_score = score
                high_node = node

        return [high_score, high_node]

    def highest_betweenness_centrality_scores(graph, communities, display=False):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater
        Get the betweenness centrality of the nodes in the graph (a measure of the importance of a node in connecting different parts of the graph)
        :param graph: networkX - Graph networkX (of the amazon dataset refined)
        :type graph: networkX
        :param communities: String [[]] - All communities with all nodes of a community
        :type communities: String [[]]
        :param display: Boolean - Display or not the plots and prints
        :type display: Boolean
        :return: list of the results
        """

        current_time = datetime.datetime.now()
        print("\n>> You have called the highest betweeness centrality scores, (at", current_time, "), please wait :)")

        popular_nodes = []
        for community in communities:
            popular_nodes.append(AnalyticsGraph.highest_betweenness_centrality_score(graph, community, display))

        if display:
            for x, popular in enumerate(popular_nodes):
                print("\t\t\t (ANL) : ", x, ": ", popular[1], ' with a centrality score of ',
                      round(int(popular[0] * 100), 2), "%")

        current_time = datetime.datetime.now()
        print("<< The highest betweeness centrality scores has finished (at", current_time, "), arigato <3\n")

        myExport = ""
        for x, popular in enumerate(popular_nodes):
            myExport = myExport + str(x) + ":" + str(popular[1]) + "=" + str(round(int(popular[0] * 100), 2)) + "\n"
        with open('./results/communities_populars.txt', 'w') as file:
            # Write the string variable to the file
            file.write(myExport)

        return popular_nodes

    def clustering_coefficient(graph, display=False):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater
        Get the score for centrality analytics in the context of exploration analysis
        :param graph: networkX - Graph networkX (of the amazon dataset refined)
        :type graph: networkX
        :param display: Boolean - Display or not the plots and prints
        :type display: Boolean
        :return: Result of the clustering coefficient
        """
        cc = nx.average_clustering(graph)
        if display:
            print("\t\t\t (ANL) : Clustering coefficient:", cc)
        return cc

    def diameter_centrality(graph, display=False):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater
        Get the score for centrality analytics in the context of exploration analysis
        :param graph: networkX - Graph networkX (of the amazon dataset refined)
        :type graph: networkX
        :param display: Boolean - Display or not the plots and prints
        :type display: Boolean
        :return: Result of the diameter centrality
        """
        # Get the connected components of the graph
        connected_components = nx.connected_components(graph)

        # Compute the diameter for each connected component
        diameters = [nx.diameter(graph.subgraph(component)) for component in connected_components]

        # Print the diameters
        if display:
            print("\t\t\t (ANL) : Diameters of connected components:", diameters)

        return diameters

    def degree_distribution(graph, display=False):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater
        Get the score for centrality analytics in the context of exploration analysis
        :param graph: networkX - Graph networkX (of the amazon dataset refined)
        :type graph: networkX
        :param display: Boolean - Display or not the plots and prints
        :type display: Boolean
        :return: Result of the degree distribution
        """
        # Get the degree distribution of the nodes in the graph
        degree_sequence = [d for n, d in graph.degree()]
        degree_counts = dict(
            zip(sorted(set(degree_sequence)), [degree_sequence.count(d) for d in sorted(set(degree_sequence))]))
        if display:
            print("\t\t\t (ANL) : Degree distribution:", degree_counts)
        return degree_counts


    # =================================================================================================================
    # COMMUNITY DETECTION HOMEMADE
    # =================================================================================================================
    def amazon_community_detection(graph, tag="louvain", run_silhouette=False, display=False):
        current_time = datetime.datetime.now()
        print("\n<< You have run the homemade amazon community detection algorithm (at", current_time, "), arigato <3")

        #=STAGE ONE====================================================================================================
        communities = [{u} for u in graph.nodes()]
        modularity = 1 / pow(sum(dict(graph.degree()).values()), 2)

        myGraph = graph.__class__()
        myGraph.add_nodes_from(graph)
        myGraph.add_weighted_edges_from(graph.edges(data="weight", default=1))

        graphSize = myGraph.size()

        communities, inner_partition, stillBetter = AnalyticsGraph.inner_logic(myGraph, graphSize, communities, display=display)
        stillBetter = True

        #====STAGE TWO=================================================================================================
        while stillBetter:
            new_modularity = sum(dict(myGraph.degree()).values()) / 2
            deltaQ = new_modularity - modularity
            if deltaQ <= 0:
                break
            modularity = new_modularity

            # =UPDATE WEIGHT===========================================================================
            H = myGraph.__class__()
            dicIndex = {}
            for i, part in enumerate(inner_partition):
                nodes = set()
                for node in part:
                    dicIndex[node] = i
                    nodes.add(node)
                H.add_node(i, nodes=nodes)
            for node1, node2, wt in myGraph.edges(data=True):
                wt = wt["weight"]
                com1 = dicIndex[node1]
                com2 = dicIndex[node2]
                temp = H.get_edge_data(com1, com2, {"weight": 0})["weight"]
                H.add_edge(com1, com2, weight=wt + temp)
            myGraph = H
            # =============================================================================
            communities, inner_partition, stillBetter = AnalyticsGraph.inner_logic(myGraph, graphSize, communities, display=display)

        # ==DISPLAY=====================================================================================================
        best_communities = list(communities)
        print("\t\t(ANL) : Community detection (louvain homemade) result :")
        for x, c in enumerate(best_communities):
            print("\t\t\t(ANL) : ", x, ": ", c)
        # ==SAVE========================================================================================================
        VisualizationGraph.saveCommunities(best_communities, tag)
        # ==ANALYTICS===================================================================================================
        if run_silhouette:
            AnalyticsGraph.silhouette_score(graph=graph, community_detection=best_communities, metric="euclidean", sample_size=1000)
        # ==============================================================================================================

        current_time = datetime.datetime.now()
        print("<< The homemade amazon community detection algorithm has finished (at", current_time, "), arigato <3\n")
        return best_communities

    def inner_logic(graph, size_of_graph, communities, display=True):
        #===STAGE THREE================================================================================================
        communityNodes, newCommunity = {}, []
        is_directed = graph.is_directed()

        # *** INITIALIZATION AND THE ALGO AND LIST *****************************
        # initialization of the community with each node as community
        stillBetter     = False
        operations      = 1
        pushNodeList    =  list(graph.nodes)
        in_degrees      = dict(graph.in_degree(weight="weight"))
        out_degrees     = dict(graph.out_degree(weight="weight"))
        degreeStrengthIn  = list(in_degrees.values())
        degreeStrengthOut = list(out_degrees.values())

        weightStrength = {}
        for value in graph:
            weightStrength[value] = defaultdict(float)
            for _, node, weight in graph.out_edges(value, data="weight"):
                weightStrength[value][node] += weight
            for node, _, weight in graph.in_edges(value, data="weight"):
                weightStrength[value][node] += weight

        for x, node in enumerate(graph.nodes()):
            communityNodes[node] = x

        for node in graph.nodes():
            newCommunity.append({node})

        while operations > 0:
            operations = 0

            for node in pushNodeList:
                bestModality, bestCommunity = 0, communityNodes[node]

                weightCommunity = defaultdict(int)
                for key, number_of_edges in weightStrength[node].items():
                    weightCommunity[communityNodes[key]] += number_of_edges

                in_degree = in_degrees[value]
                out_degree = out_degrees[value]
                degreeStrengthIn[bestCommunity] -= in_degree
                degreeStrengthOut[bestCommunity] -= out_degree

                size_power = size_of_graph ** 2
                remove_cost = (-weightCommunity[bestCommunity] / size_of_graph + (out_degree * degreeStrengthIn[bestCommunity] + in_degree * degreeStrengthOut[bestCommunity]) / size_power)

                for numberCommunities, number_of_edges in weightCommunity.items():
                    gain = (number_of_edges / size_of_graph - (out_degree * degreeStrengthIn[numberCommunities] + in_degree * degreeStrengthOut[numberCommunities]) / size_power)
                    Q = remove_cost + gain

                    if display:
                        print("\t\t\t\t\t\tnode : ", node)
                        print("\t\t\t\t\t\tnbr_com / number_of_edges: ", numberCommunities, " / ", number_of_edges)
                        print("\t\t\t\t\t\tgain :   (number_of_edges / size_of_graph - (out_degree * degreeStrengthIn[numberCommunities] + in_degree * degreeStrengthOut[numberCommunities]) / size_power) = (", number_of_edges, " / ", size_of_graph, " - ( ", out_degree, " * ", degreeStrengthIn[numberCommunities], " + ", in_degree, " * ", degreeStrengthOut[numberCommunities], ") / ", size_power, ")")
                        print("\t\t\t\t\t\tdeltaQ : ", Q, "\n")

                    if Q > bestModality:
                        bestModality = Q
                        bestCommunity = numberCommunities

                        if display:
                            print("\t\t\t\t\t\tNEW BEST MODALITY !!! \n")

                degreeStrengthIn[bestCommunity] += in_degree
                degreeStrengthOut[bestCommunity] += out_degree

                if bestCommunity != communityNodes[node]:
                    # Retrieve the community of the current node
                    node_community = communityNodes[node]
                    community = graph.nodes[node].get("nodes", {node})

                    # Remove the current node from its community
                    communities[node_community] -= community
                    newCommunity[node_community].remove(node)

                    # Add the current node to the best community
                    communities[bestCommunity] |= community
                    newCommunity[bestCommunity].add(node)

                    stillBetter = True
                    operations = operations + 1

                    communityNodes[node] = bestCommunity

                    if display:
                        print("\t\t\t\t\t\tnumber of operations : ", operations)
                        print("\t\t\t\t\t\tcurrent communities : ", communities, "\n")

        communitiesTMP, newCommunitiesTMP = [], []
        for community in communities:
            if len(community) > 0:
                communitiesTMP.append(community)
        for community in newCommunity:
            if len(community) > 0:
                newCommunitiesTMP.append(community)

        newCommunity = newCommunitiesTMP
        communities = communitiesTMP

        return communities, newCommunity, stillBetter


    # =================================================================================================================
    # QUALITY OF THE COMMUNITY DETECTION
    # =================================================================================================================

    def accuracy_precision_recall_jaccard(communities_library, community_homemade, display=True):
        """
        Creator : Quentin Nater
        reviewed by :
        Compute the score of Accuracy, Precision, Recall and Jaccard, comparing two community detections
        :param communities_library: list(set) - All communities detected by the networkX library
        :type communities_library: list(set)
        :param community_homemade: list(set) - All communities detected by the homemade algorithm
        :type community_homemade: list(set)
        :return: the scores of Accuracy, Precision, Recall and Jaccard
        """

        current_time = datetime.datetime.now()
        print("<< The Accuracy/Precision/Recall/Jaccard score between the 2 algorithm has been called (at", current_time, "), please wait...\n")

        # Convert the list of communities to sets
        labels = [set(community) for community in communities_library]
        data = [set(community) for community in community_homemade]

        # initialize the arrays of results
        accuracies, precisions, recalls, jaccards = [], [], [], []

        for i in range(len(data)):
            best_jaccard, index = 0.0, None

            for j in range(len(labels)):
                intersection_size = len(data[i].intersection(labels[j]))
                union_size = len(data[i].union(labels[j]))
                jaccard_similarity = intersection_size / union_size

                if jaccard_similarity > best_jaccard:
                    best_jaccard = jaccard_similarity
                    index = j

            if index is not None:
                TP = len(data[i].intersection(labels[index]))
                FP = len(data[i].difference(labels[index]))
                FN = len(labels[index].difference(data[i]))

                total = len(labels[index])
                accuracy = TP / total
                precision = TP / (TP + FP)
                recall = TP / (TP + FN)

                if display:
                    print("\n\t\t\t\t (ANA) : RUN :", i)
                    print("\n\t\t\t\t (ANA) : best_jaccard :", best_jaccard)
                    print("\t\t\t\t (ANA) : set_X :", data[i])
                    print("\t\t\t\t (ANA) : set_Y :", labels[index])
                    print("\t\t\t\t (ANA) : total :", total)
                    print("\t\t\t\t (ANA) : TP :", TP)
                    print("\t\t\t\t (ANA) : FP :", FP)
                    print("\t\t\t\t (ANA) : FN :", FN, "\n")

                accuracies.append(accuracy)
                precisions.append(precision)
                recalls.append(recall)
                jaccards.append(best_jaccard)

        accuracy = sum(accuracies) / len(accuracies)
        precision = sum(precisions) / len(precisions)
        recall = sum(recalls) / len(recalls)
        jaccard = sum(jaccards) / len(jaccards)

        print("\n\t\t (ANA) : Accuracy between the 2 algorithm is :", str(round(accuracy * 100, 2)), "%")
        print("\t\t (ANA) : Precision between the 2 algorithm is :", str(round(precision * 100, 2)), "%")
        print("\t\t (ANA) : Recall between the 2 algorithm is :", str(round(recall * 100, 2)), "%")
        print("\t\t (ANA) : Jaccard similarity between the 2 algorithm is :", str(round(jaccard, 2)), "\n")

        current_time = datetime.datetime.now()
        print("<< The Accuracy/Precision/Revall/Jaccard score between the 2 algorithm has finished (at", current_time, "), arigato <3\n")

        return accuracy, precision, recall, jaccard

    def silhouette_score(graph, community_detection, metric='euclidean', sample_size=None):
        """
        Creator: Quentin Nater
        Reviewed by:
        Compute the score of Accuracy, Precision, Recall, and Jaccard, comparing two community detections
        :param graph: NetworkX Graph - Total graph of the network
        :type graph: NetworkX Graph
        :param community_detection: list(set) - All communities detected by the algorithm
        :type community_detection: list(set)
        :param metric: String - Metric to use for the silhouette index
        :type metric: String
        :param sample_size: Integer - Number of nodes to sample from the graph (optional)
        :type sample_size: Integer or None
        :return: The score of the silhouette index
        """

        current_time = datetime.datetime.now()
        print("\n\t<< The Silhouette Index Score has been called (at", current_time, "), please wait...\n")

        if sample_size is not None and sample_size < graph.number_of_nodes():
            sampled_nodes = random.sample(list(graph.nodes()), sample_size)
            subgraph = graph.subgraph(sampled_nodes)

            new_community_detection = []
            # store the results of computation between the intersection of the community and the sample
            for community in community_detection:
                intersection = set(community).intersection(sampled_nodes)
                new_community_detection.append(intersection)
            community_detection = new_community_detection
        else:
            subgraph = graph

        # create a label for each node
        node_to_label = {}
        for label, community in enumerate(community_detection):
            for node in community:
                node_to_label[node] = label

        # create the label
        node_labels = []
        for node in subgraph.nodes():
            label = node_to_label.get(node, -1)
            node_labels.append(label)

        node_labels = np.array(node_labels).reshape(-1, 1)

        # Compute the adjacency matrix of the current graph
        adjacency_matrix = nx.to_numpy_array(subgraph)

        # Stack arrays in sequence horizontally (column wise).
        feature_matrix = np.hstack((adjacency_matrix, node_labels))

        # Compute the final score
        silhouette = silhouette_score(X=feature_matrix, labels=node_labels.ravel(), metric=metric)

        print("\t\t\t (ANA) : Silhouette index score:", silhouette, "\n")

        current_time = datetime.datetime.now()
        print("\t<< The Silhouette Index Score has finished (at", current_time, "), arigato <3\n")

        return silhouette
