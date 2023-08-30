from dataclasses import dataclass


@dataclass
class BotIntent:
    turnRate: float = None
    gunTurnRate: float = None
    radarTurnRate: float = None
    targetSpeed: float = None
    firepower: float = None
    adjustGunForBodyTurn: bool = False
    adjustRadarForBodyTurn: bool = False
    adjustRadarForGunTurn: bool = False
    rescan: bool = True
    fireAssist: bool = True
    bodyColor: str = ""
    turretColor: str = ""
    radarColor: str = ""
    bulletColor: str = ""
    scanColor: str = ""
    tracksColor: str = ""
    gunColor: str = ""
    type: str = ""

    def __setattr__(self, key, value):
        if key == 'firePower':
            assert 3.0 > value > 0, f"value of {key} must be between 0.0 and 3.0: {value}"
        self.__dict__[key] = value
