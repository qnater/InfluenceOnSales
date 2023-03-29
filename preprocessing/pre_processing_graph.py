import networkx as nx


class PreProcessGraph:

    # Creator : Quentin Nater
    # reviewed by :
    #
    # graph : networkX - Graph networkX of the amazon dataset
    #
    # Remove nodes that are isolated
    def refined_graph(graph):
        graph = PreProcessGraph.remove_isolated_nodes(graph)
        graph = PreProcessGraph.remove_not_incoming_edged_nodes(graph)
        graph = PreProcessGraph.remove_not_outgoing_edges_nodes(graph)

        print(">> Final pre-processing results : ",
              "\n\t\t\t\tNodes in the refined graph :\t\t", len(graph.nodes()),
              "\n\t\t\t\tEdges in the refined graph :\t\t", len(graph.edges()), "\n")

        return graph

    # Creator : Quentin Nater
    # reviewed by :
    #
    # graph : networkX - Graph networkX of the amazon dataset
    #
    # Remove nodes that are isolated
    def remove_isolated_nodes(graph):
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

    # Creator : Quentin Nater
    # reviewed by :
    #
    # graph : networkX - Graph networkX of the amazon dataset
    #
    # Remove nodes that are not in edged
    def remove_not_incoming_edged_nodes(graph):
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

    # Creator : Quentin Nater
    # reviewed by :
    #
    # graph : networkX - Graph networkX of the amazon dataset
    #
    # Remove nodes that are not out edged
    def remove_not_outgoing_edges_nodes(graph):
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