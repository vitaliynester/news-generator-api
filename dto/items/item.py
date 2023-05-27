from dataclasses import dataclass


@dataclass
class Item:
    uuid: str
    name: str
    type: str
