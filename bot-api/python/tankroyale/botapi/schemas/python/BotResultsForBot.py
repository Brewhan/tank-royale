from dataclasses import dataclass


@dataclass
class BotResultsForBot:
    rank: int
    survival: int
    lastSurvivorBonus: int
    bulletDamage: int
    bulletKillBonus: int
    ramDamage: int
    ramKillBonus: int
    totalScore: int
    firstPlaces: int
    secondPlaces: int
    thirdPlaces: int

    def __setattr__(self, key, value):
        if key == "rank":
            assert key > 0, f"rank must be greater than 0: {value}"
