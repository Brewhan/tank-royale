import uri
from tankroyale.botapi.events import ConnectionEvent


class ConnectionErrorEvent(ConnectionEvent):
    error: BaseException

    def __init__(self, error: BaseException):
        self.error = error

    def error(self):
        return self.error
    