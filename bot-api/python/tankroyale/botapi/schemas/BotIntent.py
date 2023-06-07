from dataclasses import dataclass
from tankroyale.botapi.schemas.Message import Message

@dataclass
class BotIntent(Message):
    turnRate: float
    gunTurnRate: float
    radarTurnRate: float
    targetSpeed: float
    firepower: float
    adjustGunForBodyTurn: bool
    adjustRadarForBodyTurn: bool
    adjustRadarForGunTurn: bool
    rescan: bool
    fireAssist: bool
    bodyColor: str
    turretColor: str
    radarColor: str
    bulletColor: str
    scanColor: str
    tracksColor: str
    gunColor: str

    def __setattr__(self, key, value):
        if key == 'firePower':
            assert 3.0 > value > 0, f"value of {key} must be between 0.0 and 3.0: {value}"
        self.__dict__[key] = value
