from dataclasses import dataclass
from typing import Optional


@dataclass
class Participant:
    id: int
    name: str
    version: str
    authors: list[str]
    gameTypes: list[str]
    description: Optional[str]
    homepage: Optional[str]
    countryCodes: Optional[list[str]]
    platform: Optional[str]
    programmingLang: Optional[str]
    initialPosition: Optional[str]
