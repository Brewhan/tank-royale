from abc import abstractmethod, ABC

import dataclasses
import json
import math

from websockets import connect
from tankroyale.botapi.Constants import Constants
from tankroyale.botapi.schemas.BotState import BotState
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
        self.intentDepth = 0

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

        self.savedTargetSpeed: float = 0
        self.savedTurnRate: float = 0
        self.savedGunTurnRate: float = 0
        self.savedRadarTurnRate: float = 0
        self.turnRemaining: float = 0
        self.distanceRemaining: float = 0
        self.gunTurnRemaining: float = 0
        self.radarTurnRemaining: float = 0
        self.enemySpotted: bool = False

        self.previousDirection: float = 0
        self.previousGunDirection: float = 0
        self.previousRadarDirection: float = 0

        self.roundNumber: int = 0

        self.botIntent: BotIntent

        self.isRunning = False
        self.isStopped = False
        self.isGameRunning = False

        self.absDeceleration = abs(Constants.DECELERATION)

        self.eventHandlingDisabled = False

    # create a new websocket connection to the server with a given url and return the ws so it can be used to send intents

    async def connect(self, url: str, server_secret: str, bot_name: str):
        if url == '':
            url = self.DEFAULT_SERVER_URL
        self.serverUrl = url
        self.serverSecret = server_secret
        async with connect(url) as ws:
            self.event = await ws.recv()
            if json.loads(self.event)['sessionId']:
                self.set_running(True)
            await ws.send(self.message(
                BotHandshake(name=bot_name, version="1.0", sessionId=json.loads(self.event)['sessionId'],
                             secret=server_secret)))
            self.connection = ws
            self.new_bot_intent()
            event = json.loads(self.event)
            self.isGameRunning = True
            while self.isGameRunning:
                if not self.isRunning:
                    print("connect: not running flag set")
                    self.set_running(True)
                    print("connect: handle startup event after flag set")
                    await self.handle_startup_event_type(event, self.connection)
                else:
                    print("connect: handle event if set_running true")
                    await self.handle_logistical_event()
                print("connect: send intent")
                if self.isGameRunning:  # Otherwise if the game ends we enter this again!
                    await self.send_intent()
            else:
                print("connect: detected game running is false.")
                return

    async def handle_startup_event_type(self, event: dict, ws: any):
        match event['type']:
            case Message.GameStartedEventForBot:
                print("handle_startup: game started event")
                await ws.send(self.message(BotIntent(type="BotReady")))
                self.new_bot_intent()
                self.on_round_started()
            case Message.RoundStartedEvent:
                await ws.send(self.message(BotIntent(type="BotIntent")))
                print("handle_startup: round started event")
                self.new_bot_intent()
                self.on_round_started()
            case Message.BotHitWallEvent:
                print("handle_startup: bot hit wall event")
                self.distanceRemaining = 0
            case Message.TickEventForBot:
                print("handle_startup: tick event")
                if event['turnNumber'] == 1:
                    print("handle_startup: turn number 1")
                    self.previousDirection = event['botState']['direction']
                    self.reset_movement()
                    print("run")
                    await self.run()
                # TODO: call relevant methods for each event
                # else:
                #     print("else")
                #     await self.send_intent()

                # TODO: more event types please
            case _:
                print("handle_startup: " + event['type'])
                print(self.botIntent)
                self.distanceRemaining = 0
                self.set_running(True)
                self.new_bot_intent()
                self.on_round_started()
                print(self.botIntent)
                print("handle_startup: running the bot")
                await self.run()

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

    def save_movement(self):
        self.savedTargetSpeed = self.botIntent.targetSpeed
        self.savedTurnRate = self.botIntent.turnRate
        self.savedGunTurnRate = self.botIntent.gunTurnRate
        self.savedRadarTurnRate = self.botIntent.radarTurnRate

    def resume(self):
        self.botIntent.targetSpeed = self.savedTargetSpeed
        self.botIntent.turnRate = self.savedTurnRate
        self.botIntent.gunTurnRate = self.savedGunTurnRate
        self.botIntent.radarTurnRate = self.savedRadarTurnRate

    def is_enemy_detected(self) -> bool:
        event = json.loads(self.event)
        if event['type'] == Message.TickEventForBot:
            if len(event['events']) > 0:
                for e in event['events']:
                    match e['type']:
                        case Message.ScannedBotEvent:
                            return True
                        case _:
                            return False

    async def send_intent(self):
        try:
            ws = self.connection
            self.botIntent.type = Message.BotIntent
            await ws.send(self.message(self.botIntent))
            self.event = await ws.recv()
            event = json.loads(self.event)

            if event['type'] == Message.RoundEndedEvent:
                print("send_intent: round ended event")
                self.set_running(False)

            if event['type'] == Message.RoundStartedEvent:
                print("send_intent: round started event")
                self.set_running(False)
                self.new_bot_intent()
                self.on_round_started()

            if event['type'] != Message.GameStartedEventForBot:  # consider this a dragon. delete at your peril
                try:
                    print("send_intent: check for round number increment")
                    print("send_intent: " + str(event))
                    if event['roundNumber'] > self.roundNumber:
                        self.roundNumber += 1
                        self.set_running(False)
                except KeyError:
                    print("cannot check: " + event['type'])

            if event['type'] == Message.TickEventForBot:
                print("send_intent: tick event")
                self.update_positions()
                if event['turnNumber'] == 1:
                    print("send_intent: turn 1 detected")
                    self.previousDirection = event['botState']['direction']
                    self.reset_movement()
                    await self.run()
                if len(event['events']) > 0:
                    for e in event['events']:
                        match e['type']:
                            case Message.BotHitWallEvent:
                                print("send_intent: bot hit wall event")
                                self.distanceRemaining = 0
                                await self.on_hit_wall(e)
                            case Message.ScannedBotEvent:
                                print("send_intent: scanned bot event")
                                self.enemySpotted = True
                                await self.on_scanned_bot(e)
                            case Message.BotHitBotEvent:
                                print("send_intent: bot hit bot event")
                                await self.on_hit_bot(e)

            else:
                print("send_intent: " + str(event))

        except RecursionError:
            print("send_intent: Recursion Error")
            return

    async def handle_logistical_event(self):
        try:
            ws = self.connection
            event = json.loads(self.event)
            match event['type']:
                case Message.GameStartedEventForBot:
                    print("handle_logistical_event: game started event")
                    await ws.send(self.message(BotIntent(type="BotReady")))
                    self.new_bot_intent()
                    self.on_round_started()
                case Message.RoundEndedEvent:
                    print("handle_logistical_event: round ended event")
                    self.roundNumber += 1
                    self.set_running(False)
                case Message.GameAbortedEvent:
                    print("handle_logistical_event: game aborted event")
                    self.isGameRunning = False
                case Message.GameEndedEventForBot:
                    print("handle_logistical_event: game ended event for bot")
                    self.isGameRunning = False
                case _:
                    print("handle_logistical_event: unknown event " + str(event['type']))

        except RecursionError:
            print("handle_logistical_event: recursion error")
            return

    def message(self, data_class: dataclasses):
        return str(dataclasses.asdict(data_class, dict_factory=lambda x: {k: v for (k, v) in x if v is not None and v !=
                                                                          ''}))

    async def start(self, url, secret, bot_name):
        await self.connect(url, secret, bot_name)

    # TODO: assign event to types instead of using json loads
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

            if math.copysign(1, distance * new_speed) != -1:
                self.isOverDriving = self.get_distance_travelled_until_stop(new_speed) > abs(distance)

            self.distanceRemaining = distance - new_speed

    def update_positions(self):
        self.update_turn_remaining()
        self.update_gun_turn_remaining()
        self.update_radar_turn_remaining()
        self.update_movement()
        self.enemySpotted = False

    def get_new_target_speed(self, speed, distance) -> float:
        if distance < 0:
            return -self.get_new_target_speed(-speed, -distance)
        target_speed = self.maxSpeed if distance == math.inf else min(self.maxSpeed, self.get_max_speed(distance))

        return self.clamp(target_speed, speed - self.absDeceleration, speed + Constants.ACCELERATION) if speed >= 0 \
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

    def clamp(self, n, smallest: float, largest: float):
        return max(smallest, min(n, largest))

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

    def _normalize_relative_angle2(self, angle: float) -> float:
        angle = angle % 360
        angle = (angle + 360) % 360
        if angle > 180:
            angle -= 360
        return angle

    def _normalize_relative_angle(self, angle: float) -> float:
        if (angle % 360) >= 0:
            if angle < 180:
                return angle
            else:
                return angle - 360
        else:
            if angle >= -180:
                return angle
            else:
                return angle + 360

    def _normalize_absolute_angle(self, angle: float) -> float:
        return angle if (angle % 360) > 0 else angle + 360

    def calc_bearing(self, direction) -> float:
        return self._normalize_relative_angle(direction - json.loads(self.event)['botState']['direction'])

    def calc_gun_bearing(self, direction) -> float:
        return self._normalize_relative_angle(direction - json.loads(self.event)['botState']['gunDirection'])

    def calc_radar_bearing(self, direction) -> float:
        return self._normalize_relative_angle(direction - json.loads(self.event)['botState']['radarDirection'])

    def distance_to(self, xy):
        return math.hypot(xy['x'] - json.loads(self.event)['botState']['x'],
                          xy['y'] - json.loads(self.event)['botState']['y'])

    def direction_to(self, xy):
        return self._normalize_absolute_angle(math.degrees(
            math.atan2(xy['y'] - json.loads(self.event)['botState']['y'],
                       xy['x'] - json.loads(self.event)['botState']['x'])))

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

    @abstractmethod
    def on_hit_wall(self, e):
        pass

    @abstractmethod
    def on_hit_bot(self, e):
        pass
