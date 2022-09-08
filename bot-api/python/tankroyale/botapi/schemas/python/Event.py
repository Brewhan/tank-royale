from dataclasses import dataclass
from tankroyale.botapi.schemas.python.Message import Message


@dataclass
class Event(Message):
    turnNumber: int
