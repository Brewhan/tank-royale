from tankroyale.botapi.schemas.python.BotResults import BotResults
from tankroyale.botapi.schemas.python.BotResultsForBot import BotResultsForBot


class ResultsMapper:
    def map(self: BotResultsForBot):
        return BotResults(self.rank,
                          self.survival,
                          self.lastSurvivorBonus,
                          self.bulletDamage,
                          self.bulletKillBonus,
                          self.ramDamage,
                          self.ramKillBonus,
                          self.totalScore,
                          self.firstPlaces,
                          self.secondPlaces,
                          self.thirdPlaces
                          )
