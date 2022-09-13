from tankroyale.botapi.schemas.BotState import BotState
from tankroyale.botapi.schemas.TickEventForBot import TickEventForBot
from tankroyale.botapi.events.TickEvent import TickEvent
from tankroyale.botapi.mapper.BotStateMapper import BotStateMapper


class EventMapper:

    def map(self: TickEventForBot, myBotId: int):
        return TickEvent(self.turnNumber,
                         self.roundNumber,
                         self.enemyCount,
                         BotStateMapper.map(self.bulletStates),
                         map(self.events, myBotId))


print(EventMapper.map(TickEventForBot(turnNumber=10, roundNumber=10, enemyCount=10,
                                      botState=BotState(energy=10, x=10.1, y=10.2, direction=170, gunDirection=40,
                                                        radarDirection=50,
                                                        radarSweep=20, speed=10, turnRate=20, gunTurnRate=10,
                                                        radarTurnRate=20, gunHeat=40, bodyColor="FFFFFF",
                                                        turretColor="FFFFFF", radarColor="FFFFFF", bulletColor="FFFFFF",
                                                        scanColor="FFFFFF", tracksColor="FFFFFF",
                                                        gunColor="FFFFFF"), bulletStates=[], events=[]), 12))
