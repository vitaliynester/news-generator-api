from typing import List

from dto import Item, CreateItem, UpdateItem
from services.neo4j import Neo4jService


class ItemsService:
    def __init__(self):
        self.neo4j = Neo4jService()
        self.down()

    def down(self):
        self.neo4j.close()

    def start(self):
        self.neo4j.start()

    def get_all_items(self) -> List[Item]:
        query = """
        MATCH path = (items:Item) 
        WITH collect(path) as ps 
        CALL apoc.convert.toTree(ps) yield value 
        RETURN value
        """
        result: List[Item] = []
        try:
            self.start()
            raw_data = self.neo4j.exec(query)
            for d in raw_data:
                try:
                    item = Item(uuid=d['value']['uuid'],
                                name=d['value']['name'],
                                type=d['value']['type']
                                )
                    result.append(item)
                except Exception:
                    continue
            return result
        except Exception:
            return []

    def get_one_item(self, uuid: str) -> Item | None:
        query = f"""
        MATCH path = (items:Item) 
        WHERE items.uuid = "{uuid}"
        WITH collect(path) as ps 
        CALL apoc.convert.toTree(ps) yield value 
        RETURN value
        """
        try:
            self.start()
            raw_data = self.neo4j.exec(query)
            for d in raw_data:
                try:
                    item = Item(uuid=d['value']['uuid'],
                                name=d['value']['name'],
                                type=d['value']['type']
                                )
                    return item
                except Exception:
                    return None
            return None
        except Exception:
            return None

    def create_item(self, item: CreateItem) -> Item | None:
        query = f"""
        MERGE path = (item:Item {'{'} uuid: apoc.create.uuid() {'}'})
        SET item.name = "{item.name}"
        SET item.type = "{item.type}"
        WITH collect(path) as ps
        CALL apoc.convert.toTree(ps) yield value
        RETURN value
        """
        try:
            self.start()
            raw_data = self.neo4j.exec(query)
            for d in raw_data:
                try:
                    item = Item(uuid=d['value']['uuid'],
                                name=d['value']['name'],
                                type=d['value']['type']
                                )
                    return item
                except Exception:
                    return None
            return None
        except Exception:
            return None

    def update_item(self, uuid: str, item: UpdateItem) -> Item | None:
        query = f"""
        MERGE path = (item:Item {'{'}uuid: "{uuid}" {'}'})
        {f'SET item.name = "{item.name}"' if item.name is not None else ''}
        {f'SET item.type = "{item.type}"' if item.type is not None else ''}
        WITH collect(path) as ps
        CALL apoc.convert.toTree(ps) yield value
        RETURN value
        """
        try:
            self.start()
            raw_data = self.neo4j.exec(query)
            for d in raw_data:
                try:
                    item = Item(uuid=d['value']['uuid'],
                                name=d['value']['name'],
                                type=d['value']['type'],
                                )
                    return item
                except Exception as ee:
                    return None
            return None
        except Exception as e:
            return None

    def remove_item(self, uuid: str) -> bool:
        query = f"""
        MATCH (item: Item {'{'}uuid: "{uuid}"{'}'})
        DELETE item
        RETURN item
        """
        try:
            self.start()
            raw_data = self.neo4j.exec(query)
            for d in raw_data:
                try:
                    return d['item'] is not None
                except Exception:
                    return False
            return False
        except Exception:
            return False
