from dataclasses import dataclass


@dataclass
class UpdateItem:
    name: str | None = None
    type: str | None = None
