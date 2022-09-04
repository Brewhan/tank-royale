from tankroyale.botapi.events import ConnectionEvent
from typing import Optional
import uri


class DisconnectedEvent(ConnectionEvent):
    remote: bool
    status_code: int
    reason: str

    def __init__(self, server_uri: uri, remote, status_code, reason):
        super(server_uri)
        self.remote = remote
        self.status_code = status_code
        self.reason = reason

    def is_remote(self):
        return self.remote

    def status_code(self):
        return Optional[self.status_code]

    def reason(self):
        return Optional[self.reason]
