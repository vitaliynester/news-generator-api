import os

from neo4j import GraphDatabase


class Neo4jService:
    def __init__(self):
        self.driver = None
        self.password = None
        self.user = None
        self.uri = None

        self.start()

    def start(self):
        self.uri = os.getenv('NEO4J_URI')
        self.user = os.getenv('NEO4J_USER')
        self.password = os.getenv('NEO4J_PASSWORD')

        if self.uri is None:
            raise Exception('NEO4J_URI не указан!')

        if self.user is None:
            raise Exception('NEO4J_USER не указан!')

        if self.password is None:
            raise Exception('NEO4J_PASSWORD не указан!')

        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def close(self):
        self.driver.close()

    def exec(self, query: str):
        with self.driver.session() as session:
            result = session.execute_write(self._create_and_return_result, query)
            return result

    def save_news(self, query: str, request: str, content: str):
        with self.driver.session() as session:
            result = session.execute_write(self._create_and_return_result_for_news, query, request, content)
            return result

    @staticmethod
    def _create_and_return_result(tx, query):
        result = tx.run(query)
        return result.data()

    @staticmethod
    def _create_and_return_result_for_news(tx, query, request: str, content: str):
        result = tx.run(query, request=request, content=content)
        return result.data()
