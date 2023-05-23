import datetime
import heapq
import networkx as nx
import re
from matplotlib import pyplot as plt


class ExploreGraph:

    def convert_asin_to_int(self, asin):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Convert the id (ASIN) into a unique integer
        :param asin: Id of the node
        :type asin: string
        :return: aA integer corresponding to the converted asin
        """

        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # Identify the presence of letters in the asin
        if any(char.isalpha() for char in asin):  # isalpha() returns True if it detects letters
            for char in asin:
                if char.isalpha():

                    # Replace each letter by the number of its alphabet's position, adding 10 to ensure unique result
                    asin = asin.replace(char, str(alphabet.index(char.upper()) + 10))

        return int(asin)

    def construct_graph_by_file(self, file_name, limit=15010574, display=True, display_detail=False):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Construct a complex graph with a file
        :param file_name: Path to the dataset
        :type file_name: string
        :param limit: Limit of the line to read (sample)
        :type limit: int
        :param display: Display the results of the analysis
        :type display: bool
        :param display_detail: Display the detail of the construction
        :type display_detail: bool
        :return: The constructed graph and the run time
        """
        current_time = datetime.datetime.now()
        print("\n<< You have called the construction of your graph (at", current_time, ").")

        # initialization of the variables
        graph = nx.DiGraph()
        i, asin_int, not_out_edged = 0, 0, 0
        list_asin, list_similars, list_not_out_edged, list_not_in_edged, list_extern = [], [], [], [], []

        # read every information of the file (dataset)
        with open(file_name, "r", encoding='utf-8') as f:
            for line in f:
                i += 1  # inc break

                # read nodes
                match = re.search(r'ASIN:\s*(\w+)', line)  # each ASIN
                if match:
                    asin = match.group(1)  # Take the first element matched

                    # add a node to the graph for the ASIN value (INT)
                    asin_int = ExploreGraph.convert_asin_to_int(self, asin)
                    graph.add_node(asin_int)
                    list_asin.append(asin_int)

                # read edges
                match = re.search(r'similar:\s*(\w+)', line)  # each similar
                if match:
                    similars = line.split(sep="  ")  # Create a list of each one of the similars as an element
                    inc = 0

                    for similar in similars:
                        inc += 1

                        if inc > 2:  # skip two initial blank spaces; only if there are more than 0 similars
                            similar_int = ExploreGraph.convert_asin_to_int(self, similar)  # casting
                            list_similars.append(similar_int)

                            # add edges between the asin product and each of its similar ones
                            graph.add_edge(*(asin_int, similar_int))

                            if display_detail:
                                print("\t\t\t\t(" + str(asin_int) + ", " + str(similar_int) + ")")

                        elif len(similars) == 2:  # information if it has 0 similars
                            not_out_edged += 0.5  # correct the two times entering the loop
                            if not_out_edged % 1 == 0:
                                asin_i = ExploreGraph.convert_asin_to_int(self, asin)  # casting
                                list_not_out_edged.append(asin_i)

                # stop reading file when the given line limit is reached
                if i == limit:
                    break

        n_nodes, n_edges = graph.number_of_nodes(), graph.number_of_edges()


        if display:
            list_similars = list(set(list_similars))  # remove redundancy (duplicates)
            list_not_out_edged = set(list_not_out_edged)  # casting

            # identify products never appearing as similar of others
            list_not_in_edged = set(list_asin) - set(list_similars)

            # identify products only appearing as similar of others
            list_extern = set(list_similars) - set(list_asin)

            # identify disconnected nodes
            total_isolated = list_not_in_edged & list_not_out_edged

            print("\t\t\t\tASIN : \t\t\t\t\t\t\t" + str(len(list_asin)))
            print("\t\t\t\tSIMILARS (UNIQUES) \t\t\t\t" + str(len(list_similars)))
            print("\t\t\t\tNOT IN-EDGED NODES: \t\t\t" + str(len(list_not_in_edged)))
            print("\t\t\t\tNODES CREATED OUTSIDE (FILE) : \t" + str(len(list_extern)))
            print("\t\t\t\tNOT OUT-EDGED NODES: \t\t\t" + str(int(not_out_edged)))
            print("\t\t\t\tISOLATED NODES: \t\t\t\t" + str(len(total_isolated)), "\n")

        end_time = datetime.datetime.now()
        print(">>The graph has been successfully constructed! (at", end_time, ") (nodes:" + str(n_nodes) + ", edges:" + str(n_edges) + ")")

        run_time = end_time-current_time

        return graph, run_time

    def analytics_exploration(self, graph, display=False):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater & Sophie Caroni
        Get all needed analytics for exploration
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param display: Display or not the plots and prints
        :type display: Boolean
        """
        print(">> You have called the construction of your graph, please wait :)")

        if display:
            ExploreGraph.simple_plotting(self, graph)

        first_node = list(graph.nodes())[0]
        path_dfs = ExploreGraph.dfs_iterative(self, graph, first_node)

        print("\t\t\t (EXP) : All nodes visited nodes (path_dfs) : ", path_dfs)
        print("\t\t\t (EXP) : Size of path_dfs ", len(path_dfs))
        print("\t\t\t (EXP) : Number of nodes:", graph.number_of_nodes())

        if display:
            ExploreGraph.draw_path_graph(self, graph, path_dfs)

        start_node = list(graph.nodes())[0]
        goal_node = list(graph.nodes())[13]
        path_star = ExploreGraph.a_star_search(self, graph, start_node, goal_node)

        if path_star is not None:
            print("\t\t\t (EXP) : Small walk (0->13) -> visited nodes (path_star) : ", path_star)
            print("\t\t\t (EXP) : Small walk (0->13) -> size of path ", len(path_star))
            print("\t\t\t (EXP) : Small walk (0->13) -> found:", " -> ", path_star)
            if display:
                ExploreGraph.draw_path_graph(self, graph, path_star)


    def draw_path_graph(self, graph, path, tag="visualization_graph"):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater & Sophie Caroni
        Display all the path inside the graph plot
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param path: Path with all nodes
        :type path: list
        :param tag: Part of the file name of the figure that will be saved
        :type tag: string
        """
        print(">> You have called the plot of your graph with draw of the path, please wait :)")

        # Calculate the layout positions of the nodes using the spring layout algorithm
        pos = nx.spring_layout(graph, seed=42)

        # Draw the graph with labeled nodes
        nx.draw(graph, pos, with_labels=True, node_color="lightblue", node_size=400, font_size=10)

        if path:
            # Generate a list of edges from the given path
            edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]

            # Draw only the edges from the path with a different color and thicker width
            nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color='r', width=2)

        plt.title("Draw Path Algorithm")
        plt.show()

        # Save the plot as PNG file
        plt.savefig("./plots/draw_path_graph_" + str(tag) + ".png")

    def simple_plotting(self, graph, tag="visualization_graph"):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater & Sophie Caroni
        Simple plot the graph with better view
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param tag: Part of the file name of the figure that will be saved
        :type tag: string
        """
        print(">> You have called the plot of your graph, please wait :)")

        # Visualize the graph
        plt.figure(figsize=(10, 6))
        nx.draw(graph, node_size=10, edge_color='grey', alpha=0.5)
        plt.title("Simple Plot")
        plt.savefig("./plots/simple_plotting_" + tag + ".png")
        plt.show()

    def dfs(self, graph, node, visited):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater & Sophie Caroni
        Complete exploration through a Depth-First-Search
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param node: String - First node of the graph (current used)
        :type node: String
        :param visited: List of current the visited nodes
        :type visited: list
        """
        if node not in visited:
            visited.append(node)
            if node in graph:
                for neighbor in graph[node]:
                    ExploreGraph.dfs(self, graph, neighbor, visited)
        return visited

    def a_star_search(self, graph, start, goal):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater
        Exploration from one node to one other with A* algo method
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param start: Starting point of the graph (node)
        :type start: String
        :param goal: Destination point of the graph (node)
        :type goal: list
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

    def dfs_iterative(self, graph, starting_node):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater
        Complete exploration through a Depth-First-Search
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param starting_node: First node of the graph (current used)
        :type starting_node: String
        """
        visited = set()
        stack = [starting_node]

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                if node in graph:
                    for neighbor in graph[node]:
                        stack.append(neighbor)
        return visited

    def explore_community(self, graph, community, display=False):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Explore all nodes of a community and draw all their connect via DFS algorithm
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param community: List of community (list of nodes)
        :type community: String [[]]
        :param display: Display the plot
        :type display: bool
        """
        # Set the community as being a proper graph
        subgraph = graph.subgraph(community)

        # Apply dfs starting from the first node of the graph
        first_node = list(subgraph.nodes())[0]
        path_dfs = ExploreGraph.dfs(self, subgraph, first_node, [])

        # Possibly show the found path
        if display:
            print("\t\t\t (EXP) : All nodes visited nodes (path_dfs) : ", path_dfs)
            print("\t\t\t (EXP) : Size of path_dfs ", len(path_dfs))
            print("\t\t\t (EXP) : Number of nodes:", subgraph.number_of_nodes())

            ExploreGraph.draw_path_graph(self, subgraph, path_dfs)