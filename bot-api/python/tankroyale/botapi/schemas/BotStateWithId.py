from dataclasses import dataclass
from tankroyale.botapi.schemas.BotState import BotState


@dataclass
class BotStateWithId(BotState):
    id: int
