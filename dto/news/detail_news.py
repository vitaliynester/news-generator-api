from dataclasses import dataclass
from typing import List

from ..items import Item
from ..persons import Person
from ..places import Place
from ..weathers import Weather


@dataclass
class DetailNews:
    uuid: str
    query: str
    content: str
    items: List[Item]
    persons: List[Person]
    places: List[Place]
    weathers: List[Weather]
