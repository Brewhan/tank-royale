from tankroyale.botapi.schemas.python.Message import Message
from dataclasses import dataclass


@dataclass
class GameEndedEventForBot(Message):
    numberOfRounds: int
    results: str
