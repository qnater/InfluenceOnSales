import heapq

import networkx as nx
import re

from matplotlib import pyplot as plt


class ExploreGraph:

    def convert_asin_to_int(asin):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Convert the id (ASIN) into a INT unique value
        :param asin: string - ID of the node
        :return: an integer corresponding to the converted asin
        """
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if any(char.isalpha() for char in asin):  # isalpha() returns True if it detects letters
            for char in asin:
                if char.isalpha():
                    asin = asin.replace(char, str(alphabet.index(char.upper()) + 10))

        return int(asin)

    def construct_graph_by_file(file_name, limit=15010574, display=True, displayDetail=False):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Construct a complex graph with a file
        :param filename: string - path to the dataset
        :param limit: int - limit of the line to read (sample)
        :param display: bool - display the results of the analysis
        :param displayDetail: bool - display the detail of the construction
        :return: an integer corresponding to the converted asin
        """
        print(">> You have called the construction of your graph, please wait :)")

        # initialization of the variables
        graph = nx.DiGraph()
        i, asin_int, notOutEdged = 0, 0, 0
        list_asin, list_similars, list_not_out_edged, list_not_in_edged, list_extern = [], [], [], [], []

        # read every information of the file (dataset)
        with open(file_name, "r", encoding='utf-8') as f:
            for line in f:

                i += 1  # inc break

                # read nodes ===============================================
                match = re.search(r'ASIN:\s*(\w+)', line)  # each ASIN
                if match:
                    asin = match.group(1)  # Take the first element matched

                    # add a node to the graph for the ASIN value (INT)
                    asin_int = ExploreGraph.convert_asin_to_int(asin)
                    graph.add_node(asin_int)
                    list_asin.append(asin_int)

                # read edges ===============================================
                match = re.search(r'similar:\s*(\w+)', line)  # each similar
                if match:
                    similars = line.split(sep="  ")  # Create a list of each one of the similars as an element
                    inc = 0

                    for similar in similars:
                        inc += 1

                        if inc > 2:  # skip two initial blank spaces; only if there are more than 0 similars
                            similar_int = ExploreGraph.convert_asin_to_int(similar)  # casting
                            list_similars.append(similar_int)
                            graph.add_edge(*(asin_int, similar_int))  # Add edges between the asin product and each of its similar ones

                            if displayDetail:
                                print("\t\t\t\t(" + str(asin_int) + ", " + str(similar_int) + ")")

                        elif len(similars) == 2:  # information if it has 0 similars (CHECK FOR ANALYSIS)
                            notOutEdged += 0.5  # to correct the two times entering the loop
                            if notOutEdged % 1 == 0:
                                asin_i = ExploreGraph.convert_asin_to_int(asin)  # casting
                                list_not_out_edged.append(asin_i)

                # Stop reading file when the given line limit is reached =======================================
                if i == limit:
                    break

        nNodes, nEdges = graph.number_of_nodes(), graph.number_of_edges()
        print("\t\tThe graph has been successfully constructed! (nodes:" + str(nNodes) + ", edges:" + str(nEdges) + ")")

        if display:
            list_similars = list(set(list_similars))  # remove redundancy (duplicates)
            list_not_out_edged = set(
                list_not_out_edged)  # casting ## should'nt this be remove redundancy instead of casting?

            list_not_in_edged = set(list_asin) - set(list_similars)  # find products with asin but not appearing as similars of others
            list_extern = set(list_similars) - set(list_asin)  # find products appearing as similars but not defined in this dataset file

            total_isolated = list_not_in_edged & list_not_out_edged  # find disconnected nodes

            print("\t\t\t\tASIN : \t\t\t\t\t\t\t" + str(len(list_asin)))
            print("\t\t\t\tSIMILARS (UNIQUES) \t\t\t\t" + str(len(list_similars)))
            print("\t\t\t\tNOT IN-EDGED NODES: \t\t\t" + str(len(list_not_in_edged)))
            print("\t\t\t\tNODES CREATED OUTSIDE (FILE) : \t" + str(len(list_extern)))
            print("\t\t\t\tNOT OUT-EDGED NODES: \t\t\t" + str(int(notOutEdged)))
            print("\t\t\t\tISOLATED NODES: \t\t\t\t" + str(len(total_isolated)), "\n")

        return graph

    def analytics_exploration(graph, display=False):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater
        Get all needed analytics for exploration
        :param graph: networkX - Graph networkX (of the amazon dataset refined)
        :type graph: networkX
        :param display: Boolean - Display or not the plots and prints
        :type display: Boolean
        """

        print(">> You have called the construction of your graph, please wait :)")
        if display:
            ExploreGraph.simple_plotting(graph)

        first_node = list(graph.nodes())[0]
        pathDFS = ExploreGraph.dfs(graph, first_node, [])

        print("\t\t\t (EXP) : All nodes visited nodes (pathDFS) : ", pathDFS)
        print("\t\t\t (EXP) : Size of pathDFS ", len(pathDFS))
        print("\t\t\t (EXP) : Number of nodes:", graph.number_of_nodes())

        if display:
            ExploreGraph.draw_path_graph(graph, pathDFS)

        start_node = list(graph.nodes())[0]
        goal_node = list(graph.nodes())[13]
        pathStar = ExploreGraph.a_star_search(graph, start_node, goal_node)

        if pathStar is not None:
            print("\t\t\t (EXP) : All nodes visited nodes (pathStar) : ", pathStar)
            print("\t\t\t (EXP) : Size of pathStar ", len(pathStar))
            print("\t\t\t (EXP) : pathStar found:", " -> ", pathStar)
            if display:
                ExploreGraph.draw_path_graph(graph, pathStar)
        else:
            print("\t\t\t (EXP) : Path not found")

    def draw_path_graph(graph, path, tag="visualization_graph"):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater
        Display all the path inside the graph plot
        :param graph: networkX - Graph networkX (of the amazon dataset refined)
        :type graph: networkX
        :param path: String[] - Path with all nodes
        :type path: String[]
        """
        print(">> You have called the plot of your graph with draw of the path, please wait :)")

        pos = nx.spring_layout(graph, seed=42)
        nx.draw(graph, pos, with_labels=True, node_color="lightblue", node_size=400, font_size=10)
        if path:
            edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color='r', width=2)
        plt.title("Draw Path Algorithm")
        plt.show()

        plt.savefig("./plots/draw_path_graph_" + str(tag) + ".png")

    def simple_plotting(graph, tag="visualization_graph"):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater
        Simple plot the graph with better view
        :param graph: networkX - Graph networkX (of the amazon dataset refined)
        :type graph: networkX
        """
        print(">> You have called the plot of your graph, please wait :)")

        # Visualize the graph
        plt.figure(figsize=(10, 6))
        nx.draw(graph, node_size=10, edge_color='grey', alpha=0.5)
        plt.title("Simple Plot")
        plt.savefig("./plots/simple_plotting_" + tag + ".png")
        plt.show()


    def dfs(graph, node, visited):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater
        Complete exploration through a Depth-First-Search
        :param graph: networkX - Graph networkX (of the amazon dataset refined)
        :type graph: networkX
        :param node: String - First node of the graph (current used)
        :type node: String
        :param visited: String[] - List of current the visited nodes
        :type visited: String[]
        """
        if node not in visited:
            visited.append(node)
            if node in graph:
                for neighbor in graph[node]:
                    ExploreGraph.dfs(graph, neighbor, visited)
        return visited

    def a_star_search(graph, start, goal):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater
        Exploration from one node to one other with A* algo method
        :param graph: networkX - Graph networkX (of the amazon dataset refined)
        :type graph: networkX
        :param start: String - Starting point of the graph (node)
        :type start: String
        :param goal: String[] - Destination point of the graph (node)
        :type goal: String[]
        """
        frontier = [(0, start, [])]  # (priority, node, path)
        explored = set()
        heuristic = 0

        while frontier:
            cost, current, path = heapq.heappop(frontier)
            if current == goal:
                return path + [current]

            if current not in explored:
                explored.add(current)
                if current in graph:
                    for neighbor in graph[current]:
                        new_cost = cost + 1 + heuristic
                        heapq.heappush(frontier, (new_cost, neighbor, path + [current]))

        return None

    def dfs_iterative(graph, start_node):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater
        Complete exploration through a Depth-First-Search
        :param graph: networkX - Graph networkX (of the amazon dataset refined)
        :type graph: networkX
        :param start_node: String - First node of the graph (current used)
        :type start_node: String
        """
        visited = set()
        stack = [start_node]

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                if node in graph:
                    for neighbor in graph[node]:
                        stack.append(neighbor)
        return visited

    def exploreCommunity(graph, community, display=False):
        """
         Creator : Quentin Nater
         reviewed by :
         Explore all nodes of a community a draw all their connect via DFS algo
         :param graph: networkX - graph of the dataset
         :type graph: networkX
         :param communities: String [[]] - List of community (list of nodes)
         :type communities: String [[]]
         :param display: bool - display the plot
         :type display: bool
         """
        subgraph = graph.subgraph(community)  # create subgraph with only those nodes

        first_node = list(subgraph.nodes())[0]
        pathDFS = ExploreGraph.dfs(subgraph, first_node, [])

        if display:
            print("\t\t\t (EXP) : All nodes visited nodes (pathDFS) : ", pathDFS)
            print("\t\t\t (EXP) : Size of pathDFS ", len(pathDFS))
            print("\t\t\t (EXP) : Number of nodes:", subgraph.number_of_nodes())

            ExploreGraph.draw_path_graph(subgraph, pathDFS)
