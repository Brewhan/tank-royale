import websockets
from uri import URI
from tankroyale.botapi.Constants import Constants


class BaseBotInternals:
    DEFAULT_SERVER_URL = "ws://localhost:7654"
    SERVER_URL_PROPERTY_KEY = "server.url"
    SERVER_SECRET_PROPERTY_KEY = "server.secret"
    NOT_CONNECTED_TO_SERVER_MSG = "Not connected to a game server. Make sure onConnected() event handler has been " \
                                  "called first "
    GAME_NOT_RUNNING_MSG = "Game is not running. Make sure onGameStarted() event handler has been called first"
    TICK_NOT_AVAILABLE_MSG = "Game is not running or tick has not occurred yet. Make sure onTick() event handler has " \
                             "been called first "
    serverUrl: URI
    serverSecret: str

    ##EventQueue

    maxSpeed = Constants.MAX_SPEED
    maxTurnRate = Constants.MAX_TURN_RATE
    maxGunTurnRate = Constants.MAX_GUN_TURN_RATE
    maxRadarTurnRate = Constants.MAX_RADAR_TURN_RATE

    savedTargetSpeed: float
    savedTurnRate: float
    savedGunTurnRate: float
    savedRadarTurnRate: float
