from tankroyale.botapi.internal.Bot import Bot


class BrewBot(Bot):
    async def run(self):
        await self.turn_gun_right(10)

    def on_scanned_bot(self, e):
        print("scanned event")
        self.fire(1.0)
        print(self.botIntent)


# AndyBot().on_round_started()

BrewBot().start_bot('PBbMsuCpFZtmEaNAWjqOKQ')

