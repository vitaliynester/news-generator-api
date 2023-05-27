from dataclasses import dataclass


@dataclass
class News:
    uuid: str
    content: str
    query: str
