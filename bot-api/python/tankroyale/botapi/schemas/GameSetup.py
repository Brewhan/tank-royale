from dataclasses import dataclass


@dataclass
class GameSetup:
    gameType: str
    arenaWidth: int
    isArenaWidthLocked: bool
    arenaHeight: int
    isArenaHeightLocked: bool
    minNumberOfParticipants: int
    isMinNumberOfParticipantsLocked: bool
    maxNumberOfParticipants: int
    isMaxNumberOfParticipantsLocked: bool
    numberOfRounds: int
    isNumberOfRoundsLocked: bool
    gunCoolingRate: float
    isGunCoolingRateLocked: bool
    maxInactivityTurns: int
    isMaxInactivityTurnsLocked: bool
    turnTimeout: int
    isTurnTimeoutLocked: bool
    readyTimeout: int
    isReadyTimeoutLocked: bool
    defaultTurnsPerSecond: int
