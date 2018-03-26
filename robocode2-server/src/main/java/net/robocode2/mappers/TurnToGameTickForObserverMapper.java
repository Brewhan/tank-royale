package net.robocode2.mappers;

import net.robocode2.json_schema.events.TickEventForObserver;
import net.robocode2.model.Turn;
import net.robocode2.model.Round;

public final class TurnToGameTickForObserverMapper {

	private TurnToGameTickForObserverMapper() {}

	public static TickEventForObserver map(Round round, Turn turn) {
		TickEventForObserver tick = new TickEventForObserver();
		tick.setType(TickEventForObserver.Type.TICK_EVENT_FOR_OBSERVER);
		tick.setBotStates(BotsToBotsWithIdMapper.map(turn.getBots()));
		tick.setBulletStates(BulletsToBulletStatesMapper.map(turn.getBullets()));
		tick.setRoundState(RoundToRoundStateMapper.map(round, turn));
		tick.setEvents(EventsToEventsMapper.map(turn.getObserverEvents()));
		return tick;
	}
}