from abc import ABC

from tankroyale.botapi.internal.BaseBotInternals import BaseBotInternals
import asyncio
import json


class Bot(BaseBotInternals, ABC):

    # scanning whilst moving still has some ways to go - possibly some issue with threading

    # TODO: implement this properly - the issue here is that we need to understand
    #  distance remaining and loop the dispatch of the intent until it has gotten where it needs to go
    async def forward(self, distance: float):
        if self.isStopped:
            await self.send_intent(self.queue)
        else:
            self.set_forward(distance)
            while True:
                if self.isRunning and (self.distanceRemaining != 0):
                    await self.send_intent(self.queue)
                else:
                    break

    def set_forward(self, distance: float):
        speed = self.get_new_target_speed(json.loads(self.event)['botState']['speed'], distance)
        self.botIntent.targetSpeed = speed
        self.distanceRemaining = distance

    async def back(self, distance: float):
        await self.forward(-distance)

    # TODO: implement this properly
    # target_speed()

    # TODO: implement this properly
    # distance_remaining()

    async def turn_left(self, degrees: float):
        if self.isStopped:
            await self.send_intent(self.queue)
        else:
            self.set_turn_left(degrees)
        while True:
            if self.isRunning and self.turnRemaining != 0:
                await self.send_intent(self.queue)
            else:
                break

    def set_turn_left(self, degrees: float):
        self.turnRemaining = degrees
        self.botIntent.turnRate = degrees

    async def turn_right(self, degrees: float):
        await self.turn_left(-degrees)

    # TODO: implement this properly
    # turn_remaining()

    async def turn_gun_left(self, degrees: float):
        if self.isStopped:
            await self.send_intent(self.queue)
        else:
            self.set_turn_gun_left(degrees)
        while True:
            if self.isRunning and self.gunTurnRemaining != 0:
                await self.send_intent(self.queue)
            else:
                break

    def set_turn_gun_left(self, degrees: float):
        self.gunTurnRemaining = degrees
        self.botIntent.gunTurnRate = degrees

    async def turn_gun_right(self, degrees: float):
        await self.turn_gun_left(-degrees)

    # TODO: implement this properly
    # turn_gun_remaining()

    async def turn_radar_left(self, degrees: float):
        if self.isStopped:
            await self.send_intent(self.queue)
        else:
            self.set_turn_radar_left(degrees)
        while True:
            if self.isRunning and self.radarTurnRemaining != 0:
                await self.send_intent(self.queue)
            else:
                break

    def set_turn_radar_left(self, degrees: float):
        self.radarTurnRemaining = degrees
        self.botIntent.radarTurnRate = degrees

    async def turn_radar_right(self, degrees: float):
        await self.turn_radar_left(-degrees)

    # TODO: implement this properly
    # turn_radar_remaining()

    async def fire(self, firepower: float):
        self.botIntent.firepower = firepower
        await self.send_intent(self.queue)
        # stop firing after first shot
        self.botIntent.firepower = 0
        await self.send_intent(self.queue)  ## THIS IS A DELIBERATE BUG - REMOVE ONCE TICK EVENT IS SENDING INTENTS EVERY TICK.

    def get_energy(self) -> float:
        return json.loads(self.event)['botState']['energy']

    async def stop(self):
        self.save_movement()
        self.reset_movement()
        await self.send_intent(self.queue)

    # TODO: implement rescan
    async def rescan(self):
        self.botIntent.rescan = True
        await self.send_intent(self.queue)

    # TODO: implement this properly
    # wait_for()
