import asyncio
from abc import ABC

from tankroyale.botapi.internal.Bot import Bot


class BrewBot(Bot):
    turn_direction: int = 1
    seeking = True

    async def run(self):
        try:
            self.seeking = True
            await self.reset_to_zero()
            while self.isRunning and self.seeking:
                print("turning_left")
                await self.turn_left(5 * self.turn_direction)
        except KeyError:  # ignore non processable events
            return

    async def on_scanned_bot(self, scanned_bot):
        self.seeking = False
        print("on_scanned_bot: " + str(scanned_bot))
        await self.turn_to_face_target(scanned_bot)
        distance = self.distance_to(scanned_bot)
        await self.forward(distance + 50)
        print("on_scanned_bot: forward")
        # self.seeking = True

    async def on_hit_bot(self, e):
        if e['energy'] > 16:
            await self.fire(3)
        if e['energy'] > 10:
            await self.fire(4)
        if e['energy'] > 4:
            await self.fire(2)
        if e['energy'] > 0.4:
            await self.fire(0.1)
        await self.forward(40)  # Ram them again!

    async def turn_to_face_target(self, xy):
        bearing = self.calc_bearing(self.direction_to(xy))
        gun_bearing = self.calc_gun_bearing(self.direction_to(xy))
        print("turn_to_face_target: " + str(bearing))
        if bearing >= 0:
            self.turn_direction = 1
        else:
            self.turn_direction = -1
        await self.turn_left(bearing)
        # await self.turn_gun_left(gun_bearing)

    async def on_hit_wall(self, e):  # we do not use this but we must include it
        self.seeking = True
        pass


BrewBot().start_bot('ZDGYJOivwIyqvYQqCP4LOg', 'BrewRam')
