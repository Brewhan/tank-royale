from dataclasses import dataclass


@dataclass
class BotAddress:
    host: str
    port: int
