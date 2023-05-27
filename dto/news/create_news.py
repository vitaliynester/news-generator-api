from dataclasses import dataclass
from typing import List


@dataclass
class CreateNews:
    items: List[str]
    persons: List[str]
    places: List[str]
    weathers: List[str]
