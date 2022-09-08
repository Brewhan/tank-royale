from dataclasses import dataclass
from tankroyale.botapi.schemas.python.Message import Message


@dataclass
class ChangeTps(Message):
    tps: int
