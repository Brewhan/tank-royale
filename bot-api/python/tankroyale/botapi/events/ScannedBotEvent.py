import BotEvent


class ScannedBotEvent(BotEvent):
    scanned_by_bot_id: int
    scanned_bot_id: int
    energy: float
    x: float
    y: float
    direction: float
    speed: float

    def __init__(self,
                 turn_number: int,
                 scanned_by_bot_id: int,
                 scanned_bot_id: int,
                 energy: float,
                 x: float,
                 y: float,
                 direction: float,
                 speed: float):
        super(turn_number)
        self.scanned_by_bot_id = scanned_by_bot_id
        self.scanned_bot_id = scanned_bot_id
        self.energy = energy
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed

    def scanned_by_bot_id(self):
        return self.scanned_by_bot_id

    def scanned_bot_id(self):
        return self.scanned_bot_id

    def energy(self):
        return self.energy

    def x(self):
        return self.x

    def y(self):
        return self.y

    def direction(self):
        return self.direction

    def speed(self):
        return self.speed
