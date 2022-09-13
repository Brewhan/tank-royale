from dataclasses import dataclass
from tankroyale.botapi.schemas.Message import Message


@dataclass
class TpsChangedEvent(Message):
    tps: int
