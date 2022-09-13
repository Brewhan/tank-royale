from dataclasses import dataclass


@dataclass
class BotResultsForBot:
    rank: int
    survival: float
    lastSurvivorBonus: float
    bulletDamage: float
    bulletKillBonus: float
    ramDamage: float
    ramKillBonus: float
    totalScore: float
    firstPlaces: int
    secondPlaces: int
    thirdPlaces: int

    def __setattr__(self, key, value):
        if key == "rank":
            assert key > 0, f"rank must be greater than 0: {value}"
