from abc import ABC

from tankroyale.botapi.internal.BaseBotInternals import BaseBotInternals
import asyncio
import json


class Bot(BaseBotInternals, ABC):

    # TODO: implement this properly - the issue here is that we need to understand
    #  distance remaining and loop the dispatch of the intent until it has gotten where it needs to go
    async def forward(self, distance: float):
        if self.isStopped:
            await self.send_intent()
        else:
            self.set_forward(distance)
            while True:
                if self.isRunning and (self.distanceRemaining != 0):
                    await self.send_intent()
                else:
                    break

    def set_forward(self, distance: float):
        speed = self.get_new_target_speed(json.loads(self.event)['botState']['speed'], distance)
        self.botIntent.targetSpeed = speed
        self.distanceRemaining = distance

    async def back(self, distance: float):
        await self.forward(-distance)

    def turn_rate(self, turn_rate: float):
        self.botIntent.turnRate = turn_rate
        self.send_intent()

    def gun_turn_rate(self, turn_rate: float):
        self.botIntent.gunTurnRate = turn_rate
        self.send_intent()

    def radar_turn_rate(self, turn_rate: float):
        self.botIntent.radarTurnRate = turn_rate
        self.send_intent()

    # TODO: implement this properly
    # target_speed()

    # TODO: implement this properly
    # distance_remaining()

    def turn_left(self, degrees: float):
        self.botIntent.turnRate = degrees
        self.send_intent()

    def turn_right(self, degrees: float):
        self.botIntent.turnRate = -degrees
        self.send_intent()

    # TODO: implement this properly
    # turn_remaining()

    def turn_gun_left(self, degrees: float):
        self.botIntent.gunTurnRate = degrees
        self.send_intent()

    async def turn_gun_right(self, degrees: float):
        self.botIntent.gunTurnRate = -degrees
        await self.send_intent()

    # TODO: implement this properly
    # turn_gun_remaining()

    def turn_radar_left(self, degrees: float):
        self.botIntent.radarTurnRate = degrees
        self.send_intent()

    def turn_radar_right(self, degrees: float):
        self.botIntent.radarTurnRate = -degrees
        self.send_intent()

    # TODO: implement this properly
    # turn_radar_remaining()

    async def fire(self, firepower: float):
        self.botIntent.firepower = firepower
        await self.send_intent()
        #stop firing after first shot
        self.botIntent.firepower = 0
        await self.send_intent() ## THIS IS A DELIBERATE BUG - REMOVE ONCE TICK EVENT IS SENDING INTENTS EVERY TICK.

    async def stop(self):
        self.reset_movement()
        await self.send_intent()

    def rescan(self):
        self.botIntent.rescan = True
        self.send_intent()

    # TODO: implement this properly
    # wait_for()

    def start_bot(self, secret: str):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.start('', secret))

