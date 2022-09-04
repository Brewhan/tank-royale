from tankroyale.botapi import BulletState
import BotEvent


class HitByBulletEvent(BotEvent):
    bullet: BulletState
    damage: float
    energy: float

    def __init__(self, turn_number, bullet, damage, energy):
        super(turn_number)
        self.bullet = bullet
        self.damage = damage
        self.energy = energy

    def bullet(self):
        return self.bullet

    def damage(self):
        return self.damage

    def energy(self):
        return self.energy