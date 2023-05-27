from dataclasses import dataclass


@dataclass
class CreatePerson:
    first_name: str
    last_name: str
    work: str
    age: int
