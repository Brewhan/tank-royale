from dataclasses import dataclass

from tankroyale.botapi.schemas import BulletState, BotState
from tankroyale.botapi.events.BotEvent  import BotEvent

@dataclass
class TickEvent(BotEvent):
    round_number: int
    enemy_count: int
    bot_state: BotState
    
    bullet_states: list[BulletState.BulletState]
    events: list[BotEvent]

    def __init__(self,
                 turn_number: int,
                 round_number: int,
                 bot_state: BotState,
                 bullet_states: list[BulletState.BulletState],
                 events: list[BotEvent]):
        super(turn_number)
        self.round_number = round_number
        self.bot_state = bot_state
        self.bullet_states = bullet_states
        self.events = events

    def round_number(self):
        return self.round_number

    def enemy_count(self):
        return self.enemy_count

    def bot_state(self):
        return self.bot_state

    def bullet_states(self):
        return self.bullet_states

    def events(self):
        return self.events
    