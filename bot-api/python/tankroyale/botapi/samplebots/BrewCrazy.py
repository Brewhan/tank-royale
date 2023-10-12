import asyncio
from abc import ABC

from tankroyale.botapi.internal.Bot import Bot


class BrewBot(Bot, ABC):
    moving_forward: bool = False

    async def run(self):
        try:
            await self.reset_to_zero()
            while self.isRunning:
                await self.forward(40000)
                self.moving_forward = True
                # self.set_turn_right(90)
                # await self.wait_for_turn_remaining()
                # self.set_turn_left(180)
                # await self.wait_for_turn_remaining()
                # self.set_turn_right(180)
                # await self.wait_for_turn_remaining()
                async with asyncio.TaskGroup() as tg:
                    tg.create_task(self.turn_left(90))
                    tg.create_task(self.turn_right(90))
                    tg.create_task(self.turn_left(180))

            # await self.turn_right(180)

        except KeyError:  # ignore non processable events
            return

    async def on_hit_wall(self, e):
        print("on_hit_wall: hit wall")
        self.reverse_direction()

    async def on_hit_bot(self, e):
        self.reverse_direction()

    async def on_scanned_bot(self, scanned_bot):
        await self.fire(1)
        await self.fire(0)  # always turn the gun off after use - only polite.

    def reverse_direction(self):
        if self.moving_forward:
            print("reverse_direction: moving forward")
            self.back(40000)
            self.moving_forward = False
        else:
            print("reverse_direction: not moving forward")
            self.forward(40000)
            self.moving_forward = True

    async def wait_for_turn_remaining(self):
        while self.turnRemaining != 0:
            await self.send_intent()



BrewBot().start_bot('ZDGYJOivwIyqvYQqCP4LOg', 'BrewCrazy')
