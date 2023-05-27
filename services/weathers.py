from typing import List

from dto import Weather, UpdateWeather, CreateWeather
from services.neo4j import Neo4jService


class WeathersService:
    def __init__(self):
        self.neo4j = Neo4jService()
        self.down()

    def down(self):
        self.neo4j.close()

    def start(self):
        self.neo4j.start()

    def get_all_weathers(self) -> List[Weather]:
        query = """
        MATCH path = (weathers:Weather) 
        WITH collect(path) as ps 
        CALL apoc.convert.toTree(ps) yield value 
        RETURN value
        """
        result: List[Weather] = []
        try:
            self.start()
            raw_data = self.neo4j.exec(query)
            for d in raw_data:
                try:
                    weather = Weather(uuid=d['value']['uuid'],
                                      type=d['value']['type']
                                      )
                    result.append(weather)
                except Exception:
                    continue
            return result
        except Exception:
            return []

    def get_one_weather(self, uuid: str) -> Weather | None:
        query = f"""
        MATCH path = (weathers:Weather) 
        WHERE weathers.uuid = "{uuid}"
        WITH collect(path) as ps 
        CALL apoc.convert.toTree(ps) yield value 
        RETURN value
        """
        try:
            self.start()
            raw_data = self.neo4j.exec(query)
            for d in raw_data:
                try:
                    weather = Weather(uuid=d['value']['uuid'],
                                      type=d['value']['type']
                                      )
                    return weather
                except Exception as ee:
                    return None
            return None
        except Exception as e:
            return None

    def update_weather(self, uuid: str, weather: UpdateWeather) -> Weather | None:
        query = f"""
        MERGE path = (weather:Weather {'{'}uuid: "{uuid}" {'}'})
        {f'SET weather.type = "{weather.type}"' if weather.type is not None else ''}
        WITH collect(path) as ps
        CALL apoc.convert.toTree(ps) yield value
        RETURN value
        """
        try:
            self.start()
            raw_data = self.neo4j.exec(query)
            for d in raw_data:
                try:
                    weather = Weather(uuid=d['value']['uuid'],
                                      type=d['value']['type']
                                      )
                    return weather
                except Exception as ee:
                    return None
            return None
        except Exception as e:
            return None

    def create_weather(self, weather: CreateWeather) -> Weather | None:
        query = f"""
        MERGE path = (weather:Weather {'{'} uuid: apoc.create.uuid() {'}'})
        SET weather.type = "{weather.type}"
        WITH collect(path) as ps
        CALL apoc.convert.toTree(ps) yield value
        RETURN value
        """
        try:
            self.start()
            raw_data = self.neo4j.exec(query)
            for d in raw_data:
                try:
                    weather = Weather(uuid=d['value']['uuid'],
                                      type=d['value']['type']
                                      )
                    return weather
                except Exception:
                    return None
            return None
        except Exception:
            return None

    def remove_weather(self, uuid: str) -> bool:
        query = f"""
        MATCH (weather: Weather {'{'}uuid: "{uuid}"{'}'})
        DELETE weather
        RETURN weather
        """
        try:
            self.start()
            raw_data = self.neo4j.exec(query)
            for d in raw_data:
                try:
                    return d['weather'] is not None
                except Exception:
                    return False
            return False
        except Exception:
            return False
