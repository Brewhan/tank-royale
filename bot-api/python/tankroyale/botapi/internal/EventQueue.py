from tankroyale.botapi.internal.BaseBotInternals import BaseBotInternals, BotEventHandlers
from tankroyale.botapi.events import BotEvent, TickEvent, CustomEvent


class EventQueue:
    MAX_QUEUE_SIZE = 256
    MAX_EVENT_AGE = 2
    baseBotInternals: BaseBotInternals
    BotEventHandlers: BotEventHandlers

    currentTopEvent: BotEvent
    currentTopEventPriority: int

    interruptibles = set()

    events = list(BotEvent)



    def clear(self):
        self.events.clear()
        BaseBotInternals.conditions.clear()
        currentTopEvent = None
        currentTopEventPriority = 0

    def clearEvents(self):
        self.events.clear()

    def setInterruptible(self, eventClass, interruptible: bool):
        if interruptible:
            self.interruptibles.add(eventClass)
        else:
            self.interruptibles.remove(eventClass)

    def isInterruptible(self):
        return self.currentTopEvent in self.interruptibles
    
    def addEventsFromTick(self, event: TickEvent):
        self.addEvent(event)
        map(self.addEvent, event)

        # self.add_custom_events()

    def addEvent(self, event):
        if len(self.events) > self.MAX_QUEUE_SIZE:
            print("Maximum event queue size has been reached: " + self.MAX_QUEUE_SIZE)
        else:
            self.events.append(event)

    # W I P
    # def add_custom_events(self):
    #     for condition in self.baseBotInternals.conditions:
    #         if condition.
    #             self.add_event(CustomEvent(self.baseBotInternals.tickEvent.turn_number, condition))

    # def add_event(self, custom_event: CustomEvent):
    #     self.add_custom_events(custom_event)


    def isNotOldOrCriticalEvent(self, event: BotEvent, currentTurn: int) -> bool:
        isNotOld = event.BotEvent.turn_number + self.MAX_EVENT_AGE >= currentTurn
        isCritical = event.BotEvent.is_critical
        return isNotOld or isCritical

    def isOldAndNonCriticalEvent(self, event: BotEvent, currentTurn: int) -> bool:
        isOld = event.BotEvent.turn_number + self.MAX_EVENT_AGE < currentTurn
        isNonCritical = not event.BotEvent.is_critical
        return isOld and isNonCritical
    

    def isInterruptible(self):
        return self.currentTopEvent.BotEvent.__class__ in self.interruptibles
    

    def sortEvents(self, events: list[BotEvent.BotEvent]) -> None:
        events.sort(key=lambda event: self.getPriority(event), reverse=True)

    def remove_old_events(self, current_turn):
        self.events = [event for event in self.events if not self.isOldAndNonCriticalEvent(event, current_turn)]

    def getPriority(self, event):
        return self.baseBotInternals.getPriority(event.__class__)
    

    def dispatchEvents(self, currentTurn: int) -> None:
        self.remove_old_events(currentTurn)
        self.sortEvents()
        while self.baseBotInternals.isRunning() and len(self.events) > 0:
            event = self.events[0]
            priority = self.getPriority(event)
            if priority < self.currentTopEventPriority:
                return
            if priority == self.currentTopEventPriority:
                if not self.isInterruptible():
                    return
                self.setInterruptible(event.__class__, False)
            oldTopEventPriority = self.currentTopEventPriority
            self.currentTopEventPriority = priority
            self.currentTopEvent = event
            self.events.remove(event)
            try:
                if self.isNotOldOrCriticalEvent(event, currentTurn):
                    self.BotEventHandlers.BotEventHandlers.fire(event)
                self.setInterruptible(event.__class__, False)
            finally:
                self.currentTopEventPriority = oldTopEventPriority