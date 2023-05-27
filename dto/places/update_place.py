from dataclasses import dataclass


@dataclass
class UpdatePlace:
    name: str | None = None
    type: str | None = None
