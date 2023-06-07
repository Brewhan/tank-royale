from uri import URI
import websockets
from tankroyale.botapi.Constants import Constants
from tankroyale.botapi.events import RoundStartedEvent, BulletHitWallEvent, Condition, BulletFiredEvent, BulletHitBotEvent, BulletHitBulletEvent, ScannedBotEvent, DeathEvent, WonRoundEvent, SkippedTurnEvent, TickEvent, CustomEvent, BotDeathEvent, BulletHitWallEvent, HitByBulletEvent, HitWallEvent, DefaultEventPriority as dep
from tankroyale.botapi.internal import EventQueue, BotEventHandlers, StopResumeListener
from tankroyale.botapi.schemas import BotIntent

#import StopResumeListener

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

    maxSpeed = Constants.MAX_SPEED
    maxTurnRate = Constants.MAX_TURN_RATE
    maxGunTurnRate = Constants.MAX_GUN_TURN_RATE
    maxRadarTurnRate = Constants.MAX_RADAR_TURN_RATE

    savedTargetSpeed: float
    savedTurnRate: float
    savedGunTurnRate: float
    savedRadarTurnRate: float

    botIntent: BotIntent

    
    eventQueue = EventQueue
    botEventHandlers = BotEventHandlers.BotEventHandlers
    conditions = set(Condition)

    nextTurnMonitor = object()

    isRunning = False
    isStopped = False
    stopResumeListner = StopResumeListener()

    absDecelleration = abs(Constants.DECELERATION)

    eventHandlingDisabled = False

    eventPriorities = {
        WonRoundEvent: dep.DefaultEventPriority.WON_ROUND,
        SkippedTurnEvent: dep.DefaultEventPriority.SKIPPED_TURN,
        TickEvent: dep.DefaultEventPriority.TICK,
        CustomEvent: dep.DefaultEventPriority.CUSTOM,
        BotDeathEvent: dep.DefaultEventPriority.BOT_DEATH,
        BulletHitWallEvent: dep.DefaultEventPriority.BULLET_HIT_WALL,
        BulletHitBulletEvent: dep.DefaultEventPriority.BULLET_HIT_BULLET,
        BulletHitBotEvent: dep.DefaultEventPriority.BULLET_HIT_BOT,
        BulletFiredEvent: dep.DefaultEventPriority.BULLET_FIRED,
        HitByBulletEvent: dep.DefaultEventPriority.HIT_BY_BULLET,
        HitWallEvent: dep.DefaultEventPriority.HIT_WALL,
        ScannedBotEvent: dep.DefaultEventPriority.SCANNED_BOT,
        DeathEvent: dep.DefaultEventPriority.DEATH,
    }



       # create a new websocket connection to the server with a given url
    async def connect(self, url: URI) -> None:
        self.serverUrl = url
        self.serverSecret = ""
        self.connection = await websockets.connect(url)  
        # else if the message from the server is not "OK" then raise an error
        if await self.connection.recv() != "OK":
            raise RuntimeError("Failed to connect to server" + url)
        


        
    def init(self):        
        self.botEventHandlers.onRoundStarted.subscribe(self.onRoundStarted, 100)
        self.botEventHandlers.onNextTurn.subscribe(onNextTurn, 100)
        self.botEventHandlers.onBulletFired.subscribe(onBulletFired, 100)

    def setRunning(self, isRunning: bool):
        self.isRunning = isRunning

    def enableEventHandling(self, enable: bool):
        self.eventHandlingDisabled = not enable

    def setStopResumeHandler(self, stopResumeListener: StopResumeListener):
        self.stopResumeListner = stopResumeListener

    def onRoundStarted(self, event: RoundStartedEvent):
        self.resetMovement()
        self.eventQueue.clear
        self.isStopped = False
        self.eventHandlingDisabled = False

    def newBotIntent():
        botIntent = BotIntent.BotIntent
        botIntent.Type(BotIntent.Message.Type.BotIntent)
        return botIntent
        
    def resetMovement(self):
        self.botIntent.BotIntent.turnRate = 0
        self.botIntent.BotIntent.gunTurnRate = 0
        self.botIntent.BotIntent.radarTurnRate = 0
        self.botIntent.BotIntent.targetSpeed = 0
        self.botIntent.BotIntent.firepower = 0
    
    
    


    init()
      



