import networkx as nx
import numpy as np
from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

from analytics.analytics_graph import AnalyticsGraph
from visualization.visualization_graph import VisualizationGraph as vg


class PersistenceGraph:

    # MATCH(n) DETACH DELETE n
    #
    # LOAD CSV WITH HEADERS FROM "https://naterscreations.com/d/baby.csv"
    # AS row MERGE(from:Product {ASIN: row.ASIN})
    # MERGE(to: Product {ASIN: row.Similar})
    # MERGE(from)-[: SIMILAR_TO]->(to)
    #
    # MATCH p = () - [:SIMILAR_TO]->() RETURN p LIMIT 25;


    def __init__(self):
        uri = "neo4j+s://95147e5a.databases.neo4j.io:7687"
        user = "neo4j"
        password = "GslPkJDwnmAZC_COZUcHQ1hFymVSQTzS_f6loACAyNY"

        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def run(self, query, **kwargs):
        with self.driver.session(database="neo4j") as session:
            result = session.run(query, **kwargs)
            return result

    def close(self):
        self.driver.close()

    def old_populateDB(self, graph, delete_previous=True):
        """
        Creator : Quentin Nater & Sophie Caroni
        reviewed by :
        Populate the API Database NEO4J online
        :param graph: networkX - Graph networkX of the amazon dataset
        :type graph: networkX
        """

        print(">> You have called the creation of your graph in Neo4j, please wait :)")

        # Delete any previous graph currently existing on Neo4j
        if delete_previous:
            PersistenceGraph.delete_graph(self, verbose=False)

        # Keep track of the Neo4j node IDs for each node in the networkx graph
        node_ids = {}

        for (a, b) in graph.edges():
            # Check if node a already exists in Neo4j
            if a in node_ids:
                a_id = node_ids[a]
            else:
                # If not, create a new node in Neo4j and store its ID
                a_id = PersistenceGraph.create_node(self, a)
                node_ids[a] = a_id
            # Check if node b already exists in Neo4j
            if b in node_ids:
                b_id = node_ids[b]
            else:
                # If not, create a new node in Neo4j and store its ID
                b_id = PersistenceGraph.create_node(self, b)
                node_ids[b] = b_id

            # Create an edge between the nodes a and b in Neo4j
            PersistenceGraph.create_edge(self, a_id, b_id)

        print(">> The graph was successfully created, please enjoy ;)")

        # Close driver connection
        PersistenceGraph.close(self)

    def populateDB(self, graph, delete_previous=True, communities=None):
        """
        Creator : Quentin Nater & Sophie Caroni
        reviewed by :
        Populate the API Database NEO4J online
        :param graph: networkX - Graph networkX of the amazon dataset
        :type graph: networkX
        """

        print(">> You have called the creation of your graph in Neo4j, please wait :)")

        # Delete any previous graph currently existing on Neo4j
        if delete_previous:
            PersistenceGraph.delete_graph(self, verbose=False)

        # Keep track of the Neo4j node IDs for each node in the networkx graph
        node_ids = {}

        for (a, b) in graph.edges():
            # Check if node a already exists in Neo4j
            if a in node_ids:
                a_id = node_ids[a]
            else:
                # If not, create a new node in Neo4j and store its ID
                a_id = PersistenceGraph.create_node(self, a)
                node_ids[a] = a_id
            # Check if node b already exists in Neo4j
            if b in node_ids:
                b_id = node_ids[b]
            else:
                # If not, create a new node in Neo4j and store its ID
                b_id = PersistenceGraph.create_node(self, b)
                node_ids[b] = b_id

            # Create an edge between the nodes a and b in Neo4j
            PersistenceGraph.create_edge(self, a_id, b_id)

        if not communities:
            #  Retrieve communities if not already passed as argument
            communities = vg.retrieveCommunities("./results/communities100000.txt")

        for idx, community in enumerate(communities):
            for node in community:
                node = node.replace("'", "")
                with self.driver.session() as session:
                    query = f"""
                                MATCH (n:Node {{id: '{node}'}})
                                SET n.community = '{idx}'
                                RETURN n
                            """
                    result = session.run(query)

        print(">> The graph was successfully created, please enjoy ;)")

        # Close driver connection
        PersistenceGraph.close(self)


    def create_edge(self, depart, destination, tag="similar_to"):
        """
        Creator : Sophie Caroni
        reviewed by :
        Creates an edge between two nodes in the API Database NEO4J online
        :param
        :type
        """

        query = f"""
                MATCH (n1:Node),(n2:Node)
                WHERE n1.id = '{depart}' AND n2.id = '{destination}'
                CREATE (n1)-[r:{tag}]->(n2)
                RETURN n1.id AS p1, n2.id AS p2
                """
        with self.driver.session() as session:
            session.run(query)

        return

    def create_hyperedge(self, depart, destination):
        """
        Creator : Sophie Caroni
        reviewed by :
        Creates an edge between two nodes in the API Database NEO4J online
        :param
        :type
        """

        query = f"""
                MATCH (n1:Hypernode),(n2:Hypernode)
                WHERE n1.id = '{depart}' AND n2.id = '{destination}'
                CREATE (n1)-[r:hypernode_link]->(n2)
                RETURN n1.id AS p1, n2.id AS p2
                """
        with self.driver.session() as session:
            session.run(query)

        return


    def create_node(self, node_id):
        """
        Creator : Quentin Nater
        reviewed by :
        Creates a node in the API Database NEO4J online
        :param node_id: ID of the new node to create
        :type node_id: str
        """

        query = f"CREATE (:Node {{id: '{node_id}'}})"
        with self.driver.session() as session:
            session.run(query)

        return node_id

    def create_hypernode(self, hypernode_id):
        """
        Creator : Quentin Nater
        reviewed by :
        Creates a node in the API Database NEO4J online
        :param node_id: ID of the new node to create
        :type node_id: str
        """

        query = f"CREATE (:Hypernode {{id: '{hypernode_id}'}})"
        with self.driver.session() as session:
            session.run(query)

        return hypernode_id



    def delete_graph(self, verbose=True):
        """
        Creator : Sophie Caroni
        reviewed by :
        Deletes the graph currently existing in the API Database NEO4J online
        """

        if verbose:
            print(">> You have called the deletion of any currently existing graph in Neo4j, please wait :)")

        query = f"MATCH (n) DETACH DELETE n"
        with self.driver.session() as session:
            session.run(query)

        if verbose:
            print(">> The graph was successfully deleted from Neo4j.")

        return

    def match_node(self, node_id):
        """
        Creator : Quentin Nater
        reviewed by :
        Creates a node in the API Database NEO4J online
        :param node_id: ID of the new node to create
        :type node_id: str
        """

        query = f"""
                MATCH (n:Node {{id: '{node_id}'}}) 
                RETURN n
                """

        with self.driver.session() as session:
            result = session.run(query)
            for record in result:
                print(record)

        return node_id

    def display_communities(self, communities=None):
        """
        Creator : Sophie Caroni
        reviewed by :
        :param communities:
        :type communities: List of tuples.
        Deletes the graph currently existing in the API Database Neo4j online
        """
        print(">> You have asked the display of communities in the DB.")

        if not communities:
            # Retrieve communities if not already passed as argument
            communities = vg.retrieveCommunities("./results/communities100000.txt")
            print(communities)

        # Convert the sets into lists, to make them suitable for Cypher
        communities = [list(community) for community in communities]

        # No errors but no color
        with self.driver.session() as session:
            for i, community in enumerate(communities):
                query = f"MATCH (n) WHERE n.name IN {community} SET n:community_{i} RETURN count(n)"
                session.run(query)

        return

    def display_community(self, community_id, communities=None): # not sure about the parameters
        """
        Creator : Sophie Caroni
        reviewed by :
        :param community_id:
        :type communities: Int
        Display a selected community.
        """
        print(f">> You have called the display of the community {community_id} in the DB.")

        # Retrieve communities if not already passed as argument
        if not communities:
            communities = vg.retrieveCommunities("./results/communities100000.txt")

        # Convert the sets into lists, to make them suitable for Cypher
        communities = [list(community) for community in communities]

        # Pick the community to display
        community = communities[community_id]

        # Display community members
        for idx, node in enumerate(community):
            if idx == 0:
                node = node.replace("'", "") # see if still needed
                PersistenceGraph.match_node(self, node)

        # Close driver connection
        PersistenceGraph.close(self)

        return


    def display_hypernodes_communities(self, graph, communities=None, delete_previous=False): # not sure about the parameters
        """
        Creator : Sophie Caroni
        reviewed by :
        :param graph: networkX - Graph networkX of the amazon dataset
        :type graph: networkX
        :param community_id:
        :type communities: Int
        Display a selected community.
        """
        print(">> You have called the display of hypernode communities in the DB.")

        # Delete any previous graph currently existing on Neo4j
        if delete_previous:
            PersistenceGraph.delete_graph(self, verbose=False)

        # Retrieve communities if not already passed as argument
        if not communities:
            communities = vg.retrieveCommunities("./results/communities100000.txt")
            # communities = AnalyticsGraph.amazon_community_detection(graph, "test")

        # Convert the sets into lists, to make them suitable for Cypher
        communities = [list(community) for community in communities]

        hypernodes = []
        # Create and display community as hypernodes
        for idx, community in enumerate(communities):

            # Name each hypernode them by their index and the number of nodes contained in the community
            hypernode_id = str(idx) # + f" ({len(community)})"
            PersistenceGraph.create_hypernode(self, hypernode_id)

            all_neighbors = []
            # Retrieve neighbors of the hypernode
            for node in community:
                neighbors = nx.neighbors(graph, node)
                for node in neighbors:
                    all_neighbors.append(node)
            hypernodes.append((idx, np.unique(all_neighbors)))
        print(hypernodes)

        final_hypernodes = []
        for (idx, neighbors) in hypernodes:
            final_neighbors, current_communities = [], -1
            for node in neighbors:
                for i, com in enumerate(communities):
                    if node in com:
                        current_communities = i
                final_neighbors.append(current_communities)
            final_hypernodes.append((idx, np.unique(final_neighbors)))

        for (idx, neighbors) in final_hypernodes:
            for n in neighbors:
                if n != idx:
                    PersistenceGraph.create_hyperedge(self, idx, n)

        # Close driver connection
        PersistenceGraph.close(self)