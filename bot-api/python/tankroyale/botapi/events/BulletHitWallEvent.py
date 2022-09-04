from tankroyale.botapi.BulletState import BulletState


class BulletHitWallEvent:
    bullet_state: BulletState

    def __init__(self,
                 turn_number: int,
                 bullet_state: BulletState):
        super(turn_number)
        self.bullet_state = bullet_state
    
    def bullet(self):
        return self.bullet_state
