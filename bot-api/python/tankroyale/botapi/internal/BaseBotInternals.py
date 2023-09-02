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
        self.turnRemaining: float = 0
        self.distanceRemaining: float = 0
        self.gunTurnRemaining: float = 0
        self.radarTurnRemaining: float = 0

        self.previousDirection: float = 0
        self.previousGunDirection: float = 0
        self.previousRadarDirection: float = 0

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
                    self.reset_movement()
                    await self.run()
                # TODO: call relevant methods for each event
                if len(event['events']) > 0:
                    for e in event['events']:
                        match e['type']:
                            case Message.ScannedBotEvent:
                                await self.on_scanned_bot(e)
                else:
                    await self.send_intent()

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
        if json.loads(self.event)['type'] == 'TickEventForBot': #try and move this higher
            self.update_turn_remaining()
            self.update_gun_turn_remaining()
            self.update_radar_turn_remaining()
            self.update_movement()

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

    def update_turn_remaining(self):
        delta = self.calc_delta_angle(json.loads(self.event)['botState']['direction'], self.previousDirection)
        self.previousDirection = json.loads(self.event)['botState']['direction']
        if abs(self.turnRemaining) <= abs(delta):
            self.turnRemaining = 0
        else:
            self.turnRemaining -= delta
            if self.is_near_zero(self.turnRemaining):
                self.turnRemaining = 0
        self.botIntent.turnRate = self.turnRemaining
        
    def update_gun_turn_remaining(self):
        delta = self.calc_delta_angle(json.loads(self.event)['botState']['gunDirection'], self.previousGunDirection)
        self.previousGunDirection = json.loads(self.event)['botState']['gunDirection']
        if abs(self.gunTurnRemaining) <= abs(delta):
            self.gunTurnRemaining = 0
        else:
            self.gunTurnRemaining -= delta
            if self.is_near_zero(self.gunTurnRemaining):
                self.gunTurnRemaining = 0
    
        self.botIntent.gunTurnRate = self.gunTurnRemaining

    def update_radar_turn_remaining(self):
        delta = self.calc_delta_angle(json.loads(self.event)['botState']['radarDirection'], self.previousRadarDirection)
        self.previousRadarDirection = json.loads(self.event)['botState']['radarDirection']
        if abs(self.radarTurnRemaining) <= abs(delta):
            self.radarTurnRemaining = 0
        else:
            self.radarTurnRemaining -= delta
            if self.is_near_zero(self.radarTurnRemaining):
                self.radarTurnRemaining = 0

        # self.set_radar_turn_rate(self.radarTurnRemaining)
        self.botIntent.radarTurnRate = self.radarTurnRemaining

    def update_movement(self):
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

    def get_distance_travelled_until_stop(self, speed) -> float:
        speed = abs(speed)
        distance = 0
        while speed > 0:
            distance += (speed := self.get_new_target_speed(speed, 0))
        return distance

    def is_near_zero(self, value: float) -> float:
        return abs(value) < .00001

    def clamp(self, n, smallest: float, largest: float): return max(smallest, min(n, largest))

    def calc_delta_angle(self, target_angle: float, source_angle: float) -> float:
        angle = target_angle - source_angle
        # angle += -360 if angle > 180 else 360 if angle < -180 else 0

        if angle > 180:
            angle += -360
        elif angle < -180:
            angle += 360
        else:
            angle += 0
        # return min(y-x, y-x+2*math.pi, y-x-2*math.pi, key=abs)
        return angle

    def to_infinite_value(self, turn_rate: float) -> float:
        if turn_rate > 0:
            return math.inf
        if turn_rate < 0:
            return -math.inf
        else:
            return 0

    def set_turn_rate(self, turn_rate: float):
        self.botIntent.turnRate = turn_rate
        self.turnRemaining = self.to_infinite_value(turn_rate)
        # self.send_intent()

    def set_gun_turn_rate(self, turn_rate: float):
        self.botIntent.gunTurnRate = turn_rate
        self.gunTurnRemaining = self.to_infinite_value(turn_rate)
        # self.send_intent()

    def set_radar_turn_rate(self, turn_rate: float):
        self.botIntent.radarTurnRate = turn_rate
        self.radarTurnRemaining = self.to_infinite_value(turn_rate)
        # self.send_intent()

    @abstractmethod
    def on_scanned_bot(self, e):
        pass


