from dataclasses import dataclass
from tankroyale.botapi.schemas.python.Message import Message
from tankroyale.botapi.schemas.python.BotInfo import BotInfo


@dataclass
class BotListUpdate(Message):
    bots: list[BotInfo]
