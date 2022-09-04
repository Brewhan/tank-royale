from tankroyale.botapi.events import BotEvent, Condition


class CustomEvent(BotEvent):
    condition: Condition

    def __init__(self, turn_number, condition):
        super(turn_number)
        self.condition = condition

    def condition(self):
        return self.condition
