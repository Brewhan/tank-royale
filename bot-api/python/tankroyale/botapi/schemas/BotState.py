from dataclasses import dataclass


@dataclass
class BotState:
    energy: float
    x: float
    y: float
    direction: float
    gunDirection: float
    radarDirection: float
    radarSweep: float
    speed: float
    turnRate: float
    gunTurnRate: float
    radarTurnRate: float
    gunHeat: float
    bodyColor: str
    turretColor: str
    radarColor: str
    bulletColor: str
    scanColor: str
    tracksColor: str
    gunColor: str
