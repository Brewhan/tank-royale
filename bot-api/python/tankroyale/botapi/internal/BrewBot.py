from tankroyale.botapi.internal.Bot import Bot


class BrewBot(Bot):

    # Called when bot starts
    async def run(self):
        await self.turn_gun_right(10)

    async def on_scanned_bot(self, e):
        await self.fire(1.0)


# AndyBot().on_round_started()

BrewBot().start_bot('PBbMsuCpFZtmEaNAWjqOKQ')

