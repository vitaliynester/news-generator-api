import os
from typing import List

import requests
from fastapi import HTTPException

from dto import News, CreateNews, DetailNews, Item, Person, Place, Weather
from services import ItemsService, PlacesService, PersonsService, WeathersService
from services.neo4j import Neo4jService


class NewsService:
    def __init__(self):
        self.neo4j = Neo4jService()
        self.down()

    def down(self):
        self.neo4j.close()

    def start(self):
        self.neo4j.start()

    def get_all_news(self) -> List[DetailNews]:
        query = f"""
        MATCH path = (news:News)-[*]->(c)
        WITH collect(path) AS ps
        CALL apoc.convert.toTree(ps) yield value
        RETURN value
        """
        result: List[DetailNews] = []
        try:
            self.start()
            raw_data = self.neo4j.exec(query)
            for d in raw_data:
                try:
                    items: List[Item] = []
                    persons: List[Person] = []
                    places: List[Place] = []
                    weathers: List[Weather] = []

                    for mention in d['value']['mentions']:
                        if mention['_type'] == 'Person':
                            person = Person(uuid=mention['uuid'],
                                            last_name=mention['lastName'],
                                            first_name=mention['firstName'],
                                            work=mention['work'],
                                            age=mention['age']
                                            )
                            persons.append(person)
                        if mention['_type'] == 'Weather':
                            weather = Weather(uuid=mention['uuid'], type=mention['type'])
                            weathers.append(weather)
                        if mention['_type'] == 'Place':
                            place = Place(uuid=mention['uuid'], name=mention['name'], type=mention['type'])
                            places.append(place)
                        if mention['_type'] == 'Item':
                            item = Item(uuid=mention['uuid'], name=mention['name'], type=mention['type'])
                            items.append(item)

                    news = DetailNews(uuid=d['value']['uuid'],
                                      query=d['value']['query'],
                                      content=d['value']['content'],
                                      items=items,
                                      places=places,
                                      persons=persons,
                                      weathers=weathers)
                    result.append(news)
                except Exception:
                    continue
            return result
        except Exception:
            return result

    def get_one_news(self, uuid: str) -> DetailNews | None:
        query = f"""
        MATCH path = (news:News)-[*]->(c)
        WHERE news.uuid = "{uuid}"
        WITH collect(path) AS ps
        CALL apoc.convert.toTree(ps) yield value
        RETURN value
        """
        try:
            self.start()
            raw_data = self.neo4j.exec(query)
            for d in raw_data:
                try:
                    items: List[Item] = []
                    persons: List[Person] = []
                    places: List[Place] = []
                    weathers: List[Weather] = []

                    for mention in d['value']['mentions']:
                        if mention['_type'] == 'Person':
                            person = Person(uuid=mention['uuid'],
                                            last_name=mention['lastName'],
                                            first_name=mention['firstName'],
                                            work=mention['work'],
                                            age=mention['age']
                                            )
                            persons.append(person)
                        if mention['_type'] == 'Weather':
                            weather = Weather(uuid=mention['uuid'], type=mention['type'])
                            weathers.append(weather)
                        if mention['_type'] == 'Place':
                            place = Place(uuid=mention['uuid'], name=mention['name'], type=mention['type'])
                            places.append(place)
                        if mention['_type'] == 'Item':
                            item = Item(uuid=mention['uuid'], name=mention['name'], type=mention['type'])
                            items.append(item)

                    news = DetailNews(uuid=d['value']['uuid'],
                                      query=d['value']['query'],
                                      content=d['value']['content'],
                                      items=items,
                                      places=places,
                                      persons=persons,
                                      weathers=weathers)

                    return news
                except Exception:
                    return None
            return None
        except Exception:
            return None

    def create_news(self, dto: CreateNews) -> News | None:
        news = self.check_exists_news(dto)
        if news is not None:
            return news
        # Шаг 0. Проверить все данные
        items: List[Item] = []
        items_service = ItemsService()
        for uuid in dto.items:
            item = items_service.get_one_item(uuid)
            if item is None:
                raise HTTPException(status_code=400, detail=f'Предмет {uuid} не найден!')
            items.append(item)
        items_service.down()

        places: List[Place] = []
        places_service = PlacesService()
        for uuid in dto.places:
            place = places_service.get_one_place(uuid)
            if place is None:
                raise HTTPException(status_code=400, detail=f'Место {uuid} не найдено!')
            places.append(place)
        places_service.down()

        persons: List[Person] = []
        persons_service = PersonsService()
        for uuid in dto.persons:
            person = persons_service.get_one_person(uuid)
            if person is None:
                raise HTTPException(status_code=400, detail=f'Участник {uuid} не найден!')
            persons.append(person)
        places_service.down()

        weathers: List[Weather] = []
        weathers_service = WeathersService()
        for uuid in dto.weathers:
            weather = weathers_service.get_one_weather(uuid)
            if weather is None:
                raise HTTPException(status_code=400, detail=f'Погода {uuid} не найдена!')
            weathers.append(weather)
        weathers_service.down()

        # Шаг 1. Сформировать текстовый запрос в ChatGPT
        persons_text = 'Действующие лица: '
        for person in persons:
            persons_text += f'{person.last_name} {person.first_name} в возрасте {person.age} работает в {person.work}, '
        persons_text = persons_text[:-2]

        artifacts_text = 'Артефакты: '
        for item in items:
            artifacts_text += f'{item.type} под названием {item.name}, '
        artifacts_text = artifacts_text[:-2]

        places_text = 'Места действия: '
        for place in places:
            places_text += f'{place.type} под названием {place.name}, '
        places_text = places_text[:-2]

        weathers_text = 'Погода: '
        for weather in weathers:
            weathers_text += f'{weather.type}, '
        weathers_text = weathers_text[:-2]

        request_text = f"{persons_text}\n{artifacts_text}\n{places_text}\n{weathers_text}\nСделай большую новость с учетом этих вводных"

        # Шаг 2. Отправить этот запрос на сервис
        url = f'{os.getenv("CHAT_GPT_SERVICE")}/api/v1/chat'
        response = requests.post(url, json={
            "message": request_text
        })
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail='Не удалось получить ответ из ChatGPT')
        content = response.json()['message']

        # Шаг 3. Сформировать запрос для Neo4J
        persons_query = ""
        persons_query_relation = ""
        for it, person in enumerate(persons):
            persons_query += f'(person{it}:Person {"{"}uuid: "{person.uuid}" {"}"}),'
            persons_query_relation += f'CREATE (news)-[:MENTIONS]->(person{it})'
        persons_query = persons_query[:-1]

        places_query = ""
        places_query_relation = ""
        for it, place in enumerate(places):
            places_query += f'(place{it}:Place {"{"}uuid: "{place.uuid}" {"}"}),'
            places_query_relation += f'CREATE (news)-[:MENTIONS]->(place{it})'
        places_query = places_query[:-1]

        items_query = ""
        items_query_relation = ""
        for it, item in enumerate(items):
            items_query += f'(item{it}:Item {"{"}uuid: "{item.uuid}" {"}"}),'
            items_query_relation += f'CREATE (news)-[:MENTIONS]->(item{it})'
        items_query = items_query[:-1]

        weathers_query = ""
        weathers_query_relation = ""
        for it, weather in enumerate(weathers):
            weathers_query += f'(weather{it}:Weather {"{"}uuid: "{weather.uuid}" {"}"}),'
            weathers_query_relation += f'CREATE (news)-[:MENTIONS]->(weather{it})'
        weathers_query = weathers_query[:-1]

        query = f"""
        MATCH {persons_query},{places_query},{items_query},{weathers_query}
        CREATE (news:News {"{"}uuid: apoc.create.uuid(), query: $request, content: $content{"}"})
        {persons_query_relation}
        {places_query_relation}
        {items_query_relation}
        {weathers_query_relation}
        RETURN news
        """
        try:
            self.start()
            raw_data = self.neo4j.save_news(query, request_text, content)
            for d in raw_data:
                try:
                    news = News(uuid=d['news']['uuid'],
                                content=d['news']['content'],
                                query=d['news']['query']
                                )
                    return news
                except Exception:
                    return None
            return None
        except Exception as e:
            return None

    def check_exists_news(self, dto: CreateNews) -> News | None:
        query = f"""
        MATCH path = (news:News), 
                     (news)-[:MENTIONS]->(characters:Person), 
                     (news)-[:MENTIONS]->(items:Item), 
                     (news)-[:MENTIONS]->(places:Place), 
                     (news)-[:MENTIONS]->(weathers:Weather)
        WHERE characters.uuid IN [{'"' + '",'.join([f"{uuid}" for uuid in dto.persons]).replace('",', '","') + '"'}]
          AND items.uuid IN [{'"' + '",'.join([f"{uuid}" for uuid in dto.items]).replace('",', '","') + '"'}]
          AND places.uuid IN [{'"' + '",'.join([f"{uuid}" for uuid in dto.places]).replace('",', '","') + '"'}]
          AND weathers.uuid IN [{'"' + '",'.join([f"{uuid}" for uuid in dto.weathers]).replace('",', '","') + '"'}]
        WITH collect(path) AS ps
        CALL apoc.convert.toTree(ps) yield value
        RETURN value
        """
        try:
            self.start()
            raw_data = self.neo4j.exec(query)
            for d in raw_data:
                try:
                    place = News(uuid=d['value']['uuid'],
                                 content=d['value']['content'],
                                 query=d['value']['query']
                                 )
                    return place
                except Exception:
                    return None
            return None
        except Exception:
            return None

    def remove_news(self, uuid: str) -> bool:
        query = f"""
        MATCH (news: News {'{'}uuid: "{uuid}"{'}'})
        DETACH DELETE news
        RETURN news
        """
        try:
            self.start()
            raw_data = self.neo4j.exec(query)
            for d in raw_data:
                try:
                    return d['news'] is not None
                except Exception:
                    return False
            return False
        except Exception:
            return False
