from dataclasses import dataclass


@dataclass
class Place:
    uuid: str
    name: str
    type: str
