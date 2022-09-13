from dataclasses import dataclass
from tankroyale.botapi.schemas.Message import Message


@dataclass
class ChangeTps(Message):
    tps: int
