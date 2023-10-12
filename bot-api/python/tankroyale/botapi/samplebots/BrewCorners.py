import random
from abc import ABC

from tankroyale.botapi.internal.Bot import Bot


def random_corner() -> int:
    randint = random.randint(0, 3)
    return 90 * randint


class BrewBot(Bot, ABC):
    enemies: float
    corner = random_corner()
    stop_when_see_enemy = False
    counter = 0

    async def run(self):
        try:
            await self.reset_to_zero()
            await self.go_corner()

            gun_increment: float = 1

            while self.isRunning:
                for i in range(0, 90):
                    await self.turn_gun_right(gun_increment)
                gun_increment *= -1
        except KeyError:  # ignore non processable events
            return

    async def on_scanned_bot(self, scanned_bot):
        while self.stop_when_see_enemy and self.is_enemy_detected() and self.isRunning:
            await self.smart_fire(self.distance_to(scanned_bot))
            await self.rescan()  # this needs implementing

    async def go_corner(self):
        self.stop_when_see_enemy = False
        bearing = self.calc_bearing(random_corner())
        await self.turn_left(bearing)
        self.stop_when_see_enemy = True
        await self.stop()
        await self.forward(5000)
        await self.turn_right(90)
        await self.forward(5000)
        await self.turn_gun_right(90)

    async def smart_fire(self, distance: float):
        if distance > 200 or self.get_energy() < 15:
            await self.fire(1)
        elif distance > 50:
            await self.fire(2)
        else:
            await self.fire(3)
        await self.fire(0)

    async def on_hit_bot(self, e):
        print("on_hit_bot")
        pass

    async def on_hit_wall(self, e):
        print("on_hit_wall")
        pass


BrewBot().start_bot('ZDGYJOivwIyqvYQqCP4LOg', 'BrewCorners')
