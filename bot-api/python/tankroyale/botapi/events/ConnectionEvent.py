import uri


class ConnectionEvent:
    server_uri: uri

    def __init__(self, server_uri: uri):
        self.server_uri = server_uri

    def server_uri(self):
        return self.server_uri
