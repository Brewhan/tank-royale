import Condition
from tankroyale.botapi import BaseBot


class NextTurnCondition(Condition):
    base_bot: BaseBot
    creation_turn_number: int

    def __init__(self, base_bot):
        super("NextTurnCondition")
        self.base_bot = base_bot
        self.creation_turn_number = base_bot.turn_number()

    def test(self):
        return self.base_bot.turn_number() > self.creation_turn_number
