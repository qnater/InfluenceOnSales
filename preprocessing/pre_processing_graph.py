import datetime
import random
import networkx as nx


class PreProcessGraph:

    def refine_graph(self, graph):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Remove nodes that are isolated
        :param graph: Graph networkX of the amazon dataset
        :type graph: networkX
        :return: The refined graph
        """
        # Before the refinement
        PreProcessGraph.display_efficiency_of_graph(self, graph)

        # Refinement: remove irrelevant nodes
        graph = PreProcessGraph.remove_isolated_nodes(self, graph)
        graph = PreProcessGraph.remove_not_in_edged_nodes(self, graph)
        graph = PreProcessGraph.remove_not_out_edged_nodes(self, graph)

        print(">> Final pre-processing results : ",
              "\n\t\t\t\tNodes in the refined graph :\t\t", len(graph.nodes()),
              "\n\t\t\t\tEdges in the refined graph :\t\t", len(graph.edges()), "\n")

        # After the refinement
        PreProcessGraph.display_efficiency_of_graph(self, graph)

        return graph

    def refine_graph_k(self, graph, k=0, limit=200000):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Clean the dataset and create sample of the graph
        :param graph: Graph networkX of the amazon dataset
        :type graph: networkX
        :param k: Node(s) with this number of degree will be removed, in case the cleaning is stuck before the limit
        :type k: int
        :param limit: Number of nodes desired for the refined graph
        :type limit: int
        :return: The refined graph
        """
        current_time = datetime.datetime.now()
        print(">> You have called the in depth refinement of the graph, (at", current_time, "), please wait.")

        # Keep track of the current number of nodes of the graph
        inc, current_score = 1, 0

        # Loop until the number of nodes in the graph is less than the specified limit
        while limit < graph.number_of_nodes():
            current_score = graph.number_of_nodes()

            # If the score is not changing (there are not any useless nodes) start removing edges of degree k+1
            if current_score == graph.number_of_nodes():
                k += 1
                graph = PreProcessGraph.remove_nodes_by_degree(self, graph, k)
                print("\t\t\t\t(PRE-PRO) : Change k - ", k)

                # To keep the lowest k possible, reset it if the number of nodes changes after removing nodes with the current k
                if current_score != graph.number_of_nodes():
                    k = 0

            print("\t\t\t\t(PRE-PRO) : number loops : ", inc, " : ", graph.number_of_nodes(), " for k = ", k)
            graph = PreProcessGraph.refine_graph(self, graph)
            inc += 1

        print("\t\t\t\t(PRE-PRO) : current number of nodes : ", graph.number_of_nodes())

        current_time = datetime.datetime.now()
        print("<< The refinement of the graph (perfect) has finished (at", current_time, ").")

        # Further refine the graph to eliminate the nodes being isolated from the last refinement
        graph = PreProcessGraph.refine_graph(self, graph)

        return graph

    def remove_isolated_nodes(self, graph):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Remove nodes that are isolated
        :param graph: Graph networkX of the amazon dataset
        :type graph: networkX
        :return: The graph without isolated nodes
        """
        print(">> You have called the pre-processing function to refine your graph (isolated), please wait .")

        isolatedNodes = list(nx.isolates(graph))

        originalAmount, originalEdges = len(graph.nodes()), len(graph.edges())

        graph.remove_nodes_from(isolatedNodes)

        print("\t\t\t\tNumber of isolated node detected :\t", len(isolatedNodes),
              "\n\t\t\t\tNodes in the original graph:\t\t", originalAmount,
              "\n\t\t\t\tEdges in the original graph:\t\t", originalEdges,
              "\n\t\t\t\tNodes in the refined graph :\t\t", len(graph.nodes()),
              "\n\t\t\t\tEdges in the refined graph :\t\t", len(graph.edges()), "\n")

        return graph

    def remove_not_in_edged_nodes(self, graph):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Remove nodes not having any incoming edge
        :param graph: Graph networkX of the amazon dataset
        :type graph: networkX
        :return: The graph without nodes not having any incoming edge
        """
        print(
            ">> You have called the pre-processing function to refine your graph (without incoming edges), please wait.")

        notIncomingEdges = []
        for node, in_degree in graph.in_degree():
            if in_degree == 0:
                notIncomingEdges.append(node)

        originalAmount, originalEdges = len(graph.nodes()), len(graph.edges())

        graph.remove_nodes_from(notIncomingEdges)

        print("\t\t\t\tNumber of not incoming edged node detected :\t", len(notIncomingEdges),
              "\n\t\t\t\tNodes in the original graph:\t\t", originalAmount,
              "\n\t\t\t\tEdges in the original graph:\t\t", originalEdges,
              "\n\t\t\t\tNodes in the rafined graph :\t\t", len(graph.nodes()),
              "\n\t\t\t\tEdges in the rafined graph :\t\t", len(graph.edges()), "\n")

        return graph

    def remove_not_out_edged_nodes(self, graph):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Remove nodes not having any outgoing edge
        :param graph: Graph networkX of the amazon dataset
        :type graph: networkX
        :return: The graph without nodes not having any outgoing edge
        """
        print(
            ">> You have called the pre-processing function to refine your graph (without outgoing edges), please wait.")

        notOutgoingEdges = []

        for node, out_degree in graph.out_degree():
            if out_degree == 0:
                notOutgoingEdges.append(node)

        originalAmount, originalEdges = len(graph.nodes()), len(graph.edges())

        graph.remove_nodes_from(notOutgoingEdges)

        print("\t\t\t\tNumber of not outgoing edged node detected :\t", len(notOutgoingEdges),
              "\n\t\t\t\tNodes in the original graph:\t\t", originalAmount,
              "\n\t\t\t\tEdges in the original graph:\t\t", originalEdges,
              "\n\t\t\t\tNodes in the refined graph :\t\t", len(graph.nodes()),
              "\n\t\t\t\tEdges in the refined graph :\t\t", len(graph.edges()), "\n")

        return graph

    def remove_nodes_by_degree(self, graph, k):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Remove nodes having less than degree k
        :param graph: Graph networkX of the amazon dataset
        :type graph: networkX
        :param k: Threshold of node-degree
        :type k: int
        :return: The refined graph, only having nodes with degree more than k
        """
        print(">> You have called the pre-processing function to refine your graph (by node degree), please wait.")

        # Before the refinement
        PreProcessGraph.display_efficiency_of_graph(self, graph)

        nodeToEliminate = []

        for node, degree in graph.out_degree():
            if degree <= k:
                nodeToEliminate.append(node)

        originalAmount, originalEdges = len(graph.nodes()), len(graph.edges())

        graph.remove_nodes_from(nodeToEliminate)

        print("\t\t\t\tNumber of  node detected :\t\t\t", len(nodeToEliminate),
              "\n\t\t\t\tNodes in the original graph:\t\t", originalAmount,
              "\n\t\t\t\tEdges in the original graph:\t\t", originalEdges,
              "\n\t\t\t\tNodes in the refined graph :\t\t", len(graph.nodes()),
              "\n\t\t\t\tEdges in the refined graph :\t\t", len(graph.edges()), "\n")

        # After the refinement
        PreProcessGraph.display_efficiency_of_graph(self, graph)

        return graph

    def display_score_by_degree(self, graph, n):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Generate an array of arrays of n nodes. Each node in each array has a specific degree
        :param graph: Graph networkX of the amazon dataset
        :type graph: networkX
        :param n: Number of random node of each degree to keep
        :type n: int
        :return: nodeDegree - array of arrays of n nodes. Each node in each array has a specific degree.
        """
        print(">> You have called the pre-processing function to refine your graph (display degree), please wait.")

        # Store nodes of each different degree (1-8) in a list
        nodeDegrees = [[], [], [], [], [], []]

        # Initialize a counter for each degree category
        inc = [0, 0, 0, 0, 0, 0, 0, 0]

        # Loop until n nodes of each degree category have been found
        while inc[0] < n * 6:
            node = random.choice(list(graph.nodes()))

            nodeDegree = graph.degree[node]

            # Check the degree and add the node to the appropriate category
            if nodeDegree == 0 and inc[1] < n:
                nodeDegrees[0].append(node)
                inc[0] = inc[0] + 1
                inc[1] = inc[1] + 1
            elif nodeDegree == 1 and inc[2] < n:
                nodeDegrees[1].append(node)
                inc[0] = inc[0] + 1
                inc[2] = inc[2] + 1
            elif nodeDegree == 2 and inc[3] < n:
                nodeDegrees[2].append(node)
                inc[0] = inc[0] + 1
                inc[3] = inc[3] + 1
            elif nodeDegree == 3 and inc[4] < n:
                nodeDegrees[3].append(node)
                inc[0] = inc[0] + 1
                inc[4] = inc[4] + 1
            elif nodeDegree == 4 and inc[5] < n:
                nodeDegrees[4].append(node)
                inc[0] = inc[0] + 1
                inc[5] = inc[5] + 1
            elif nodeDegree == 5 and inc[6] < n:
                nodeDegrees[5].append(node)
                inc[0] = inc[0] + 1
                inc[6] = inc[6] + 1

        # Iterate over each degree category in nodeDegrees
        for i, degree in enumerate(nodeDegrees):
            print(i, ": ", degree)
            # Iterate over each node in the degree category
            for node in degree:
                # Calculate the degree centrality of each node
                degree_centrality = nx.degree_centrality(graph)[node]

                print(f"\t\t\tDegree centrality of node {node}\t\t: {degree_centrality}")

        return nodeDegrees

    def display_efficiency_of_graph(self, graph, write=False, tag="efficiency", run_time=0, scenario="1"):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Display efficiency of the graph with coefficient clustering and average of degrees
        :param graph: Graph networkX of the amazon dataset
        :type graph: networkX
        :param write: Write the result in the database
        :type write: bool
        :param tag: Name of the filename with the results
        :type tag: string
        :param run_time: Time of the run of the graph construction
        :type run_time: float
        :param scenario: Number of scenario played
        :type scenario: string
        """
        degrees = [graph.degree(n) for n in graph.nodes()]
        number_of_edges = graph.number_of_edges()
        number_of_nodes = graph.number_of_nodes()
        coefficient_clustering = nx.average_clustering(graph)
        avg_degree = (sum(degrees) / len(degrees))
        print("\n\t\t\t\t\t\t (I) number of edges        :\t", number_of_edges,
              "\n\t\t\t\t\t\t (I) coefficient clustering :\t", coefficient_clustering,
              "\n\t\t\t\t\t\t (I) average of degrees     :\t", avg_degree, "\n\n")

        if write:
            with open("./results/scenario_"+str(scenario)+"/" + str(tag) + ".txt", 'w') as file:
                file.write("The efficiency of the graph " + str(tag) +
                           "\nRun Time : " + str(run_time) +
                           "\nNumber of Nodes : " + str(number_of_nodes) +
                           "\nNumber of Edges : " + str(number_of_edges) +
                           "\nClustering Coefficient : " + str(coefficient_clustering) +
                           "\nAverage Degree : " + str(avg_degree))
