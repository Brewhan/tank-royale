from dataclasses import dataclass
from enum import Enum


class Message:


    class Type(Enum):
        BotHandshake = "BotHandshake"
        ControllerHandshake = "ControllerHandshake"
        ObserverHandshake = "ObserverHandshake"
        ServerHandshake = "ServerHandshake"
        BotReady = "BotReady"
        BotIntent = "BotIntent"
        BotInfo = "BotInfo"
        BotListUpdate = "BotListUpdate"
        GameStartedEventForBot = "GameStartedEventForBot"
        GameStartedEventForObserver = "GameStartedEventForObserver"
        GameEndedEventForBot = "GameEndedEventForBot"
        GameEndedEventForObserver = "GameEndedEventForObserver"
        GameAbortedEvent = "GameAbortedEvent"
        GamePausedEventForObserver = "GamePausedEventForObserver"
        GameResumedEventForObserver = "GameResumedEventForObserver"
        RoundStartedEvent = "RoundStartedEvent"
        RoundEndedEvent = "RoundEndedEvent"
        ChangeTps = "ChangeTps"
        TpsChangedEvent = "TpsChangedEvent"
        BotDeathEvent = "BotDeathEvent"
        BotHitBotEvent = "BotHitBotEvent"
        BotHitWallEvent = "BotHitWallEvent"
        BulletFiredEvent = "BulletFiredEvent"
        BulletHitBotEvent = "BulletHitBotEvent"
        BulletHitBulletEvent = "BulletHitBulletEvent"
        BulletHitWallEvent = "BulletHitWallEvent"
        HitByBulletEvent = "HitByBulletEvent"
        ScannedBotEvent = "ScannedBotEvent"
        SkippedTurnEvent = "SkippedTurnEvent"
        TickEventForBot = "TickEventForBot"
        TickEventForObserver = "TickEventForObserver"
        WonRoundEvent = "WonRoundEvent"
        StartGame = "StartGame"
        StopGame = "StopGame"
        PauseGame = "PauseGame"
        ResumeGame = "ResumeGame"
        NextTurn = "NextTurn"

    
    type: Type