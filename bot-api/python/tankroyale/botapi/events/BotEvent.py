class BotEvent:
    turn_number: int

    def __init__(self, turn_number: int):
        self.turn_number = turn_number

    def turn_number(self):
        return self.turn_number

    @staticmethod
    def is_critical():
        return False
