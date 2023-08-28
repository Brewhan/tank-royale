from tankroyale.botapi.internal.Bot import Bot


class BrewBot(Bot):

    async def run(self):
        super().run()
        while self.isRunning:
            await self.turn_gun_right(10)






# AndyBot().on_round_started()

BrewBot().start_bot('PBbMsuCpFZtmEaNAWjqOKQ')

