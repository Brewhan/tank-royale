from dataclasses import dataclass
from tankroyale.botapi.schemas.InitialPosition import InitialPosition


@dataclass
class BotHandshake:
    name: str
    version: str
    authors: [] = None
    description: str = None
    homepage: str = None
    countryCodes: list = None
    gameTypes: list = None
    platform: str = None
    programmingLang: str = None
    initialPosition: InitialPosition = None
    secret: str = None
    bootId: str = None
    sessionId: str = None
    type: str = "BotHandshake"
