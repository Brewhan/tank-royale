from tankroyale.botapi.internal.Bot import Bot
import asyncio


class BrewBot(Bot):

    # Called when bot starts
    async def run(self):
        await self.forward(15.0)
        await self.turn_left(45)
        await self.forward(15.0)
        await self.back(15.0)
        # #TODO: turn left is very spinny - will have to look into this.
        # await self.turn_left(100)
        # await self.forward(1.0)
        # await self.turn_right(45)
        # await self.forward(1.0)
        await self.turn_gun_left(45.0)
        # await self.turn_gun_right(45.0)
        # await self.turn_radar_left(100.0)
        # await self.turn_radar_right(100.0)

    async def on_scanned_bot(self, e):
        await self.fire(1.0)


# AndyBot().on_round_started()

BrewBot().start_bot('PBbMsuCpFZtmEaNAWjqOKQ')
