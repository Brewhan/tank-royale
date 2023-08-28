from tankroyale.botapi.internal.BaseBotInternals import BaseBotInternals
import asyncio


class Bot(BaseBotInternals):

    # TODO: implement this properly
    def forward(self, distance: float):
        self.botIntent.targetSpeed(distance)

    def back(self, distance: float):
        self.botIntent.targetSpeed(-distance)

    def turn_rate(self, turn_rate: float):
        self.botIntent.turnRate(turn_rate)

    def gun_turn_rate(self, turn_rate: float):
        self.botIntent.gunTurnRate(turn_rate)

    def radar_turn_rate(self, turn_rate: float):
        self.botIntent.radarTurnRate(turn_rate)

    # TODO: implement this properly
    # target_speed()

    # TODO: implement this properly
    # distance_remaining()

    def turn_left(self, degrees: float):
        self.botIntent.turnRate(degrees)

    def turn_right(self, degrees: float):
        self.botIntent.turnRate(-degrees)

    # TODO: implement this properly
    # turn_remaining()

    def turn_gun_left(self, degrees: float):
        self.botIntent.gunTurnRate(degrees)

    def turn_gun_right(self, degrees: float):
        self.botIntent.gunTurnRate(-degrees)

    # TODO: implement this properly
    # turn_gun_remaining()

    def turn_radar_left(self, degrees: float):
        self.botIntent.radarTurnRate(self, degrees)

    def turn_radar_right(self, degrees: float):
        self.botIntent.radarTurnRate(-degrees)

    # TODO: implement this properly
    # turn_radar_remaining()

    def fire(self, firepower: float):
        self.botIntent.firepower(firepower)

    def stop(self):
        self.reset_movement()

    def rescan(self):
        self.botIntent.rescan = True

    # TODO: implement this properly
    # wait_for()


# TODO: make this a function callable in the bot script
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(Bot().start('', 'PBbMsuCpFZtmEaNAWjqOKQ'))
