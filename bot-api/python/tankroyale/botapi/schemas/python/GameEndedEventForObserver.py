from tankroyale.botapi.schemas.python.Message import Message
from dataclasses import dataclass


@dataclass
class GameEndedEventForObserver(Message):
    numberOfRounds: int
    results: str
