from tankroyale.botapi.internal.BaseBotInternals import BaseBotInternals


class EventQueue:
    MAX_QUEUE_SIZE = 256
    MAX_EVENT_AGE = 2
    baseBotInternals: BaseBotInternals
    