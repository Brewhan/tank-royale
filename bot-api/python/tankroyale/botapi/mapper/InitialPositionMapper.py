from tankroyale.botapi.schemas.python.InitialPosition import InitialPosition


class InitialPositionMapper:
    def map(self: InitialPosition):
        if self is None:
            return None
        initialPosition = InitialPosition
        initialPosition.y = self.y
        initialPosition.x = self.x
        initialPosition.angle = self.angle
        return initialPosition
