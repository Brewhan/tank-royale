from dataclasses import dataclass
from typing import Optional
from tankroyale.botapi.schemas.python.Message import Message
from tankroyale.botapi.schemas.python.BotAddress import BotAddress


@dataclass
class ResumeGame(Message):
    botAddresses: list[BotAddress]
    gameSetup: Optional[str]
