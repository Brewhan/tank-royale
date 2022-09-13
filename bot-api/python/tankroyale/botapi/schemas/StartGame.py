from dataclasses import dataclass
from typing import Optional
from tankroyale.botapi.schemas.Message import Message
from tankroyale.botapi.schemas.BotAddress import BotAddress


@dataclass
class ResumeGame(Message):
    botAddresses: list[BotAddress]
    gameSetup: Optional[str]
