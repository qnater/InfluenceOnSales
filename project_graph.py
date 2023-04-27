import os

import pandas as pd
import matplotlib as mpl
import networkx as nx
import spicy as sp
from matplotlib import pyplot as plt

from explore.exploration_graph import ExploreGraph as eg
from visualization.visualization_graph import VisualizationGraph as vg
from analytics.analytics_graph import AnalyticsGraph as ag
from preprocessing.pre_processing_graph import PreProcessGraph as pg
from export.export_graph import ExportGraph as xg

# QUENTIN NATER - 01.03.2023
if __name__ == '__main__':
    print("\n=========================================================================================")
    print("========================INFLUENCE=OF=POPULARITY=ON=SALES===UNI-FR========================")
    print("=========================================================================================\n")



    if os.name == "nt":
        mpl.use('TkAgg')  # without it, cannot run my plots (maybe personal)
    elif os.name == "posix":
        print("Sorry bro about your MAC...")
    else:
        print("Unknown operating system.")

    tag = "analyse"  # prod or test

    if tag == "test":
        graph = eg.construct_graph_by_file("./dataset/amazon_refined.txt")
        ag.community_library_detection()

    elif tag == "analyse":
        graph = eg.construct_graph_by_file("./dataset/amazon_refined.txt")
        vg.display_simple_graph(graph, False)
        pg.remove_nodes_by_degree(graph, 4)
        ag.community_library_detection(graph, "louvain")
        #ag.centrality_betweenness_library(graph)

    elif tag == "staging":
        graph = eg.construct_graph_by_file("./dataset/amazon-meta.txt")
        graph = pg.refined_graph(graph)
        xg.create_dataset(graph)

    elif tag == "prod":
        graph = nx.Graph()
        graph.add_nodes_from(["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"])
        graph.add_edges_from([("0", "2"),("0", "4"),("0", "3"),("0", "5"),
                              ("1", "2"),("1", "4"),("1", "7"),
                              ("2", "4"), ("2", "5"), ("2", "6"),
                              ("3", "7"),
                              ("4", "10"),
                              ("4", "10"),
                              ("5", "7"),("5", "11"),
                              ("6", "7"),("6", "11"),
                              ("8", "11"), ("8", "9"),("8", "14"),("8", "15"),("8", "10"),
                              ("9", "12"), ("9", "14"),
                              ("10", "14"), ("10", "12"), ("10", "11"), ("10", "13"),
                              ("11", "13")])

        #graph = eg.construct_graph_by_file("./dataset/amazon_refined.txt")
        vg.display_simple_graph(graph, False)
        #pg.remove_nodes_by_degree(graph, 4)
        ag.homemade_community_detection(graph)

    elif tag == "explore":
        import networkx as nx
        import matplotlib.pyplot as plt
        G = nx.Graph()
        G.add_nodes_from(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"])
        G.add_edges_from([("0", "2"), ("0", "4"), ("0", "3"), ("0", "5"),
                              ("1", "2"), ("1", "4"), ("1", "7"),
                              ("2", "4"), ("2", "5"), ("2", "6"),
                              ("3", "7"),
                              ("4", "10"),
                              ("5", "7"), ("5", "11"),
                              ("6", "7"), ("6", "11"),
                              ("8", "11"), ("8", "9"), ("8", "14"), ("8", "15"), ("8", "10"),
                              ("9", "12"), ("9", "14"),
                              ("10", "14"), ("10", "12"), ("10", "11"), ("10", "13"),
                              ("11", "13")])





        # Create an empty graph
        #G = nx.Graph()

        # Open the file and read the lines
        #with open(
        #        "/Users/Emmanuel/Desktop/UNIFR/Social Media Analytics/Project/InfluenceOnSales/dataset/amazon_refined2.txt",
        #        "r") as f:
        #    lines = f.readlines()

        # Parse the lines to extract nodes and edges
        #for line in lines:
        #    if line.startswith("ASIN:"):
        #        node = line.strip().split(":")[1].strip()
        #    elif line.startswith("  similar:"):
        #        edges = line.strip().split(":")[1].strip().split()
        #        for edge in edges:
        #            G.add_edge(node, edge)



        # Remove nodes with degree 3
        #nodes_with_degree_3 = [node for node, degree in G.degree() if degree == 3]
        #G.remove_nodes_from(nodes_with_degree_3)

        # Get the number of nodes and edges in the graph
        print("Number of nodes:", G.number_of_nodes())
        print("Number of edges:", G.number_of_edges())

        # Get the degree distribution of the nodes in the graph
        degree_sequence = [d for n, d in G.degree()]
        degree_counts = dict(
            zip(sorted(set(degree_sequence)), [degree_sequence.count(d) for d in sorted(set(degree_sequence))]))
        print("Degree distribution:", degree_counts)

        # Get the connected components of the graph
        connected_components = nx.connected_components(G)

        # Compute the diameter for each connected component
        diameters = [nx.diameter(G.subgraph(component)) for component in connected_components]

        # Print the diameters
        print("Diameters of connected components:", diameters)

        # Get the clustering coefficient of the nodes in the graph (a measure of the density of triangles in the graph)
        print("Clustering coefficient:", nx.average_clustering(G))

        # Get the betweenness centrality of the nodes in the graph (a measure of the importance of a node in connecting different parts of the graph)
        bc_scores = nx.betweenness_centrality(G)
        print("Betweenness centrality:")
        for node, score in bc_scores.items():
            print(f"{node}: {score}")

        # Degree centrality measure
        dc_scores = nx.degree_centrality(G)
        print("Degree centrality:")
        for node, score in dc_scores.items():
            print(f"{node}: {score}")

        # Eigenvector centrality measure
        ec_scores = nx.eigenvector_centrality(G)
        print("Eigenvector centrality:")
        for node, score in ec_scores.items():
            print(f"{node}: {score}")

        # PageRank centrality measure
        pr_scores = nx.pagerank(G)
        print("PageRank:")
        for node, score in pr_scores.items():
            print(f"{node}: {score}")

        # Closeness centrality measure
        cc_scores = nx.closeness_centrality(G)
        print("Closeness centrality:")
        for node, score in cc_scores.items():
            print(f"{node}: {score}")

        # Adamic-Adar score
        aa_scores = nx.adamic_adar_index(G)
        print("Adamic-Adar score:")
        for u, v, p in aa_scores:
            print(f"({u}, {v}): {p}")

        # Betweenness centrality measure
        bc_scores = nx.betweenness_centrality(G)
        print("Betweenness centrality:")
        for node, score in bc_scores.items():
            print(f"{node}: {score}")

        # Jaccard similarity measure
        js_scores = nx.jaccard_coefficient(G)
        print("Jaccard similarity:")
        for u, v, p in js_scores:
            print(f"({u}, {v}): {p}")

        # Visualize the graph
        plt.figure(figsize=(10, 10))
        nx.draw(G, node_size=10, edge_color='grey', alpha=0.5)
        plt.show()

        # Complete exploration thru a Depth-First-Search
        def dfs(G, node, visited):
            if node not in visited:
                visited.append(node)
                if node in G:
                    for neighbor in G[node]:
                        dfs(G, neighbor, visited)
            return visited


        visited = []
        start_node = '5'
        path = dfs(G, start_node, visited)

        print("Visited nodes:", len(path))
        print("Path:", " -> ".join(path))


        def create_networkx_graph(graph):
            G = nx.DiGraph()
            for node in graph:
                G.add_node(node)
                for neighbor in graph[node]:
                    G.add_edge(node, neighbor)
            return G


        def draw_graph(G, path=None):
            pos = nx.spring_layout(G, seed=42)
            nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=2000, font_size=10)
            if path:
                edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
                nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='r', width=2)
            plt.show()


        visited = []
        start_node = '5'
        path = dfs(G, start_node, visited)

        G = create_networkx_graph(G)
        draw_graph(G, path)
        import heapq


        def heuristic(node, goal):
            return 0


        def a_star_search(graph, start, goal):
            frontier = [(0, start, [])]  # (priority, node, path)
            explored = set()

            while frontier:
                cost, current, path = heapq.heappop(frontier)
                if current == goal:
                    return path + [current]

                if current not in explored:
                    explored.add(current)
                    if current in graph:
                        for neighbor in graph[current]:
                            new_cost = cost + 1 + heuristic(neighbor, goal)
                            heapq.heappush(frontier, (new_cost, neighbor, path + [current]))

            return None


        start_node = '8'
        goal_node = '3'
        path = a_star_search(G, start_node, goal_node)

        if path:
            print("Path found:", " -> ".join(path))
            G = create_networkx_graph(G)
            draw_graph(G, path)
        else:
            print("Path not found")


        def dfs_iterative(G, start_node):
            visited = set()
            stack = [start_node]

            while stack:
                node = stack.pop()
                if node not in visited:
                    visited.add(node)
                    print(node)
                    if node in G:
                        for neighbor in G[node]:
                            stack.append(neighbor)
            return visited


        start_node = '3'
        visited_nodes = dfs_iterative(G, start_node)

        path = list(visited_nodes)  # Convert the set of visited nodes to a list
        G = create_networkx_graph(G)
        draw_graph(G, path)
