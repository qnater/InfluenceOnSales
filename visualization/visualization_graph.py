import random
import datetime
import re
import matplotlib.pyplot as plt
import networkx as nx


class VisualizationGraph:

    def display_simple_graph(self, graph, display=True, tag="visualization_graph"):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Display a simple graph
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param display: Display the plot
        :type display: bool
        :param tag: Part of the file name of the figure that will be saved
        :type tag: string
        :return: the display of the graph
        """
        current_time = datetime.datetime.now()
        print(">> You have called the display of the full graph, (at", current_time, "), please wait.")

        if display:
            nx.draw(graph, with_labels=True, node_color="lightblue", node_size=400, font_size=10)
            plt.title("Simple Display Plot")
            plt.savefig("./plots/display_simple_graph" + str(tag) + ".png", format="PNG")
            plt.show()

        current_time = datetime.datetime.now()
        print("<< The display of the full graph has finished (at", current_time, ").")

        return graph

    def display_sampled_graph(self, graph, display=True, tag="visualization_graph"):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Display a sample of a graph
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param display: Display the plot
        :type display: bool
        :param tag: Part of the file name of the figure that will be saved
        :type tag: string
        """
        # number of nodes to sample
        num_nodes = 1000

        # randomly sample nodes
        nodes_list = list(graph.nodes())
        sampled_nodes = random.sample(nodes_list, num_nodes)

        # create a subgraph by the sampled nodes
        sampled_graph = graph.subgraph(sampled_nodes)

        if display:
            # draw the sampled graph
            nx.draw(sampled_graph, with_labels=True, node_color="lightblue", node_size=400, font_size=10)
            plt.title("Simple Sampled Plot")
            plt.savefig("./plots/display_sampled_graph_" + str(tag) + ".png", format="PNG")
            plt.show()

    def display_communities_graph(self, graph, communities, populars, display=False, tag="visualization_graph"):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Display communities with different colors and highlight the most central node
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param communities: List of communities (nodes)
        :type communities: list of list 
        :param populars: List of popular nodes for each community ([[[score][name]], ...])
        :type populars: list of list 
        :param display: Display the plot
        :type display: bool
        :param tag: Part of the file name of the figure that will be saved
        :type tag: string
        """
        current_time = datetime.datetime.now()
        print("\n>> You have called the display of the community graph, (at", current_time, "), please wait.")

        # Create a dictionary mapping each node to its community
        node_to_community = {}
        community_colors = []
        for i, community in enumerate(communities):
            for node in community:
                node_to_community[node] = i
                community_colors.append("#" + "".join([random.choice("0123456789ABCDEF") for _ in range(6)]))

        # Draw the graph with each node colored according to its community
        pos = nx.spring_layout(graph)
        for node in graph.nodes():
            for p in populars:
                if node in p:
                    color = '#FFD700'
                    break
                else:
                    color = community_colors[node_to_community[node]]
            nx.draw_networkx_nodes(graph, pos, nodelist=[node], node_color=color)
        nx.draw_networkx_edges(graph, pos)
        nx.draw_networkx_labels(graph, pos)
        plt.title("Communities Graph Detection")
        plt.savefig("./plots/display_communities_graph_" + str(tag) + ".png", format="PNG")
        if display:
            plt.show()

        current_time = datetime.datetime.now()
        print("<< The display of the community graph has finished (at", current_time, ").\n")

    def degree_distribution(self, graph, display=False, tag="visualization_graph"):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Display the degree distribution of the graph
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param display: bool - display the plot
        :type display: bool
        :param tag: Part of the file name of the figure that will be saved
        :type tag: string
        """
        # Get access to the degree
        degrees = []
        for n, degree in graph.degree():
            degrees.append(degree)

        plt.hist(degrees)
        plt.xlabel('Degree')
        plt.ylabel('Number')

        # Display
        if display:
            plt.tight_layout()
            plt.title("Degree Distribution")
            plt.savefig("./plots/degree_distribution_" + str(tag) + ".png", format="PNG")
            plt.show()

    def save_communities(self, communities, limit=100000):
        """
        Creator : Quentin Nater
        reviewed by : Sophie Caroni
        Save on file all communities
        :param communities: List of all communities
        :type communities: list of list 
        :param limit: Number of nodes in the graph
        :type limit: int or string
        """
        my_export = ""
        for x, community in enumerate(communities):
            my_export = my_export + str(x) + ":" + str(community) + "\n"
        with open('./results/communities'+str(limit)+'.txt', 'w') as file:

            # Write the string variable to the file
            file.write(my_export)

    def retrieve_communities(self, txt_file):
        """
        Creator : Sophie Caroni
        reviewed by : Sophie Caroni
        Retrieve communities from a txt file
        :param txt_file: File containing all communities
        :type txt_file: String
        """
        communities = []
        # Open the input txt file for reading
        with open(txt_file, 'r') as file:

            # Loop through each line
            for line in file:

                # As soon as the line as '[', extract the community from the list and set it as community
                matches = re.findall(r"\{(.*?)\}", line)
                if len(matches) > 0:
                    for match in matches:
                        current_community = {asin for asin in match.split(", ")}
                        communities.append(current_community)

        return communities
