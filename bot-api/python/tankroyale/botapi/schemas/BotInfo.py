from dataclasses import dataclass
from tankroyale.botapi.schemas.BotHandshake import BotHandShake


@dataclass
class BotInfo(BotHandShake):
    host: str = None
    type: int = None
