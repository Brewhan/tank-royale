from botapi.internal.EventHandler import EventHandler
from botapi.events import ConnectedEvent, BotEvent, GameStartedEvent, HitBotEvent, ConnectionErrorEvent, RoundStartedEvent, GameEndedEvent, BulletHitWallEvent, BulletFiredEvent, BulletHitBotEvent, BulletHitBulletEvent, ScannedBotEvent, DeathEvent, WonRoundEvent, SkippedTurnEvent, TickEvent, CustomEvent, BotDeathEvent, BulletHitWallEvent, HitByBulletEvent, HitWallEvent


class BotEventHandlers:

    onConnected = EventHandler(ConnectedEvent)
    onDisconnected = EventHandler(ConnectedEvent)
    onConnectionError = EventHandler(ConnectionErrorEvent)
    onGameStarted = EventHandler(GameStartedEvent)
    onGameEnded = EventHandler(GameEndedEvent)
    onGameAborted = EventHandler()
    onRoundStarted = EventHandler(RoundStartedEvent)
    onTick = EventHandler(TickEvent)
    onCustomEvent = EventHandler(CustomEvent)
    onBotDeath = EventHandler(BotDeathEvent)
    onBulletHitWall = EventHandler(BulletHitWallEvent)
    onBulletHitBullet = EventHandler(BulletHitBulletEvent)
    onBulletHitBot = EventHandler(BulletHitBotEvent)
    onBulletFired = EventHandler(BulletFiredEvent)
    onHitByBullet = EventHandler(HitByBulletEvent)
    onHitWall = EventHandler(HitWallEvent)
    onScannedBot = EventHandler(ScannedBotEvent)
    onDeath = EventHandler(DeathEvent)
    onWonRound = EventHandler(WonRoundEvent)
    onSkippedTurn = EventHandler(SkippedTurnEvent)
    onRoundStarted = EventHandler(RoundStartedEvent)
    onHitBot = EventHandler(HitBotEvent)

    onNextTurn = EventHandler(TickEvent)

    onConnected.subscribe(onConnected)
    onDisconnected.subscribe(onDisconnected)
    onConnectionError.subscribe(onConnectionError)
    onGameStarted.subscribe(onGameStarted)
    onGameEnded.subscribe(onGameEnded)
    onGameAborted.subscribe(onGameAborted)
    onRoundStarted.subscribe(onRoundStarted)
    onTick.subscribe(onTick)
    onCustomEvent.subscribe(onCustomEvent)
    onBotDeath.subscribe(onBotDeath)
    onBulletHitWall.subscribe(onBulletHitWall)
    onBulletHitBullet.subscribe(onBulletHitBullet)
    onBulletHitBot.subscribe(onBulletHitBot)
    onBulletFired.subscribe(onBulletFired)
    onHitByBullet.subscribe(onHitByBullet)
    onHitWall.subscribe(onHitWall)
    onScannedBot.subscribe(onScannedBot)
    onDeath.subscribe(onDeath)
    onWonRound.subscribe(onWonRound)
    onSkippedTurn.subscribe(onSkippedTurn)
    onRoundStarted.subscribe(onRoundStarted)
    onHitBot.subscribe(onHitBot)

    def fire(event: BotEvent):
        if isinstance(event, TickEvent):
            BotEventHandlers.onTick.publish(event)
        elif isinstance(event, ScannedBotEvent):
            BotEventHandlers.onScannedBot.publish(event)
        elif isinstance(event, SkippedTurnEvent):
            BotEventHandlers.onSkippedTurn.publish(event)
        elif isinstance(event, HitBotEvent):
            BotEventHandlers.onHitBot.publish(event)
        elif isinstance(event, HitByBulletEvent):
            BotEventHandlers.onHitByBullet.publish(event)
        elif isinstance(event, HitWallEvent):
            BotEventHandlers.onHitWall.publish(event)
        elif isinstance(event, DeathEvent):
            BotEventHandlers.onDeath.publish(event)
        elif isinstance(event, WonRoundEvent):
            BotEventHandlers.onWonRound.publish(event)
        elif isinstance(event, BotDeathEvent):
            BotEventHandlers.onBotDeath.publish(event)
        elif isinstance(event, BulletHitWallEvent):
            BotEventHandlers.onBulletHitWall.publish(event)
        elif isinstance(event, BulletHitBulletEvent):
            BotEventHandlers.onBulletHitBullet.publish(event)
        elif isinstance(event, BulletHitBotEvent):
            BotEventHandlers.onBulletHitBot.publish(event)
        elif isinstance(event, BulletFiredEvent):
            BotEventHandlers.onBulletFired.publish(event)
        elif isinstance(event, CustomEvent):
            BotEventHandlers.onCustomEvent.publish(event)
        else:
            raise Exception("IllegalStateException: The event is not a valid event")
        
        
        

