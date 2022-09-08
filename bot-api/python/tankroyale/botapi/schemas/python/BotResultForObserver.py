from dataclasses import dataclass


@dataclass
class BotResultsForObserver:
    id: int
    name: str
    version: str