from dataclasses import dataclass
from tankroyale.botapi.schemas.python.Event import Event
from tankroyale.botapi.schemas.python.BotStateWithId import BotStateWithId
from tankroyale.botapi.schemas.python.BulletState import BulletState
from tankroyale.botapi.events.BotEvent import BotEvent


@dataclass
class TickEventForObserver(Event):
    roundNumber: int
    botStates: list[BotStateWithId]
    bulletStates: list[BulletState]
    events: list[BotEvent]
