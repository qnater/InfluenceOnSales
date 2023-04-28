import random

import matplotlib.pyplot as plt
import networkx as nx


class VisualizationGraph:

    def display_simple_graph(graph, display=True, tag="visualization_graph"):
        """
        Creator : Quentin Nater
        reviewed by :
        Display a simple graph
        :param graph: networkX - graph of the dataset
        :type graph: networkX
        :param display: bool - display the plot
        :type display: bool
        :return: the display of the graph
        """
        if display:
            nx.draw(graph, with_labels=True, node_color="lightblue", node_size=400, font_size=10)
            plt.title("Simple Display Plot")
            plt.savefig("./plots/display_simple_graph" + str(tag) + ".png", format="PNG")
            plt.show()

        return graph


    def display_sampled_graph(myGraph, display=True, tag="visualization_graph"):
        """
        Creator : Quentin Nater
        reviewed by :
        Display a sample of a graph
        :param graph: networkX - graph of the dataset
        :type graph: networkX
        :param display: bool - display the plot
        :type display: bool
        :param tag: String - special information for the saved plot
        :type tag: String
        """
        # number of nodes to sample
        num_nodes = 1000

        # randomly sample nodes
        nodes_list = list(myGraph.nodes())
        sampled_nodes = random.sample(nodes_list, num_nodes)

        # create a subgraph with the sampled nodes and all their edges
        sampled_graph = myGraph.subgraph(sampled_nodes)

        if display:
            # draw the sampled graph
            nx.draw(sampled_graph, with_labels=True, node_color="lightblue", node_size=400, font_size=10)
            plt.title("Simple Sampled Plot")
            plt.savefig("./plots/display_sampled_graph_" + str(tag) + ".png", format="PNG")
            plt.show()


    def display_communities_graph(graph, communities, populars, display=False, tag="visualization_graph"):
        """
        Creator : Quentin Nater
        reviewed by :
        Display communities in the graph with different color and highlight the more central one
        :param graph: networkX - graph of the dataset
        :type graph: networkX
        :param communities: String [[]] - List of community (list of nodes)
        :type communities: String [[]]
        :param populars: String [[]] - List of popular nodes for each community ([[[score][name]], ...])
        :type populars: String [[]]
        :param display: bool - display the plot
        :type display: bool
        :param tag: String - special information for the saved plot
        :type tag: String
        """
        # Create a dictionary mapping each node to its community
        node_to_community = {}
        community_colors = []
        for i, community in enumerate(communities):
            for node in community:
                node_to_community[node] = i
                community_colors.append("#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)]))

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
        plt.show()



    def degree_distribution(graph, display=False, tag="visualization_graph"):
        """
        Creator : Quentin Nater
        reviewed by :
        Display the degree distribution of the graph
        :param graph: networkX - graph of the dataset
        :type graph: networkX
        :param display: bool - display the plot
        :type display: bool
        :param tag: String - special information for the saved plot
        :type tag: String
        """
        # get access to the degree
        degrees = []
        for n, degree in graph.degree():
            degrees.append(degree)

        plt.hist(degrees)

        plt.xlabel('Degree')
        plt.ylabel('Number')

        # display
        if display:
            plt.tight_layout()
            plt.title("Degree Distribution")
            plt.savefig("./plots/degree_distribution_" + str(tag) + ".png", format="PNG")
            plt.show()

    def saveCommunities(communities):
        """
        Creator : Quentin Nater
        reviewed by :
        Save on file all communities
        :param communities: String [[]] - list of all communities
        :type communities: String [[]]
        """
        myExport = ""
        for x, community in enumerate(communities):
            myExport = myExport + str(x) + ":" + str(community) + "\n"
        with open('./results/communities.txt', 'w') as file:
            # Write the string variable to the file
            file.write(myExport)

