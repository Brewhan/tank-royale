from dataclasses import dataclass

from tankroyale.botapi.schemas import BulletState, BotState
from tankroyale.botapi.events.BotEvent  import BotEvent


@dataclass
class TickEvent(BotEvent):
    roundNumber: int
    enemyCount: int
    botState: BotState
    bulletStates: list[BulletState.BulletState]
    events: list[BotEvent]
    type: str
