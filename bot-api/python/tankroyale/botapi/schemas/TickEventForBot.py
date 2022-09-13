from dataclasses import dataclass
from tankroyale.botapi.schemas.Event import Event
from tankroyale.botapi.schemas.BotState import BotState
from tankroyale.botapi.schemas.BulletState import BulletState
from tankroyale.botapi.events.BotEvent import BotEvent


@dataclass
class TickEventForBot(Event):
    roundNumber: int
    enemyCount: int
    botState: BotState
    BulletStates: list[BulletState]
    events: list[BotEvent]
