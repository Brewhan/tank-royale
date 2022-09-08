from tankroyale.botapi.schemas.python.BotState import BotState


class BotStateMapper:
    def map(self: BotState):
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


print(BotStateMapper.map(
    BotState(energy=10, x=10.1, y=10.2, direction=170, gunDirection=40, radarDirection=50,
             radarSweep=20, speed=10, turnRate=20, gunTurnRate=10, radarTurnRate=20, gunHeat=40, bodyColor="FFFFFF",
             turretColor="FFFFFF", radarColor="FFFFFF", bulletColor="FFFFFF", scanColor="FFFFFF", tracksColor="FFFFFF",
             gunColor="FFFFFF")))
