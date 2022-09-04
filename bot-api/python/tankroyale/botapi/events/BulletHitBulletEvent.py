from tankroyale.botapi import BulletState
import BotEvent


class BulletHitBulletEvent(BotEvent):
    bullet: BulletState
    hit_bullet: BulletState

    def __init__(self,
                 turn_number: int,
                 bullet: BulletState,
                 hit_bullet: BulletState):
        super(turn_number)
        self.bullet = bullet
        self.hit_bullet = hit_bullet

    def bullet(self):
        return self.bullet

    def hit_bullet(self):
        return self.hit_bullet
