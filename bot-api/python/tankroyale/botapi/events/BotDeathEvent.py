import BotEvent


class BotDeathEvent(BotEvent):
    victim_id: int

    def __init__(self, turn_number: int, victim_id: int):
        super(turn_number)
        self.victim_id = victim_id

    def victim_id(self):
        return self.victim_id
