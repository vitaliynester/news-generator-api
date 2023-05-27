from dataclasses import dataclass


@dataclass
class CreateItem:
    name: str
    type: str
