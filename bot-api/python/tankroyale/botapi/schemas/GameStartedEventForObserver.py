from dataclasses import dataclass
from tankroyale.botapi.schemas.Message import Message
from tankroyale.botapi.schemas.Participant import Participant


@dataclass
class GameStartedEventForBot(Message):
    gameSetup: str
    participants: list[Participant]
