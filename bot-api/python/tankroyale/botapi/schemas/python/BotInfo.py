from dataclasses import dataclass
from tankroyale.schemas.python.BotHandshake import BotHandShake


@dataclass
class BotInfo(BotHandShake):
    host: str = None
    type: int = None
