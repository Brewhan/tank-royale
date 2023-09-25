import random
from tankroyale.botapi.internal.Bot import Bot


def random_corner() -> int:
    randint = random.randint(0, 3)
    return 90 * randint


class BrewBot(Bot):
    enemies: float
    corner = random_corner()
    stop_when_see_enemy = False
    counter = 0

    async def run(self):
        await self.go_corner()

        gun_increment: float = 1

        while self.isRunning:
            for i in range(0, 90):
                await self.turn_gun_right(gun_increment)
            gun_increment *= -1
        else:
            print("not running")

    async def on_scanned_bot(self, e):
        distance = self.distance_to(e['x'], e['y'])
        if self.stop_when_see_enemy:
            print(self.counter)
            # await self.stop()
            await self.smart_fire(distance)
            await self.rescan()  # this needs implementing
            # self.resume()
        else:
            await self.smart_fire(distance)

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


BrewBot().start_bot('ZDGYJOivwIyqvYQqCP4LOg')
