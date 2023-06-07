from dataclasses import dataclass


@dataclass
class Constants:
    BOUNDING_CIRCLE_RADIUS: int = 18
    SCAN_RADIUS: int = 1200
    MAX_TURN_RATE: int = 10
    MAX_GUN_TURN_RATE: int = 20
    MAX_RADAR_TURN_RATE: int = 45
    MAX_SPEED: int = 8
    MIN_FIREPOWER: float = 0.1
    MAX_FIREPOWER: float = 3
    MIN_BULLET_SPEED: float = 20 - 3 * MAX_FIREPOWER
    MAX_BULLET_SPEED: float = 20 - 3 * MIN_FIREPOWER
    ACCELERATION: int = 1
    DECELERATION: int = -2
