from dataclasses import dataclass


@dataclass
class Person:
    uuid: str
    first_name: str
    last_name: str
    age: int
    work: str
