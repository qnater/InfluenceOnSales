from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable


class PersistenceGraph:

    # MATCH(n) DETACH DELETE n
    #
    # LOAD CSV WITH HEADERS FROM "https://naterscreations.com/d/baby.csv"
    # AS row MERGE(from:Product {ASIN: row.ASIN})
    # MERGE(to: Product {ASIN: row.Similar})
    # MERGE(from)-[: SIMILAR_TO]->(to)
    #
    # MATCH p = () - [:SIMILAR_TO]->() RETURN p LIMIT 25;

    def populateDB(self, graph):
        """
        Creator : Quentin Nater
        reviewed by :
        Populate the API Database NEO4J online
        :param graph: networkX - Graph networkX of the amazon dataset
        :type graph: networkX
        """

        # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
        uri = "neo4j+s://0d2d7b8e.databases.neo4j.io:7687"
        user = "neo4j"
        password = "bta9fHGXHYBwD1fIKnLpJwwFUiZZxwtV5zouYfcgCwA"
        app = PersistenceGraph(uri, user, password)

        for (a, b) in graph.edges():
            app.create_edge(a, b)

        app.close()

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def create_edge(self, depart, destination):
        """
        Creator : Quentin Nater
        reviewed by :
        Populate the API Database NEO4J online
        :param graph: networkX - Graph networkX of the amazon dataset
        :type graph: networkX
        :param depart: String - Node of depart of the relationship
        :type depart: String
        :param destination: String - Node of destination of the relationship
        :type destination: String
        """

        with self.driver.session(database="neo4j") as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.execute_write(self._create_and_return_friendship, depart, destination)
            for row in result:
                print("\t\t\t(NEO4J) : Created edge between: {p1}, {p2}".format(p1=row['p1'], p2=row['p2']))

    @staticmethod
    def _deleteDB(tx):
        """
        Creator : Quentin Nater
        reviewed by :
        Delete the API Database NEO4J online
        """

        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/


        # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
        uri = "neo4j+s://0d2d7b8e.databases.neo4j.io:7687"
        user = "neo4j"
        password = "bta9fHGXHYBwD1fIKnLpJwwFUiZZxwtV5zouYfcgCwA"
        app = PersistenceGraph(uri, user, password)

        query = (
            "MATCH(n) DETACH DELETE n"
        )
        result = app.run(query)
        print("\t\t\t(NEO4J) : ", result)

        app.close()

    @staticmethod
    def _create_and_return_friendship(tx, person1_name, person2_name):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
            "CREATE (p1:Person { name: $person1_name }) "
            "CREATE (p2:Person { name: $person2_name }) "
            "CREATE (p1)-[:KNOWS]->(p2) "
            "RETURN p1, p2"
        )
        result = tx.run(query, person1_name=person1_name, person2_name=person2_name)
        try:
            return [{"p1": row["p1"]["name"], "p2": row["p2"]["name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def find_person(self, person_name):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_read(self._find_and_return_person, person_name)
            for row in result:
                print("Found person: {row}".format(row=row))

    @staticmethod
    def _find_and_return_person(tx, person_name):
        query = (
            "MATCH (p:Person) "
            "WHERE p.name = $person_name "
            "RETURN p.name AS name"
        )
        result = tx.run(query, person_name=person_name)
        return [row["name"] for row in result]
