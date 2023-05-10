from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

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

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def run(self, query, **kwargs):
        with self.driver.session(database="neo4j") as session:
            result = session.run(query, **kwargs)
            return result

    def close(self):
        self.driver.close()

    def populateDB(self, graph, delete_previous=True):
        """
        Creator : Quentin Nater & Sophie Caroni
        reviewed by :
        Populate the API Database NEO4J online
        :param graph: networkX - Graph networkX of the amazon dataset
        :type graph: networkX
        """

        print(">> You have called the creation of your graph in Neo4j, please wait :)")

        # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
        uri = "neo4j+s://0d2d7b8e.databases.neo4j.io:7687"
        user = "neo4j"
        password = "bta9fHGXHYBwD1fIKnLpJwwFUiZZxwtV5zouYfcgCwA"
        app = PersistenceGraph(uri, user, password)

        # Delete any previous graph currently existing on Neo4j
        if delete_previous:
            app.delete_graph(verbose=False)

        # Keep track of the Neo4j node IDs for each node in the networkx graph
        node_ids = {}

        for (a, b) in graph.edges():
            # Check if node a already exists in Neo4j
            if a in node_ids:
                a_id = node_ids[a]
            else:
                # If not, create a new node in Neo4j and store its ID
                a_id = app.create_node(a)
                node_ids[a] = a_id
            # Check if node b already exists in Neo4j
            if b in node_ids:
                b_id = node_ids[b]
            else:
                # If not, create a new node in Neo4j and store its ID
                b_id = app.create_node(b)
                node_ids[b] = b_id

            # Create an edge between the nodes a and b in Neo4j
            app.create_edge(a_id, b_id)

        print(">> The graph was successfully created, please enjoy ;)")

        # Close driver connection
        app.close()


    def create_edge(self, depart, destination):
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
                CREATE (n1)-[r:similar_to]->(n2)
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


    def display_communities(self, communities=None):
        """
        Creator : Sophie Caroni
        reviewed by :
        :param communities:
        :type communities: List of tuples.
        Deletes the graph currently existing in the API Database Neo4j online
        """

        if not communities:
            # Compute communities using Louvain algorithm
            communities = vg.retrieveCommunities("./results/communities100000.txt")
            print(communities)

        # Convert the sets into lists, to make them suitable for Cypher
        communities = [list(community) for community in communities]

        # No errors but no colors
        # query = """
        #         UNWIND $communities AS community
        #         MATCH (n)
        #         WHERE id(n) IN community
        #         SET n.community = community
        #     """
        #
        # with self.driver.session() as session:
        #     session.run(query, communities=communities)

        # Errors
        # # Construct Cypher query to color nodes by community
        # query = "MATCH (n) "
        # for i, community in enumerate(communities):
        #     # Generate a unique label for the community
        #     label = f"community_{i}"
        #     # Add a SET clause to color nodes in the community with the label
        #     query += f"FOREACH (node IN [{','.join(str(n) for n in community)}] | SET node:{label}) "
        # # Return the number of nodes colored by community
        # query += "RETURN count(DISTINCT n)"
        #
        # with self.driver.session() as session:
        #     session.run(query)

        # No errors but no color
        with self.driver.session() as session:
            for i, community in enumerate(communities):
                query = f"MATCH (n) WHERE n.name IN {community} SET n:community_{i} RETURN count(n)"
                session.run(query)

        return

    def display_community(self, community_id, communities=None, delete_previous=True): # not sure about the parameters
        """
        Creator : Sophie Caroni
        reviewed by :
        :param community_id:
        :type communities: Int
        Display a selected community.
        """

        ## needed to be able to call create_node, right?
        # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
        uri = "neo4j+s://0d2d7b8e.databases.neo4j.io:7687"
        user = "neo4j"
        password = "bta9fHGXHYBwD1fIKnLpJwwFUiZZxwtV5zouYfcgCwA"
        app = PersistenceGraph(uri, user, password)

        # Delete any previous graph currently existing on Neo4j
        if delete_previous:
            app.delete_graph(verbose=False)

        # # Compute communities using Louvain algorithm if not already passed as argument
        if not communities:
            communities = vg.retrieveCommunities("./results/communities100000.txt")

        # Convert the sets into lists, to make them suitable for Cypher
        communities = [list(community) for community in communities]

        # Pick the community to display
        community = communities[community_id]

        # Display community members
        for node in community:
            node = node.replace("'", "") # see if still needed
            app.create_node(node)

        # Close driver connection
        app.close()

        return


    def display_hypernodes_communities(self, communities=None, delete_previous=True): # not sure about the parameters
        """
        Creator : Sophie Caroni
        reviewed by :
        :param community_id:
        :type communities: Int
        Display a selected community.
        """

        ## needed to be able to call create_node, right?
        # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
        uri = "neo4j+s://0d2d7b8e.databases.neo4j.io:7687"
        user = "neo4j"
        password = "bta9fHGXHYBwD1fIKnLpJwwFUiZZxwtV5zouYfcgCwA"
        app = PersistenceGraph(uri, user, password)

        # Delete any previous graph currently existing on Neo4j
        if delete_previous:
            app.delete_graph(verbose=False)

        # Compute communities using Louvain algorithm if not already passed as argument
        if not communities:
            communities = vg.retrieveCommunities("./results/communities100000.txt")

        # Convert the sets into lists, to make them suitable for Cypher
        communities = [list(community) for community in communities]

        # Create and display community as hypernodes (naming them by their index)
        # hypernodes = []
        # for idx, community in enumerate(communities):
        #     for node in community
        #         node = node.replace("'", "") # see if still needed
        #     hypernodes.append(i)
        #     app.create_node([hypernode] for hypernode in hypernodes)
        #
        # # Close driver connection
        # app.close()
        #
        # return

    # Create and display community as hypernodes (naming them by their index and the number of nodes contained)
        for idx, community in enumerate(communities):
            # hypernode_name =
            app.create_node(idx)

            # # Add each node in the community as a child node of the hypernode
            # for node in community:
            #     node = node.replace("'", "")
            #     app.create_node(node)
            #     app.create_relationship("PART_OF", [node], [f"Community {idx}"])

        # Close driver connection
        app.close()


###### TO REVIEW
    # def create_relationship(self, source_name, target_name, label):
    #     with self._driver.session() as session:
    #         session.write_transaction(self._create_relationship, source_name, target_name, label)
    #
