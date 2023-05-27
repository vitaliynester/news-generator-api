from typing import List

from dto import Person, UpdatePerson, CreatePerson
from services.neo4j import Neo4jService


class PersonsService:
    def __init__(self):
        self.neo4j = Neo4jService()
        self.down()

    def down(self):
        self.neo4j.close()

    def start(self):
        self.neo4j.start()

    def get_all_persons(self) -> List[Person]:
        query = """
        MATCH path = (persons:Person) 
        WITH collect(path) as ps 
        CALL apoc.convert.toTree(ps) yield value 
        RETURN value
        """
        result: List[Person] = []
        try:
            self.start()
            raw_data = self.neo4j.exec(query)
            for d in raw_data:
                try:
                    person = Person(uuid=d['value']['uuid'],
                                    last_name=d['value']['lastName'],
                                    first_name=d['value']['firstName'],
                                    age=d['value']['age'],
                                    work=d['value']['work']
                                    )
                    result.append(person)
                except Exception:
                    continue
            return result
        except Exception:
            return []

    def get_one_person(self, uuid: str) -> Person | None:
        query = f"""
        MATCH path = (persons:Person) 
        WHERE persons.uuid = "{uuid}"
        WITH collect(path) as ps 
        CALL apoc.convert.toTree(ps) yield value 
        RETURN value
        """
        try:
            self.start()
            raw_data = self.neo4j.exec(query)
            for d in raw_data:
                try:
                    person = Person(uuid=d['value']['uuid'],
                                    last_name=d['value']['lastName'],
                                    first_name=d['value']['firstName'],
                                    age=d['value']['age'],
                                    work=d['value']['work']
                                    )
                    return person
                except Exception as ee:
                    print(ee)
                    return None
            return None
        except Exception as e:
            print(e)
            return None

    def update_person(self, uuid: str, person: UpdatePerson) -> Person | None:
        query = f"""
        MERGE path = (person:Person {'{'}uuid: "{uuid}" {'}'})
        {f'SET person.firstName = "{person.first_name}"' if person.first_name is not None else ''}
        {f'SET person.lastName = "{person.last_name}"' if person.last_name is not None else ''}
        {f'SET person.work = "{person.work}"' if person.work is not None else ''}
        {f'SET person.age = {person.age}' if person.age is not None else ''}
        WITH collect(path) as ps
        CALL apoc.convert.toTree(ps) yield value
        RETURN value
        """
        try:
            self.start()
            raw_data = self.neo4j.exec(query)
            for d in raw_data:
                try:
                    person = Person(uuid=d['value']['uuid'],
                                    last_name=d['value']['lastName'],
                                    first_name=d['value']['firstName'],
                                    age=d['value']['age'],
                                    work=d['value']['work']
                                    )
                    return person
                except Exception as ee:
                    print(ee)
                    return None
            return None
        except Exception as e:
            print(e)
            return None

    def create_person(self, person: CreatePerson) -> Person | None:
        query = f"""
        MERGE path = (person:Person {'{'} uuid: apoc.create.uuid() {'}'})
        SET person.firstName = "{person.first_name}"
        SET person.lastName = "{person.last_name}"
        SET person.work = "{person.work}"
        SET person.age = {person.age}
        WITH collect(path) as ps
        CALL apoc.convert.toTree(ps) yield value
        RETURN value
        """
        try:
            self.start()
            raw_data = self.neo4j.exec(query)
            for d in raw_data:
                try:
                    person = Person(uuid=d['value']['uuid'],
                                    last_name=d['value']['lastName'],
                                    first_name=d['value']['firstName'],
                                    age=d['value']['age'],
                                    work=d['value']['work']
                                    )
                    return person
                except Exception:
                    return None
            return None
        except Exception:
            return None

    def remove_person(self, uuid: str) -> bool:
        query = f"""
        MATCH (person: Person {'{'}uuid: "{uuid}"{'}'})
        DELETE person
        RETURN person
        """
        try:
            self.start()
            raw_data = self.neo4j.exec(query)
            for d in raw_data:
                try:
                    return d['person'] is not None
                except Exception:
                    return False
            return False
        except Exception:
            return False
