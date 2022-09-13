from tankroyale.botapi.schemas.Color import Color


class BulletState:
    bullet_id: int
    owner_id: int
    power: float
    x: float
    y: float
    direction: float
    color: Color

    def __init__(self,
                 bullet_id: int,
                 owner_id: int,
                 power: float,
                 x: float,
                 y: float,
                 direction: float,
                 color: Color) -> None:
        self.bullet_id = bullet_id
        self.owner_id = owner_id
        self.power = power
        self.x = x
        self.y = y
        self.direction = direction
        self.color = color
