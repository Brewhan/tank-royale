import BotEvent


class SkippedTurnEvent(BotEvent):

    def __init__(self, turn_number: int):
        super(turn_number)

    @staticmethod
    def is_critical():
        return True
