from abc import abstractmethod, ABC

import dataclasses
import json

from websockets import connect
from tankroyale.botapi.Constants import Constants
from tankroyale.botapi.schemas.BotHandshake import BotHandshake
from tankroyale.botapi.schemas.BotIntent import BotIntent
from tankroyale.botapi.schemas.Message import Message


class BaseBotInternals(ABC):

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

    # create a new websocket connection to the server with a given url and return the ws so it can be used to send intents

    async def connect(self, url: str, server_secret: str):
        if url == '':
            url = self.DEFAULT_SERVER_URL
        self.serverUrl = url
        self.serverSecret = server_secret
        async with connect(url) as ws:
            self.event = await ws.recv()
            if json.loads(self.event)['sessionId']:
                self.set_running(True)
            await ws.send(self.message(BotHandshake(name="Brew", version="1.0", sessionId=json.loads(self.event)['sessionId'], secret=server_secret)))
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
                self.new_bot_intent()
                self.on_round_started()
                await self.run()
            case Message.TickEventForBot:
                # await ws.send(self.message(BotIntent(type="BotIntent", gunTurnRate=1.0)))
                # TODO: call relevant methods for each event

                for e in event['events']:
                    match e['type']:
                        case Message.ScannedBotEvent:
                            self.on_scanned_bot(e)
                # TODO: more event types please

            case _:
                pass

    def set_running(self, isRunning: bool):
        self.isRunning = isRunning

    @abstractmethod
    async def run(self):
        pass

    def on_round_started(self):
        self.reset_movement()
        self.isStopped = False

    def new_bot_intent(self):
        self.botIntent = BotIntent()

    def reset_movement(self):
        self.botIntent.gunTurnRate = 0
        self.botIntent.turnRate = 0
        self.botIntent.radarTurnRate = 0
        self.botIntent.targetSpeed = 0
        self.botIntent.firepower = 0

    async def dispatch_event(self):
        ws = self.connection
        self.botIntent.type = Message.BotIntent
        await ws.send(self.message(self.botIntent))
        self.event = await ws.recv() # maybe remove this

    def message(self, data_class: dataclasses):
        return str(dataclasses.asdict(data_class, dict_factory=lambda x: {k: v for (k, v) in x if v is not None and v !=
                                                                          ''}))

    async def start(self, url, secret):
        await self.connect(url, secret)

    @abstractmethod
    def on_scanned_bot(self, e):
        pass
#
# if __name__ == "__main__":
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(BaseBotInternals().start('', 'PBbMsuCpFZtmEaNAWjqOKQ'))

