class RoundStartedEvent:
    round_number: int

    def __init__(self, round_number):
        self.round_number = round_number

    def round_number(self):
        return self.round_number
