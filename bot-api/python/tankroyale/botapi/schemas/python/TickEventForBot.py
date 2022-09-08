from dataclasses import dataclass
from tankroyale.botapi.schemas.python.Event import Event
from tankroyale.botapi.schemas.python.BotState import BotState
from tankroyale.botapi.schemas.python.BulletState import BulletState
from tankroyale.botapi.events.BotEvent import BotEvent


@dataclass
class TickEventForBot(Event):
    roundNumber: int
    enemyCount: int
    botState: BotState
    BulletStates: list[BulletState]
    events: list[BotEvent]
