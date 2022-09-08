from dataclasses import dataclass
from tankroyale.botapi.schemas.python.BotState import BotState


@dataclass
class BotStateWithId(BotState):
    id: int
