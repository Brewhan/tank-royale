from dataclasses import dataclass
from typing import Optional
from tankroyale.botapi.schemas.Message import Message


@dataclass
class ObserverHandshake(Message):
    name: str
    version: str
    author: Optional[str] = None
    secret: Optional[str] = None
