from tankroyale.botapi.events import BotEvent


class HitBotEvent(BotEvent):
    victim_id: int
    energy: float
    x: float
    y: float
    is_rammed: bool

    def __init__(self,
                 turn_number: int,
                 victim_id: int,
                 energy: float,
                 x: float,
                 y: float,
                 is_rammed: bool):
        super(turn_number)
        self.victim_id = victim_id
        self.energy = energy
        self.x = x
        self.y = y
        self.is_rammed = is_rammed

    def victim_id(self):
        return self.victim_id

    def energy(self):
        return self.energy

    def x(self):
        return self.x

    def y(self):
        return self.y

    def is_rammed(self):
        return self.is_rammed
