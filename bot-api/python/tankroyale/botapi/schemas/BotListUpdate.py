from dataclasses import dataclass
from tankroyale.botapi.schemas.Message import Message
from tankroyale.botapi.schemas.BotInfo import BotInfo


@dataclass
class BotListUpdate(Message):
    bots: list[BotInfo]
