from tankroyale.botapi.schemas.Message import Message
from dataclasses import dataclass


@dataclass
class GameEndedEventForObserver(Message):
    numberOfRounds: int
    results: str
