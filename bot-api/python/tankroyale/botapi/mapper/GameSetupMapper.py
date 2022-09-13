from tankroyale.botapi.schemas.GameSetup import GameSetup


class GameSetupMapper:
    def map(self: GameSetup):
        return GameSetup(
            self.gameType,
            self.arenaWidth,
            self.arenaHeight,
            self.numberOfRounds,
            self.gunCoolingRate,
            self.maxInactivityTurns,
            self.turnTimeout,
            self.readyTimeout
        )
    