from dataclasses import dataclass
from tankroyale.botapi.schemas.Message import Message


@dataclass
class Event(Message):
    turnNumber: int
