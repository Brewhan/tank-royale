class RoundEndedEvent:
    round_number: int
    turn_number: int

    def __init__(self, round_number: int, turn_number: int):
        self.round_number = round_number
        self.turn_number = turn_number

    def round_number(self):
        return self.round_number

    def turn_number(self):
        return self.turn_number
