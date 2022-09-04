import json
import warlock
from tankroyale.botapi import BotState


class BotStateMapper:
    with open('../../schemas/bot-state.json') as j:
        SchemaBotState = warlock.model_factory(json.load(j))
        j.close()

    def map(self: SchemaBotState):
        return BotState(energy=self.energy,
                        x=self.x,
                        y=self.y,
                        direction=self.direction,
                        gunDirection=self.gunDirection,
                        radarDirection=self.radarDirection,
                        radarSweep=self.radarSweep,
                        speed=self.speed,
                        turnRate=self.turnRate,
                        gunTurnRate=self.gunTurnRate,
                        radarTurnRate=self.radarTurnRate,
                        gunHeat=self.gunHeat,
                        bodyColor=self.bodyColor,
                        turretColor=self.turretColor,
                        radarColor=self.radarColor,
                        bulletColor=self.bulletColor,
                        scanColor=self.scanColor,
                        tracksColor=self.tracksColor,
                        gunColor=self.gunColor
                        )


print(BotStateMapper.bot_state(
    BotStateMapper.BotState(energy=10, x=10.1, y=10.2, direction=170, gunDirection=40, radarDirection=50,
                            radarSweep=20, speed=10, turnRate=20, gunTurnRate=10, radarTurnRate=20, gunHeat=40)))
