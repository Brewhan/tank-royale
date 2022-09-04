import json
from tankroyale.botapi.BulletState import BulletState
from tankroyale.botapi.Color import Color
import warlock
import typing


class BulletStateMapper:
    with open('../../schemas/bullet-state.json') as j:
        SchemaBulletState = warlock.model_factory(json.load(j))
        j.close()

    @typing.overload
    def map(self: list[SchemaBulletState]):
        bullet_state_set = set()
        for i in self:
            bullet_state_set.add(i)

    def map(self: SchemaBulletState):
        return BulletState(bullet_id=self.bulledId,
                           owner_id=self.ownerId,
                           power=self.power,
                           x=self.x,
                           y=self.y,
                           direction=self.direction,
                           color=Color.from_hex(self.color))

