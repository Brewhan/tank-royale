from abc import ABC

from tankroyale.botapi.internal.Bot import Bot


class BrewBot(Bot, ABC):
    turn_direction = 1
    is_enemy_detected = False

    async def run(self):
        try:
            self.is_enemy_detected = False
            await self.reset_to_zero()
            while self.isRunning:
                if not self.is_enemy_detected:
                    await self.turn_left(2 * self.turn_direction)
        except KeyError:  # ignore non processable events
            return

    async def on_scanned_bot(self, scanned_bot):
        self.is_enemy_detected = True
        await self.turn_to_face_target(scanned_bot)
        distance = self.distance_to(scanned_bot)
        self.reset_movement()
        await self.forward(distance + 5)

    async def on_hit_bot(self, e):
        await self.turn_to_face_target(e)
        if e['energy'] > 16:
            await self.fire(3)
        elif e['energy'] > 10:
            await self.fire(2)
        elif e['energy'] > 4:
            await self.fire(1)
        elif e['energy'] > 2:
            await self.fire(.5)
        elif e['energy'] > .4:
            await self.fire(.1)
        await self.forward(40)

    async def turn_to_face_target(self, xy):
        bearing = self.calc_bearing(self.bearing_to(xy))
        if bearing >= 0:
            self.turn_direction = 1
        else:
            self.turn_direction = -1

        await self.turn_left(bearing)

    async def on_hit_wall(self, e):
        print("hit wall")
        self.is_enemy_detected = False
        await self.stop()
        await self.back(50)


BrewBot().start_bot('Ehs+AK6NdgwbO9jL9TCjfg', "BrewRam")
