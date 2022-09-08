from typing import Optional
from dataclasses import dataclass
from tankroyale.schemas.python.Message import Message
from tankroyale.schemas.python.InitialPosition import InitialPosition


@dataclass(kw_only=True)
class BotHandShake(Message):
    name: str
    version: str
    authors: []
    description: Optional[str] = None
    homepage: Optional[str] = None
    countryCodes: Optional[list] = None
    gameTypes: Optional[list] = None
    platform: Optional[str] = None
    programmingLang: Optional[str] = None
    initialPosition: Optional[InitialPosition] = None
    secret: Optional[str] = None
    bootId: Optional[str] = None
