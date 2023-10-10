from tankroyale.botapi.internal.Bot import Bot


class BrewBot(Bot):
    turn_direction: int = 0

    async def run(self):
        try:
            await self.reset_to_zero()

            while self.isRunning:
                await self.turn_left(5 * self.turn_direction)
        except KeyError:  # ignore non processable events
            return

    async def on_scanned_bot(self, scanned_bot):
        await self.turn_to_face_target(scanned_bot)
        distance = self.distance_to(scanned_bot)
        await self.forward(distance + 5)


    async def on_hit_bot(self, e):
        # my keyboard is not letting me be Productive

    async def turn_to_face_target(self, xy):
        bearing = self.bearing_to(xy)
        if bearing >= 0:
            self.turn_direction = 1
        else:
            self.turn_direction = -1
        await self.turn_left(bearing)


BrewBot().start_bot('ZDGYJOivwIyqvYQqCP4LOg')
