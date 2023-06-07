# event handler which processes events in the order they have been added to the handler

import asyncio
from typing import Callable, List, Optional

from .Event import Event


class EventHandler(Event):


    # publish an event to all subscribers
    def publish(self, event: Event, *args, **kwargs) -> None:
        event.publish(*args, **kwargs)

    # make an object called EntryWithPriority, that  has a consumer named subscriber, and a proirity
    class EntryWithPriority:
        def __init__(self, subscriber: Callable, priority: int):
            self.subscriber = subscriber
            self.priority = priority

    # add an inner class called entry_with_proiroty_comparitor, which compares two entry_with_priority objects and returns the one with the higher priority
    # this is used to sort the list of subscribers by priority

    def compare(self, entry1: EntryWithPriority, entry2: EntryWithPriority) -> int:
        return entry1.priority - entry2.priority
        
    # create a final list of EntryWithPriority objects, named subscriberEntries as a new syncronized list
    subscriberEntries: List[EntryWithPriority] = asyncio.Semaphore()

     # add a subsriber to the event
    def subscribe(self, event: Event, subscriber: Callable) -> None:
        event.subscribe(subscriber)

    # add a subscriber with a priority to the event and have it added to the subscriberEntries list
    def subscribe(self, event: Event, subscriber: Callable, priority: int) -> None:
        entry = self.EntryWithPriority(subscriber, priority)
        self.subscriberEntries.append(entry)


