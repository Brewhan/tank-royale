from tankroyale.botapi.internal.BaseBotInternals import BaseBotInternals
import asyncio


class Bot(BaseBotInternals):

    # TODO: implement this properly - the issue here is that we need to understand
    #  distance remaining and loop the dispatch of the intent until it has gotten where it needs to go
    def forward(self, distance: float):
        self.botIntent.targetSpeed = distance
        self.dispatch_event()

    def back(self, distance: float):
        self.botIntent.targetSpeed = -distance
        self.dispatch_event()

    def turn_rate(self, turn_rate: float):
        self.botIntent.turnRate = turn_rate
        self.dispatch_event()

    def gun_turn_rate(self, turn_rate: float):
        self.botIntent.gunTurnRate = turn_rate
        self.dispatch_event()

    def radar_turn_rate(self, turn_rate: float):
        self.botIntent.radarTurnRate = turn_rate
        self.dispatch_event()

    # TODO: implement this properly
    # target_speed()

    # TODO: implement this properly
    # distance_remaining()

    def turn_left(self, degrees: float):
        self.botIntent.turnRate = degrees
        self.dispatch_event()

    def turn_right(self, degrees: float):
        self.botIntent.turnRate = -degrees
        self.dispatch_event()

    # TODO: implement this properly
    # turn_remaining()

    def turn_gun_left(self, degrees: float):
        self.botIntent.gunTurnRate = degrees
        self.dispatch_event()

    async def turn_gun_right(self, degrees: float):
        self.botIntent.gunTurnRate = -degrees
        await self.dispatch_event()

    # TODO: implement this properly
    # turn_gun_remaining()

    def turn_radar_left(self, degrees: float):
        self.botIntent.radarTurnRate = degrees
        self.dispatch_event()

    def turn_radar_right(self, degrees: float):
        self.botIntent.radarTurnRate = -degrees
        self.dispatch_event()

    # TODO: implement this properly
    # turn_radar_remaining()

    async def fire(self, firepower: float):
        self.botIntent.firepower = firepower
        await self.dispatch_event()
        #stop firing after first shot
        self.botIntent.firepower = 0
        await self.dispatch_event() ## THIS IS A DELIBERATE BUG - REMOVE ONCE TICK EVENT IS SENDING INTENTS EVERY TICK.

    async def stop(self):
        self.reset_movement()
        await self.dispatch_event()

    def rescan(self):
        self.botIntent.rescan = True
        self.dispatch_event()

    # TODO: implement this properly
    # wait_for()

    def start_bot(self, secret: str):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.start('', secret))

