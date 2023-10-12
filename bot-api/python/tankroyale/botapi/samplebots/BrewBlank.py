from abc import ABC

from tankroyale.botapi.internal.Bot import Bot


class BrewBot(Bot, ABC):

    async def run(self):
        try:
            await self.reset_to_zero()
        except KeyError:  # ignore non processable events
            return

    async def on_scanned_bot(self, scanned_bot):
        while self.isRunning:
            await self.fire(1)
            await self.fire(0)  # always turn the gun off after use - only polite.

    async def on_hit_wall(self, e):
        pass

    async def on_hit_bot(self, e):
        pass


BrewBot().start_bot('ZDGYJOivwIyqvYQqCP4LOg', 'BrewBlank')
