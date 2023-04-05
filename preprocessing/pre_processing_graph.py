from random import random

import networkx as nx


class PreProcessGraph:


    def refined_graph(graph):
        """
        Creator : Quentin Nater
        reviewed by :
        Remove nodes that are isolated
        :param graph: networkX - Graph networkX of the amazon dataset
        :type graph: networkX
        :return: The graph refined
        """

        graph = PreProcessGraph.remove_isolated_nodes(graph)
        graph = PreProcessGraph.remove_not_incoming_edged_nodes(graph)
        graph = PreProcessGraph.remove_not_outgoing_edges_nodes(graph)

        print(">> Final pre-processing results : ",
              "\n\t\t\t\tNodes in the refined graph :\t\t", len(graph.nodes()),
              "\n\t\t\t\tEdges in the refined graph :\t\t", len(graph.edges()), "\n")

        return graph

    def remove_isolated_nodes(graph):
        """
        Creator : Quentin Nater
        reviewed by :
        Remove nodes that are isolated
        :param graph: networkX - Graph networkX of the amazon dataset
        :type graph: networkX
        :return: The graph refined
        """
        print(">> You have called the pre-processing function to refined your graph (isolated), please wait :)")

        isolatedNodes = list(nx.isolates(graph))

        originalAmount, originalEdges = len(graph.nodes()), len(graph.edges())

        graph.remove_nodes_from(isolatedNodes)

        print("\t\t\t\tNumber of isolated node detected :\t", len(isolatedNodes),
              "\n\t\t\t\tNodes in the original graph\t\t\t", originalAmount,
              "\n\t\t\t\tEdges in the original graph\t\t\t", originalEdges,
              "\n\t\t\t\tNodes in the refined graph :\t\t", len(graph.nodes()),
              "\n\t\t\t\tEdges in the refined graph :\t\t", len(graph.edges()), "\n")

        return graph

    def remove_not_incoming_edged_nodes(graph):
        """
        Creator : Quentin Nater
        reviewed by :
        Remove nodes that are not in edged
        :param graph: networkX - Graph networkX of the amazon dataset
        :type graph: networkX
        :return: The graph refined
        """
        print(">> You have called the pre-processing function to refined your graph (not in edged), please wait :)")

        notIncomingEdges = []
        for node, in_degree in graph.in_degree():
            if in_degree == 0:
                notIncomingEdges.append(node)

        originalAmount, originalEdges = len(graph.nodes()), len(graph.edges())

        graph.remove_nodes_from(notIncomingEdges)

        print("\t\t\t\tNumber of not incoming edged node detected :\t", len(notIncomingEdges),
              "\n\t\t\t\tNodes in the original graph\t\t\t", originalAmount,
              "\n\t\t\t\tEdges in the original graph\t\t\t", originalEdges,
              "\n\t\t\t\tNodes in the rafined graph :\t\t", len(graph.nodes()),
              "\n\t\t\t\tEdges in the rafined graph :\t\t", len(graph.edges()), "\n")

        return graph

    def remove_not_outgoing_edges_nodes(graph):
        """
        Creator : Quentin Nater
        reviewed by :
        Remove nodes that are not out edged
        :param graph: networkX - Graph networkX of the amazon dataset
        :type graph: networkX
        :return: The graph refined
        """
        print(">> You have called the pre-processing function to refined your graph (not out edged), please wait :)")

        notOutgoingEdges = []

        for node, out_degree in graph.out_degree():
            if out_degree == 0:
                notOutgoingEdges.append(node)

        originalAmount, originalEdges = len(graph.nodes()), len(graph.edges())

        graph.remove_nodes_from(notOutgoingEdges)

        print("\t\t\t\tNumber of not outgoing edged node detected :\t", len(notOutgoingEdges),
              "\n\t\t\t\tNodes in the original graph\t\t\t", originalAmount,
              "\n\t\t\t\tEdges in the original graph\t\t\t", originalEdges,
              "\n\t\t\t\tNodes in the refined graph :\t\t", len(graph.nodes()),
              "\n\t\t\t\tEdges in the refined graph :\t\t", len(graph.edges()), "\n")

        return graph

    def remove_nodes_by_degree(graph, k):
        """
        Creator : Quentin Nater
        reviewed by :
        Remove nodes that are less than a certain degree
        :param graph: networkX - Graph networkX of the amazon dataset
        :type graph: networkX
        :param k: int - Threshold of degree, less than k degree will be remove
        :type k: int
        :return: The graph refined
        """

        print(">> You have called the pre-processing function to refined your graph (by degree), please wait :)")

        nodeToEliminate = []

        for node, degree in graph.degree():
            if degree < k:
                nodeToEliminate.append(node)

        originalAmount, originalEdges = len(graph.nodes()), len(graph.edges())

        graph.remove_nodes_from(nodeToEliminate)

        print("\t\t\t\tNumber of not node detected :\t", len(nodeToEliminate),
              "\n\t\t\t\tNodes in the original graph\t\t\t", originalAmount,
              "\n\t\t\t\tEdges in the original graph\t\t\t", originalEdges,
              "\n\t\t\t\tNodes in the refined graph :\t\t", len(graph.nodes()),
              "\n\t\t\t\tEdges in the refined graph :\t\t", len(graph.edges()), "\n")

        return graph

    def display_score_by_degree(graph, n):
        """
        :author:Quentin Nater
        reviewed by :
        Generate an array of array of n nodes. Each node in each array has a specific degree.
        :param graph: networkX - Graph networkX of the amazon dataset
        :type graph: networkX
        :param n: int - Number of random node of each degree to keep
        :type n: int
        :return: nodeDegree - array of array of n nodes. Each node in each array has a specific degree.
        """

        print(">> You have called the pre-processing function to refined your graph (display degree), please wait :)")

        nodeDegree = [0, 0, 0, 0, 0, 0]

        inc = [0, 0, 0, 0, 0, 0, 0, 0]

        while inc[0] < n * 6:
            node = random.choice(list(graph.nodes()))

            nodeDegree = node.degree()

            if nodeDegree == 0 and inc[1] <= n:
                nodeDegree[0].append(node)
                inc[0] = inc[0] + 1
                inc[1] = inc[1] + 1
            elif nodeDegree == 1 and inc[2] <= n:
                nodeDegree[1].append(node)
                inc[0] = inc[0] + 1
                inc[2] = inc[2] + 1
            elif nodeDegree == 2 and inc[3] <= n:
                nodeDegree[2].append(node)
                inc[0] = inc[0] + 1
                inc[3] = inc[3] + 1
            elif nodeDegree == 3 and inc[4] <= n:
                nodeDegree[3].append(node)
                inc[0] = inc[0] + 1
                inc[4] = inc[4] + 1
            elif nodeDegree == 4 and inc[5] <= n:
                nodeDegree[4].append(node)
                inc[0] = inc[0] + 1
                inc[5] = inc[5] + 1
            elif nodeDegree == 5 and inc[6] <= n:
                nodeDegree[5].append(node)
                inc[0] = inc[0] + 1
                inc[6] = inc[6] + 1

        for degree in nodeDegree:
            print(degree)
            for node in degree:
                print("\t", node)

        return nodeDegree
