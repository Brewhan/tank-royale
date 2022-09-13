from dataclasses import dataclass


@dataclass
class BotResults:
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
