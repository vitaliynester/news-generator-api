from dataclasses import dataclass


@dataclass
class UpdatePerson:
    first_name: str | None = None
    last_name: str | None = None
    work: str | None = None
    age: int | None = None
