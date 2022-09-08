from dataclasses import dataclass
from tankroyale.botapi.schemas.python.Message import Message


@dataclass
class GameStartedEventForBot(Message):
    myId: int
    gameSetup: str
