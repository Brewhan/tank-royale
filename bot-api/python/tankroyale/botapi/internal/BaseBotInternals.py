import dataclasses
import json
import asyncio
import threading
from websockets import connect
from tankroyale.botapi.Constants import Constants
# from tankroyale.botapi.events import RoundStartedEvent, BulletHitWallEvent, Condition, BulletFiredEvent, \
#     BulletHitBotEvent, BulletHitBulletEvent, ScannedBotEvent, DeathEvent, WonRoundEvent, SkippedTurnEvent, TickEvent, \
#     CustomEvent, BotDeathEvent, BulletHitWallEvent, HitByBulletEvent, HitWallEvent, DefaultEventPriority as dep
from tankroyale.botapi.schemas.BotHandshake import BotHandshake
from tankroyale.botapi.schemas.BotIntent import BotIntent
from tankroyale.botapi.schemas.Message import Message


class BaseBotInternals:

    def __init__(self):
        self.tickEvent = None
        self.botIntent = None
        self.connection = None
        self.event = None

        self.serverSecret = None
        self.serverUrl = None
        self.DEFAULT_SERVER_URL = "ws://localhost:7654"
        self.SERVER_URL_PROPERTY_KEY = "server.url"
        self.SERVER_SECRET_PROPERTY_KEY = "server.secret"
        self.NOT_CONNECTED_TO_SERVER_MSG = "Not connected to a game server. Make sure onConnected() event handler has been " \
                                           "called first "
        self.GAME_NOT_RUNNING_MSG = "Game is not running. Make sure onGameStarted() event handler has been called first"
        self.TICK_NOT_AVAILABLE_MSG = "Game is not running or tick has not occurred yet. Make sure onTick() event handler has " \
                                      "been called first "
        self.serverUrl: str
        self.serverSecret: str

        self.maxSpeed = Constants.MAX_SPEED
        self.maxTurnRate = Constants.MAX_TURN_RATE
        self.maxGunTurnRate = Constants.MAX_GUN_TURN_RATE
        self.maxRadarTurnRate = Constants.MAX_RADAR_TURN_RATE

        self.savedTargetSpeed: float
        self.savedTurnRate: float
        self.savedGunTurnRate: float
        self.savedRadarTurnRate: float

        self.botIntent: BotIntent
        # self.tickEvent: TickEvent.TickEvent

        self.isRunning = False
        self.isStopped = False

        self.absDecelleration = abs(Constants.DECELERATION)

        self.eventHandlingDisabled = False

        # self.eventPriorities = {
        #     WonRoundEvent: dep.DefaultEventPriority.WON_ROUND,
        #     SkippedTurnEvent: dep.DefaultEventPriority.SKIPPED_TURN,
        #     TickEvent: dep.DefaultEventPriority.TICK,
        #     CustomEvent: dep.DefaultEventPriority.CUSTOM,
        #     BotDeathEvent: dep.DefaultEventPriority.BOT_DEATH,
        #     BulletHitWallEvent: dep.DefaultEventPriority.BULLET_HIT_WALL,
        #     BulletHitBulletEvent: dep.DefaultEventPriority.BULLET_HIT_BULLET,
        #     BulletHitBotEvent: dep.DefaultEventPriority.BULLET_HIT_BOT,
        #     BulletFiredEvent: dep.DefaultEventPriority.BULLET_FIRED,
        #     HitByBulletEvent: dep.DefaultEventPriority.HIT_BY_BULLET,
        #     HitWallEvent: dep.DefaultEventPriority.HIT_WALL,
        #     ScannedBotEvent: dep.DefaultEventPriority.SCANNED_BOT,
        #     DeathEvent: dep.DefaultEventPriority.DEATH,
        # }

    # create a new websocket connection to the server with a given url and return the ws so it can be used to send intents

    async def connect(self, url: str, server_secret: str):
        if url == '':
            url = self.DEFAULT_SERVER_URL
        self.serverUrl = url
        self.serverSecret = server_secret
        async with connect(url) as ws:
            self.event = await ws.recv()
            if json.loads(self.event)['sessionId']:
                self.setRunning(True)
            await ws.send(self.message(BotHandshake(name="botName", version="1.0", sessionId=json.loads(self.event)['sessionId'], secret=server_secret)))
            # self.event = await ws.recv()
            self.connection = ws
            while self.isRunning:
                await self.handle_event_type(json.loads(self.event), self.connection)
                self.event = await self.connection.recv()

    async def handle_event_type(self, event: dict, ws: any):
        match event['type']:
            case Message.GameStartedEventForBot:
                await ws.send(self.message(BotIntent(type="BotReady")))
            case Message.RoundStartedEvent:
                await ws.send(self.message(BotIntent(type="BotIntent")))
            case Message.TickEventForBot:
                await ws.send(self.message(BotIntent(type="BotIntent", gunTurnRate=1.0)))
            case _:
                print(event)

    def setRunning(self, isRunning: bool):
        self.isRunning = isRunning

    def onRoundStarted(self):
        self.resetMovement()
        self.eventQueue.EventQueue.clear()
        self.isStopped = False
        self.eventHandlingDisabled = False

    def newBotIntent(self):
        self.botIntent = BotIntent.BotIntent
        self.botIntent.Type(BotIntent.Message.Type.BotIntent)

    def resetMovement(self):
        self.botIntent.BotIntent.turnRate = 0
        self.botIntent.BotIntent.gunTurnRate = 0
        self.botIntent.BotIntent.radarTurnRate = 0
        self.botIntent.BotIntent.targetSpeed = 0
        self.botIntent.BotIntent.firepower = 0

    def onRoundStarted(self):
        self.resetMovement()
        self.eventQueue.EventQueue.clear()
        self.isStopped = False
        self.eventHandlingDisabled = False

    def message(self, data_class: dataclasses):
        return str(dataclasses.asdict(data_class, dict_factory=lambda x: {k: v for (k, v) in x if v is not None and v !=
                                                                          ''}))

    async def start(self, url, secret):
        await self.connect(url, secret)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(BaseBotInternals().start('', 'PBbMsuCpFZtmEaNAWjqOKQ'))

