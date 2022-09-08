from dataclasses import dataclass
from tankroyale.botapi.schemas.python.Message import Message


@dataclass
class TpsChangedEvent(Message):
    tps: int
