from tankroyale.botapi.schemas.BotResults import BotResults
from tankroyale.botapi.schemas.BotResultsForBot import BotResultsForBot


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
