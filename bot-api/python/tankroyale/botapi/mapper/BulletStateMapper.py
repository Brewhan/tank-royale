from tankroyale.botapi.schemas.python.BulletState import BulletState
from tankroyale.botapi.schemas.python.Color import Color
import typing


class BulletStateMapper:

    @typing.overload
    def map(self: list[BulletState]):
        bullet_state_set = set()
        for i in self:
            bullet_state_set.add(i)

    def map(self: BulletState):
        return BulletState(bullet_id=self.bulledId,
                           owner_id=self.ownerId,
                           power=self.power,
                           x=self.x,
                           y=self.y,
                           direction=self.direction,
                           color=Color.from_hex(self.color))

