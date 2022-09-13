from tankroyale.botapi.schemas import GameSetup


class GameStartedEvent:
    my_id: int
    game_setup: GameSetup

    def __init__(self, my_id: int, game_setup: GameSetup):
        self.my_id = my_id
        self.game_setup: game_setup

    def my_id(self):
        return self.my_id

    def game_setup(self):
        return self.game_setup
