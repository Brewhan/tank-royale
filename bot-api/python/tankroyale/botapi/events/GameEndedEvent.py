from tankroyale.botapi import BotResults


class GameEndedEvent:
    number_of_rounds: int
    results: BotResults

    def __init__(self, number_of_rounds: int, results: BotResults):
        self.number_of_rounds = number_of_rounds
        self.results = results

    def number_of_rounds(self):
        return self.number_of_rounds

    def results(self):
        return self.results
