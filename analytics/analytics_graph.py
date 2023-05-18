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

    def centrality_betweenness_library(self, graph):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Calculate the betweenness centrality of a graph using the networkX library
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :return: Each node with its betweenness centrality value (if above 0.0)
        """
        current_time = datetime.datetime.now()
        print(">> You have called the betweenness centrality library for your graph (at", current_time, ").")

        # Create a centrality dictionary: nodes as keys and their betweenness centrality as values
        nodes = nx.betweenness_centrality(graph)

        non_central_nodes = 0
        for node in nodes.keys():
            if round(nodes[node], 2) > 0.0:
                print("\t\t\t\t" + str(node) + " : " + str(round(nodes[node], 3)))
            else:
                non_central_nodes += 1

        if non_central_nodes == len(nodes.keys()):
            print("\t\t\t\tResult: There are no nodes having a betweenness centrality above 0.0.")

        return nodes

    def community_library_detection(self, graph, library="Default", display=False):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Detect communities with a specific library
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param library:Library chosen (girvanNewman;louvain;modularity)
        :type graph: string
        :param display: Display the details or not
        :type display: boolean
        :return: Communities found by the chosen library
        """
        current_time = datetime.datetime.now()
        print(">> You have called the community detection with the library ", library, " (at", current_time, ")")

        if library == "girvanNewman":  # Library: community.girvan_newman
            communities = girvan_newman(graph)

            if display:
                print(communities)
                for i, c in enumerate(communities):
                    print("(girvanNewman) > community ", i, " : ", c)

            modularity_score = modularity(graph, communities)
            print("Modularity score:", modularity_score)

        elif library == "louvain":  # Library: louvain_communities
            print("\t\t(ANL) : You have run the NetworkX Louvain community detection !")
            communities = louvain_communities(graph, seed=127)
            if display:
                for i, c in enumerate(communities):
                    print("\t\t\t(ANL) : ", i, ": ", c)

        else:  # Library: greedy_modularity_communities
            communities = greedy_modularity_communities(graph)

            if display:
                for i, c in enumerate(communities):
                    print("(greedy_modularity_communities) > community ", i, " : ", c)

                modularity_score = modularity(graph, communities)
                print("Modularity score:", modularity_score)

        return communities

    def homemade_modularity_gain(self, graph, first_community, second_community):
        """
        Creator : Sophie Caroni
        reviewed by :
        Compute modularity gain between two communities
        :param graph: Graph networkX of the dataset
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

    def homemade_community_detection(self, graph, display=False):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Detect communities with a specific algorithm
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :return: Communities found based on the best modularity gain
        :param display: Display the details or not
        :type display: boolean
        """
        current_time = datetime.datetime.now()
        print(">> You've called the homemade community detection (at", current_time, "), please wait.")

        # phase 1 =====================================================================================================
        # Set initial communities as one node each and compute the initial modularity
        communities = [[community] for community in graph.nodes()]
        original_modularity = modularity(nx.Graph(graph), communities)
        best_modularity = original_modularity

        if display:
            print("\t(ANL) : Original community list : ", communities)
            print("\t(ANL) : Best_modularity : ", best_modularity)

        inc, limit, delta_q, old_value, old_delta_q = 0, len(communities), 0, 0, 0

        while limit > inc:
            # phase 2 =================================================================================================
            # Retrieve the first community
            community_vi = communities.pop(0)

            if display:
                print("\t\t(ANL) : community_vi :\t", community_vi)

            # phase 3 =================================================================================================
            all_result, node_neighbors, community_neighbors = [], [], []

            # Retrieve all neighbors of the treated community (i.e. of each node of the community)
            for node in community_vi:
                for n in graph.neighbors(node):
                    node_neighbors.append(n)

            # Retrieve all communities that are neighbored to all nodes of the treated community
            for n in node_neighbors:
                for community in communities:
                    if n in community:
                        if community not in community_neighbors:
                            community_neighbors.append(community)

            community_neighbors = sorted(community_neighbors, reverse=True)

            # Skip the treated community if it currently hasn't any neighbor
            if len(community_neighbors) == 0:
                communities.append(community_vi)
                inc += 1
                continue

            # Compute modularity gain for each of the communities born by adding community_vi to each of them
            for community in community_neighbors:
                all_result.append(AnalyticsGraph.homemade_modularity_gain(self, graph, community_vi, community))

            # Save as "maxValue" the highest modularity gain brought by the adding of community_vi
            best_delta_q = max(all_result[n][0] for n in range(len(all_result)))

            # Save as "winning_community" the one getting the highest modularity gain from the adding of community_vi
            for i, values in enumerate(all_result):
                if all_result[i][0] == best_delta_q:
                    winning_community = all_result[i][2]

            # If the new community score is increasing the total modularity score
            if best_delta_q > 0:
                for community in communities:
                    if community == winning_community:
                        for c in community_vi:
                            community.append(c)
            else:
                communities.append(community_vi)

            current_modularity = modularity(graph, communities)

            if display:
                print("\t\t(ANL) : Max Delta Q :", best_delta_q, " (for ", all_result, ")")
                print("\t\t(ANL) : Winning Community :", winning_community)
                print("\t\t(ANL) : delta_q :", delta_q, )
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
        print("<< The louvain detection homemade has finished (at", current_time, ").")

        return communities

    def compare_algo_efficiency(self, graph, communities_algo_homemade):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Compare communities found using homemade algorithm with those found using louvain_communities library
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param communities_algo_homemade: list of communities, which are list of nodes
        :type communities_algo_homemade: list of list
        :return: Normalized Mutual Information between the two communities
        """
        print(">> You've called the comparator of algorithm, please wait.")

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
        except IndexError:
            nmi = -1
            print("\t\t(ANL) : Cannot get a NMI score if the number communities are not the same...")

        return nmi

    def deep_analyze(self, graph, commands, all_checked=True):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Sophie Caroni
        Compare communities found using homemade algorithm with those found using louvain_communities library
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param commands: [simple_information, degree_distribution, connected_components, diameters, clustering_coefficient,
        betweenness_centrality, degree_centrality, eigenvector_centrality, pagerank_centrality, closeness_centrality,
        adamicadar_score, jaccard_score]
        :type commands: list of strings
        :param all_checked: To execute all commands once
        :type all_checked: bool
        :return: list of all results
        """
        results = []

        if "degree_distribution" in commands or all_checked:
            commands.append([["degree_distribution"], [AnalyticsGraph.degree_distribution(graph=graph, display=True)]])

        if "clustering_coefficient" in commands or all_checked:
            commands.append([["clustering_coefficient"], [AnalyticsGraph.clustering_coefficient(graph=graph, display=True)]])

        if "diameters" in commands or all_checked:
            commands.append([["diameters"], [AnalyticsGraph.degree_centrality_scores(graph=graph, display=True)]])

        if "degree_centrality" in commands or all_checked:
            commands.append([["degree_centrality"], [AnalyticsGraph.degree_centrality_scores(graph=graph, display=True)]])

        if "eigenvector_centrality" in commands or all_checked:
            commands.append([["eigenvector_centrality"], [AnalyticsGraph.eigenvector_centrality_scores(graph=graph, display=True)]])

        if "pagerank_centrality" in commands or all_checked:
            commands.append([["pagerank_centrality"], [AnalyticsGraph.pagerank_centrality_scores(graph=graph, display=True)]])

        if "closeness_centrality" in commands or all_checked:
            commands.append([["closeness_centrality"], [AnalyticsGraph.closeness_centrality_scores(graph=graph, display=True)]])

        if "betweenness_centrality" in commands or all_checked:
            commands.append([["betweenness_centrality"], [AnalyticsGraph.betweenness_centrality_scores(graph=graph, display=True)]])

        return results

    def closeness_centrality_scores(self, graph, display=False):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater & Sophie Caroni
        Compute centrality closeness centrality of the graph
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param display: Display the details or not
        :type display: boolean
        :return: Dictionary of nodes as keys and closeness centrality as value
        """
        cc_scores = nx.closeness_centrality(graph)

        if display:
            print("\t\t\t (ANL) : Closeness centrality = ", cc_scores.items())

        return cc_scores

    def pagerank_centrality_scores(self, graph, display=False):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater & Sophie Caroni
        Compute PageRank centrality of the graph
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param display: Display the details or not
        :type display: boolean
        :return: :Dictionary of nodes as keys and PageRank's centrality as value
        """
        pr_scores = nx.pagerank(graph)

        if display:
            print("\t\t\t (ANL) : PageRank = ", pr_scores.items())

        return pr_scores

    def eigenvector_centrality_scores(self, graph, display=False):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater & Sophie Caroni
        Compute eigenvector centrality of the graph
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param display: Display the details or not
        :type display: boolean
        :return: Dictionary of nodes as keys and eigenvector centrality as value
        """
        ec_scores = nx.eigenvector_centrality(graph)

        if display:
            print("\t\t\t (ANL) : Eigenvector centrality = ", ec_scores.items())

        return ec_scores

    def degree_centrality_scores(self, graph, display=False):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater & Sophie Caroni
        Compute degree centrality of the graph
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param display: Display the details or not
        :type display: boolean
        :return: Dictionary of nodes as keys and degree centrality as value
        """
        dc_scores = nx.degree_centrality(graph)

        if display:
            print("\t\t\t (ANL) : Degree centrality = ", dc_scores.items())

        return dc_scores

    def betweenness_centrality_scores(self, graph, display=False):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater & Sophie Caroni
        Compute PageRank centrality of the graph
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param display: Display the details or not
        :type display: boolean
        :return: Dictionary of nodes as keys and betweennes centrality as value
        """
        bc_scores = nx.betweenness_centrality(graph)

        if display:
            print("\t\t\t (ANL) : Betweenness centrality = ", bc_scores.items())

        return bc_scores

    def highest_betweenness_centrality(self, graph, community, display=False):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater
        ...
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param community: List of String - All nodes of a community
        :type community: List of String
        :param display: Display the details or not
        :type display: boolean
        :return: list of the results
        """
        # Create a (sub)graph for the nodes of the choosen community
        subgraph = graph.subgraph(community)

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

    def highest_betweenness_centralities(self, graph, communities, display=False):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater
        ...
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param communities: String [[]] - All communities with all nodes of a community
        :type communities: String [[]]
        :param display: Display the details or not
        :type display: boolean
        :return: list of the results
        """
        current_time = datetime.datetime.now()
        print("\n>> You have called the highest betweeness centrality scores, (at", current_time, "), please wait.")

        popular_nodes = []
        for community in communities:
            popular_nodes.append(AnalyticsGraph.highest_betweenness_centrality(self, graph, community, display))

        if display:
            for x, popular in enumerate(popular_nodes):
                print("\t\t\t (ANL) : ", x, ": ", popular[1], ' with a centrality score of ',
                      round(int(popular[0] * 100), 2), "%")

        current_time = datetime.datetime.now()
        print("<< The highest betweeness centrality scores has finished (at", current_time, ").\n")

        my_export = ""
        for x, popular in enumerate(popular_nodes):
            my_export = my_export + str(x) + ":" + str(popular[1]) + "=" + str(round(int(popular[0] * 100), 2)) + "\n"
        with open('./results/communities_populars.txt', 'w') as file:
            # Write the string variable to the file
            file.write(my_export)

        return popular_nodes

    def clustering_coefficient(self, graph, display=False):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater & Sophie Caroni
        Compute clustering coefficient of the graph
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param display: Display the details or not
        :type display: boolean
        :return: Result of the clustering coefficient
        """
        cc = nx.average_clustering(graph)

        if display:
            print("\t\t\t (ANL) : Clustering coefficient:", cc)

        return cc

    def diameter_centrality(self, graph, display=False):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater & Sophie Caroni
        Compute diameter centrality of the graph
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param display: Display the details or not
        :type display: boolean
        :return: Result of the diameter centrality
        """
        # Get the connected components of the graph
        connected_components = nx.connected_components(graph)

        # Compute the diameter for each connected component
        diameters = [nx.diameter(graph.subgraph(component)) for component in connected_components]

        if display:
            print("\t\t\t (ANL) : Diameters of connected components:", diameters)

        return diameters

    def degree_distribution(self, graph, display=False):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater
        Get the degree distribution of the nodes in the graph
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param display: Display the details or not
        :type display: boolean
        :return: Result of the degree distribution
        """
        # Store the sequence of the degree of each node
        degree_sequence = [d for n, d in graph.degree()]

        # Count the frequency of each degree
        degree_counts = dict(zip(sorted(set(degree_sequence)), [degree_sequence.count(d) for d in sorted(set(degree_sequence))]))

        if display:
            print("\t\t\t (ANL) : Degree distribution:", degree_counts)

        return degree_counts

    # =================================================================================================================
    # COMMUNITY DETECTION HOMEMADE
    # =================================================================================================================
    def amazon_community_detection(self, graph, tag="louvain", run_silhouette=False, display=False):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Community detection algorithm
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param tag: Name of the analysis
        :type tag: string
        :param run_silhouette: Compute silhouette coefficient of not
        :type run_silhouette: boolean
        :param display: Display the details or not
        :type display: boolean
        :return: Found communities
        """
        current_time = datetime.datetime.now()
        print("\n<< You have run the homemade amazon community detection algorithm (at", current_time, ").")

        #=STAGE ONE====================================================================================================
        communities = [{u} for u in graph.nodes()]
        modularity = 1 / pow(sum(dict(graph.degree()).values()), 2)

        graph = graph.__class__()
        graph.add_nodes_from(graph)
        graph.add_weighted_edges_from(graph.edges(data="weight", default=1))
        graph_size = graph.size()

        # Perform the inner logic of the algorithm
        communities, inner_partition, _ = AnalyticsGraph.inner_logic(self, graph, graph_size, communities, display=display)
        still_better = True

        #=STAGE TWO====================================================================================================
        # Continue until the modularity does not improve anymore
        while still_better:
            new_modularity = sum(dict(graph.degree()).values()) / 2
            delta_q = new_modularity - modularity
            if delta_q <= 0:
                break
            modularity = new_modularity

            # =UPDATE WEIGHT===========================================================================
            # Update weigth of the graph edges according to the current inner partition
            updated_graph = graph.__class__()
            dict_idx = {}
            for i, part in enumerate(inner_partition):
                nodes = set()
                for node in part:
                    dict_idx[node] = i
                    nodes.add(node)
                updated_graph.add_node(i, nodes=nodes)
            for node1, node2, wt in graph.edges(data=True):
                wt = wt["weight"]
                com1 = dict_idx[node1]
                com2 = dict_idx[node2]
                temp = updated_graph.get_edge_data(com1, com2, {"weight": 0})["weight"]
                updated_graph.add_edge(com1, com2, weight=wt + temp)
            graph = updated_graph
            # =============================================================================
            communities, inner_partition, still_better = AnalyticsGraph.inner_logic(self, graph, graph_size,
                                                                                    communities, display=display)

        # ==DISPLAY=====================================================================================================
        best_communities = list(communities)
        print("\t\t(ANL) : Community detection (louvain homemade) result :")
        for x, c in enumerate(best_communities):
            print("\t\t\t(ANL) : ", x, ": ", c)

        # ==SAVE========================================================================================================
        VisualizationGraph.save_communities(self, best_communities, tag)

        # ==ANALYTICS===================================================================================================
        if run_silhouette:
            AnalyticsGraph.silhouette_score(self, graph=graph, community_detection=best_communities,
                                            metric="euclidean", sample_size=1000)
        # ==============================================================================================================

        current_time = datetime.datetime.now()
        print("<< The homemade amazon community detection algorithm has finished (at", current_time, ").\n")
        return best_communities

    def inner_logic(self, graph, size_of_graph, communities, display=True):
        """
        Creator : Quentin Nater
        reviewed by :
        Inner logic of the community detection algorithm
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param size_of_graph:
        :type size_of_graph: int
        :param communities: Commmunities
        :type communities: list
        :param display: Display the details or not
        :type display: boolean
        """
        #===STAGE THREE================================================================================================
        communityNodes, newCommunity = {}, []

        # *** INITIALIZATION AND THE ALGO AND LIST *****************************
        # initialization of the community with each node as community
        still_better     = False
        operations      = 1
        pushNodeList    = list(graph.nodes)
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
                remove_cost = (-weightCommunity[bestCommunity] / size_of_graph
                               + (out_degree * degreeStrengthIn[bestCommunity]
                                  + in_degree * degreeStrengthOut[bestCommunity])
                               / size_power)

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

                    still_better = True
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

        return communities, newCommunity, still_better

    # =================================================================================================================
    # QUALITY OF THE COMMUNITY DETECTION
    # =================================================================================================================

    def accuracy_precision_recall_jaccard(self, communities_library, community_homemade, display=True):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Compute the score of Accuracy, Precision, Recall and Jaccard, comparing two community detections
        :param communities_library: All communities detected by the networkX library
        :type communities_library: list(set)
        :param community_homemade: All communities detected by the homemade algorithm
        :type community_homemade: list(set)
        :param display: Display the details or not
        :type display: boolean
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
        print("<< The Accuracy/Precision/Revall/Jaccard score between the 2 algorithm has finished (at", current_time, ").\n")

        return accuracy, precision, recall, jaccard

    def silhouette_score(self, graph, community_detection, metric='euclidean', sample_size=None):
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
        print("\t<< The Silhouette Index Score has finished (at", current_time, ").\n")

        return silhouette
