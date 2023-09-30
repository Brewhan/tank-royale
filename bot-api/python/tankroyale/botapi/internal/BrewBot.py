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
        while self.stop_when_see_enemy and self.is_enemy_detected():
            try:
                print("detected")
                # await self.stop()
                await self.smart_fire(distance)
                await self.rescan()  # this needs implementing
                # self.resume()
            except RecursionError:
                print("recursion error hack don't @ me")
                return
        print("no enemy")
        return

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
            self.botIntent.firepower = 1
            await self.connection.send(self.message(self.botIntent))
            await self.connection.recv()
        elif distance > 50:
            self.botIntent.firepower = 2
            await self.fire(2)
            await self.connection.send(self.message(self.botIntent))
            await self.connection.recv()
        else:
            self.botIntent.firepower = 3
            await self.connection.send(self.message(self.botIntent))
            await self.connection.recv()
        self.botIntent.firepower = 0
        await self.connection.send(self.message(self.botIntent))
        await self.connection.recv()


BrewBot().start_bot('ZDGYJOivwIyqvYQqCP4LOg')
