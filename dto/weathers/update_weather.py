from dataclasses import dataclass


@dataclass
class UpdateWeather:
    type: str | None = None
