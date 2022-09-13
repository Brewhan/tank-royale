from tankroyale.botapi.schemas import BulletState
import BotEvent


class BulletHitBotEvent(BotEvent):
    victim_id: int
    bullet: BulletState
    damage: float
    energy: float

    def __init__(self,
                 turn_number: int,
                 victim_id: int,
                 bullet: BulletState,
                 damage: float,
                 energy: float):
        super(turn_number)
        self.victim_id = victim_id
        self.bullet = bullet
        self.damage = damage
        self.energy = energy

    def victim_id(self):
        return self.victim_id

    def bullet(self):
        return self.bullet

    def damage(self):
        return self.damage

    def energy(self):
        return self.energy
