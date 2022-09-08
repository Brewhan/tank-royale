from dataclasses import dataclass
from tankroyale.botapi.schemas.python.Message import Message
from tankroyale.botapi.schemas.python.Participant import Participant


@dataclass
class GameStartedEventForBot(Message):
    gameSetup: str
    participants: list[Participant]
