import datetime

import networkx as nx
import numpy as np
from neo4j import GraphDatabase

from analytics.analytics_graph import AnalyticsGraph
from visualization.visualization_graph import VisualizationGraph as vg


class PersistenceGraph:

    def __init__(self):
        # Credential for the database
        uri = "neo4j+s://95147e5a.databases.neo4j.io:7687"
        user = "neo4j"
        password = "GslPkJDwnmAZC_COZUcHQ1hFymVSQTzS_f6loACAyNY"

        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def run(self, query, **kwargs):
        """
        Creator : Sophie Caroni
        reviewed by : Quentin Nater
        Run the driver to the database
        :param query: Query to upload to the server
        :type query: String
        :param kwargs: List of other arguments
        :type kwargs: arguments
        :return result: Code of the result
        """
        with self.driver.session(database="neo4j") as session:
            result = session.run(query, **kwargs)
            return result

    def close(self):
        """
        Creator : Sophie Caroni
        reviewed by : Quentin Nater
        Close the connection to the databaset
        """
        self.driver.close()

    def populate_database(self, graph, delete_previous, communities=None, compute_community=False):
        """
        Creator : Sophie Caroni
        reviewed by : Quentin Nater
        Populate the API Database NEO4J online
        :param graph: networkX - Graph networkX of the amazon dataset
        :type graph: networkX
        :param delete_previous: tells if what is currently in Neo4j needs to be deleted; has to be False if none is in Neo4j
        :type graph: bool
        :param communities: Communities of nodes of the graph
        :type communities: set of lists
        :param compute_community: create a new community list from the homemade algorithm
        :type compute_community: bool
        :return : Communities of the computed nodes
        """
        current_time = datetime.datetime.now()
        print("\n>> You have called the creation of your graph in Neo4j, (at", current_time, "), please wait...")

        # Delete any previous graph currently existing on Neo4j
        if delete_previous:
            PersistenceGraph.delete_graph(self, verbose=False)

        # Keep track of the Neo4j node IDs for each node in the networkx graph
        node_ids = {}

        for (a, b) in graph.edges():
            # Check if node an already exists in Neo4j
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

        # create the community list if needed
        communities = PersistenceGraph.call_communities(self, graph=graph, compute_community=compute_community, communities=communities)

        for idx, community in enumerate(communities):
            for node in community:
                if isinstance(node, str):
                    node = node.replace("'", "")
                with self.driver.session() as session:
                    query = f"""
                                MATCH (n:Node {{id: '{node}'}})
                                SET n.community = '{idx}'
                                RETURN n
                            """
                    result = session.run(query)

        current_time = datetime.datetime.now()
        print(">> The graph was successfully created, (at", current_time, "), enjoy.\n")

        # Close driver connection
        PersistenceGraph.close(self)

        return communities

    def display_hypernodes_communities(self, graph, communities=None, compute_community=False, delete_previous=False):  # not sure about the parameters
        """
        Creator : Sophie Caroni
        reviewed by :
        Display a selected community.
        :param graph: networkX - Graph networkX of the amazon dataset
        :type graph: networkX
        :param communities: Communities of nodes of the graph
        :type communities: set of lists
        :param compute_community: Compute or not the community detection
        :type compute_community: bool
        :param delete_previous: Delete or not the graph currently existing in the database
        :type delete_previous: bool
        """

        current_time = datetime.datetime.now()
        print(">> You have called the creation of hypernodes graph in Neo4j, (at", current_time, "), please wait...")

        # Delete any previous graph currently existing on Neo4j
        if delete_previous:
            PersistenceGraph.delete_graph(self, verbose=False)

        # create the community list if needed
        communities = PersistenceGraph.call_communities(self, graph=graph, compute_community=compute_community, communities=communities)

        # Convert the sets into lists, to make them suitable for Cypher
        communities = [list(community) for community in communities]

        hypernodes = []
        # Create and display community as hypernodes
        for idx, community in enumerate(communities):

            # Name each hypernode them by their index and the number of nodes contained in the community
            hypernode_id = str(idx)
            PersistenceGraph.create_hypernode(self, hypernode_id)

            all_neighbors = []
            # Retrieve neighbors of the hypernode
            for node in community:
                neighbors = nx.neighbors(graph, node)
                for node in neighbors:
                    all_neighbors.append(node)
            hypernodes.append((idx, np.unique(all_neighbors)))
        print("\t\t\t\t (DB) Hypernodes: ", hypernodes)

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

        current_time = datetime.datetime.now()
        print(">> The hypernodes were successfully created, (at", current_time, "), enjoy.")

        return

    def create_edge(self, start, destination, tag="similar_to"):
        """
        Creator : Sophie Caroni
        reviewed by : Quentin Nater
        Creates an edge between two nodes in the API Database NEO4J online
        :param start: Starting node id
        :type start: str
        :param destination: Destination node id
        :type destination: str
        :param tag: Type of relationship to display
        :type tag: str
        """

        query = f"""
                MATCH (n1:Node),(n2:Node)
                WHERE n1.id = '{start}' AND n2.id = '{destination}'
                CREATE (n1)-[r:{tag}]->(n2)
                RETURN n1.id AS p1, n2.id AS p2
                """
        with self.driver.session() as session:
            session.run(query)

        return

    def create_hyperedge(self, start, destination):
        """
        Creator : Sophie Caroni
        reviewed by : Quentin Nater
        Creates an edge between two nodes in the API Database NEO4J online
        :param start: Starting node ID
        :type start: str
        :param destination: Destination node ID
        :type destination: str
        """

        query = f"""
                MATCH (n1:Hypernode),(n2:Hypernode)
                WHERE n1.id = '{start}' AND n2.id = '{destination}'
                CREATE (n1)-[r:hypernode_link]->(n2)
                RETURN n1.id AS p1, n2.id AS p2
                """

        with self.driver.session() as session:
            session.run(query)

        return

    def create_node(self, node_id):
        """
        Creator : Sophie Caroni
        reviewed by : Quentin Nater
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
        Creator : Sophie Caroni
        reviewed by : Quentin Nater
        Creates a hypernode in the API Database NEO4J online
        :param hypernode_id: ID of the new hypernode to create
        :type hypernode_id: str
        """

        query = f"CREATE (:Hypernode {{id: '{hypernode_id}'}})"
        with self.driver.session() as session:
            session.run(query)

        return hypernode_id

    def delete_graph(self, verbose=True, nodes_to_delete="all_nodes"):
        """
        Creator : Sophie Caroni
        reviewed by : Quentin Nater
        Deletes the graph currently existing in the API Database NEO4J online
        :param verbose: Starting and finishing sentences
        :type verbose: bool
        :param nodes_to_delete: How many nodes to delete from the graph
        :type nodes_to_delete: str
        """

        if verbose:
            print(">> You have called the deletion of any currently existing graph in Neo4j, please wait...")

        current_nodes = PersistenceGraph.get_node_number(self)

        if nodes_to_delete == "all_nodes":
            nodes_to_delete = current_nodes
        else:
            nodes_to_delete = int(nodes_to_delete)

        interval = nodes_to_delete // 10
        deleted_nodes = 0

        while deleted_nodes < nodes_to_delete:
            query = f"""
                    MATCH (n)
                    WITH n LIMIT {interval}
                    DETACH DELETE n
                    """

            with self.driver.session() as session:
                session.run(query)

            if nodes_to_delete > 10:
                deleted_nodes = current_nodes - PersistenceGraph.get_node_number(self)

        if verbose:
            print(">> The graph was successfully deleted from Neo4j.")

        return

    def get_node_number(self):
        """
         Creator : Sophie Caroni
         reviewed by : Quentin Nater
         Retrieves how many nodes has the graph currently existing in the API Database NEO4J online
         :return: number of nodes as integer
         """

        query = f"""
                MATCH (n)
                RETURN count(n) AS nodeCount
                """

        with self.driver.session() as session:
            result = session.run(query)
            record = result.single()
            number_of_nodes = record["nodeCount"]

        return number_of_nodes

    def match_node(self, node_id):
        """
        Creator : Sophie Caroni
        reviewed by : Quentin Nater
        Return the match node with its ID in the API Database NEO4J online
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
                print("\t\t\t\t (DB) record : ", record)

        print("\t\t\t\t (DB) query successful")

        return node_id

    def display_community(self, community_id, communities=None):
        """
        Creator : Sophie Caroni
        reviewed by : Quentin Nater
        Display nothing on the board of the API but return the value in the result format
        :param community_id: ID of the community to display
        :type community_id: int
        :param communities: Communities of nodes of the graph
        :type communities: set of lists
        Display a selected community.
        """
        print(f">> You have called the display of the community {community_id} in the DB.")

        # create the community list if needed
        communities = PersistenceGraph.call_communities(self, graph=None, compute_community=False, communities=communities)

        # Convert the sets into lists, to make them suitable for Cypher
        communities = [list(community) for community in communities]

        # Pick the community to display
        community = communities[community_id]

        # Display community members
        for idx, node in enumerate(community):
            if idx == 0:
                if isinstance(node, str):
                    node = node.replace("'", "")
                PersistenceGraph.match_node(self, node)

        # Close driver connection
        PersistenceGraph.close(self)

        return

    def call_communities(self, graph, compute_community, communities):
        """
        Creator : Sophie Caroni
        reviewed by : Quentin Nater
        Call the communities as needed in the storage, made them in the amazon community detection or take the one given by the user
        :param graph: networkX - Graph networkX of the amazon dataset
        :type graph: networkX
        :param communities: Communities of nodes of the graph
        :type communities: set of lists
        :param compute_community: create a new community list from the homemade algorithm
        :type compute_community: bool
        """
        if compute_community:
            communities, run_time = AnalyticsGraph.amazon_community_detection(self, graph=graph, tag="db", run_silhouette=False, display=False, sub_function=True)
        else:
            if not communities:
                #  Retrieve communities if not already passed as argument
                communities = vg.retrieve_communities(self, "./results/default_communities.txt")

        return communities