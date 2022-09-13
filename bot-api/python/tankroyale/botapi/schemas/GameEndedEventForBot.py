from tankroyale.botapi.schemas.Message import Message
from dataclasses import dataclass


@dataclass
class GameEndedEventForBot(Message):
    numberOfRounds: int
    results: str
