from abc import abstractmethod, ABC

import dataclasses
import json
import math


from websockets import connect
from tankroyale.botapi.Constants import Constants
from tankroyale.botapi.schemas.BotHandshake import BotHandshake
from tankroyale.botapi.schemas.BotIntent import BotIntent
from tankroyale.botapi.schemas.Message import Message

class BaseBotInternals(ABC):

    def __init__(self):
        self.isOverDriving = None
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
        self.distanceRemaining: float = 0

        self.botIntent: BotIntent
        # self.tickEvent: TickEvent.TickEvent

        self.isRunning = False
        self.isStopped = False

        self.absDeceleration = abs(Constants.DECELERATION)

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
            case Message.TickEventForBot:
                if event['turnNumber'] == 1:
                    await self.run()
                # await ws.send(self.message(BotIntent(type="BotIntent", gunTurnRate=1.0)))
                # TODO: call relevant methods for each event

                for e in event['events']:
                    match e['type']:
                        case Message.ScannedBotEvent:
                            await self.on_scanned_bot(e)
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

    async def send_intent(self):
        ws = self.connection
        self.botIntent.type = Message.BotIntent
        await ws.send(self.message(self.botIntent))
        self.event = await ws.recv()
        await self.update_movement()

    def message(self, data_class: dataclasses):
        return str(dataclasses.asdict(data_class, dict_factory=lambda x: {k: v for (k, v) in x if v is not None and v !=
                                                                          ''}))

    async def start(self, url, secret):
        await self.connect(url, secret)

    #TODO: assign event to types instead of using json loads
    async def update_movement_simple(self):
        if json.loads(self.event)['botState']['speed'] > 0:
            self.distanceRemaining -= json.loads(self.event)['botState']['speed']
            self.botIntent.targetSpeed = self.distanceRemaining
        else:
            self.botIntent.targetSpeed = 0
            self.distanceRemaining = 0

    async def update_movement(self):
        if math.isinf(self.distanceRemaining):
            self.botIntent.targetSpeed = (self.maxSpeed if self.distanceRemaining == math.inf else -self.maxSpeed)
        else:
            distance = self.distanceRemaining
            new_speed = self.get_new_target_speed(json.loads(self.event)['botState']['speed'], distance)
            self.botIntent.targetSpeed = new_speed

            if self.is_near_zero(new_speed) and self.isOverDriving:
                distance = 0
                self.isOverDriving = False

            if math.copysign(1, distance*new_speed) != -1:
                self.isOverDriving = self.get_distance_travelled_until_stop(new_speed) > abs(distance)

            self.distanceRemaining = distance - new_speed

    def get_new_target_speed(self, speed, distance) -> float:
        if distance < 0:
            return -self.get_new_target_speed(-speed, -distance)
        target_speed = self.maxSpeed if distance == math.inf else min(self.maxSpeed, self.get_max_speed(distance))

        return self.clamp(target_speed, speed - self.absDeceleration, speed + Constants.ACCELERATION) if speed >= 0\
            else self.clamp(target_speed, speed - Constants.ACCELERATION, speed + self.get_max_deceleration(-speed))

    def get_max_speed(self, distance: float):
        deceleration_time = max(1, math.ceil((math.sqrt((4 * 2 / self.absDeceleration) * distance + 1) - 1) / 2))
        if deceleration_time == math.inf:
            return Constants.MAX_SPEED
        deceleration_distance = (deceleration_time / 2) * (deceleration_time - 1) * self.absDeceleration
        return ((deceleration_time - 1) * self.absDeceleration) + ((distance - deceleration_distance) /
                                                                   deceleration_time)

    def get_max_deceleration(self, speed):
        deceleration_time = speed / self.absDeceleration
        acceleration_time = 1 - deceleration_time
        return min(1, deceleration_time) * self.absDeceleration + max(0, acceleration_time) * Constants.ACCELERATION

    def is_near_zero(self, value: float) -> float:
        return abs(value) < .00001

    def clamp(self, n, smallest: float, largest: float): return max(smallest, min(n, largest))

    @abstractmethod
    def on_scanned_bot(self, e):
        pass

    def get_distance_travelled_until_stop(self, speed) -> float:
        speed = abs(speed)
        distance = 0
        while speed > 0:
            distance += (speed := self.get_new_target_speed(speed, 0))
        return distance
#
# if __name__ == "__main__":
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(BaseBotInternals().start('', 'PBbMsuCpFZtmEaNAWjqOKQ'))

