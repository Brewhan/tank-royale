class BotEvent:
    turnNumber: int

    def __init__(self, turnNumber: int):
        self.turnNumber = turnNumber

    def turn_number(self):
        return self.turnNumber

    @staticmethod
    def is_critical():
        return False
