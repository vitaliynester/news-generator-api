from typing import List

from dto import Place, CreatePlace, UpdatePlace
from services.neo4j import Neo4jService


class PlacesService:
    def __init__(self):
        self.neo4j = Neo4jService()
        self.down()

    def down(self):
        self.neo4j.close()

    def start(self):
        self.neo4j.start()

    def get_all_places(self) -> List[Place]:
        query = """
        MATCH path = (places:Place) 
        WITH collect(path) as ps 
        CALL apoc.convert.toTree(ps) yield value 
        RETURN value
        """
        result: List[Place] = []
        try:
            self.start()
            raw_data = self.neo4j.exec(query)
            for d in raw_data:
                try:
                    place = Place(uuid=d['value']['uuid'],
                                  name=d['value']['name'],
                                  type=d['value']['type']
                                  )
                    result.append(place)
                except Exception:
                    continue
            return result
        except Exception:
            return []

    def get_one_place(self, uuid: str) -> Place | None:
        query = f"""
        MATCH path = (places:Place) 
        WHERE places.uuid = "{uuid}"
        WITH collect(path) as ps 
        CALL apoc.convert.toTree(ps) yield value 
        RETURN value
        """
        try:
            self.start()
            raw_data = self.neo4j.exec(query)
            for d in raw_data:
                try:
                    place = Place(uuid=d['value']['uuid'],
                                  name=d['value']['name'],
                                  type=d['value']['type']
                                  )
                    return place
                except Exception:
                    return None
            return None
        except Exception:
            return None

    def create_place(self, place: CreatePlace) -> Place | None:
        query = f"""
        MERGE path = (place:Place {'{'} uuid: apoc.create.uuid() {'}'})
        SET place.name = "{place.name}"
        SET place.type = "{place.type}"
        WITH collect(path) as ps
        CALL apoc.convert.toTree(ps) yield value
        RETURN value
        """
        try:
            self.start()
            raw_data = self.neo4j.exec(query)
            for d in raw_data:
                try:
                    place = Place(uuid=d['value']['uuid'],
                                  name=d['value']['name'],
                                  type=d['value']['type']
                                  )
                    return place
                except Exception:
                    return None
            return None
        except Exception:
            return None

    def update_place(self, uuid: str, place: UpdatePlace) -> Place | None:
        query = f"""
        MERGE path = (place:Place {'{'}uuid: "{uuid}" {'}'})
        {f'SET place.name = "{place.name}"' if place.name is not None else ''}
        {f'SET place.type = "{place.type}"' if place.type is not None else ''}
        WITH collect(path) as ps
        CALL apoc.convert.toTree(ps) yield value
        RETURN value
        """
        try:
            self.start()
            raw_data = self.neo4j.exec(query)
            for d in raw_data:
                try:
                    place = Place(uuid=d['value']['uuid'],
                                  name=d['value']['name'],
                                  type=d['value']['type'],
                                  )
                    return place
                except Exception as ee:
                    return None
            return None
        except Exception as e:
            return None

    def remove_place(self, uuid: str) -> bool:
        query = f"""
        MATCH (place: Place {'{'}uuid: "{uuid}"{'}'})
        DELETE place
        RETURN place
        """
        try:
            self.start()
            raw_data = self.neo4j.exec(query)
            for d in raw_data:
                try:
                    return d['place'] is not None
                except Exception:
                    return False
            return False
        except Exception:
            return False
