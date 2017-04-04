package net.robocode2.model;

import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import net.robocode2.model.events.IEvent;

public final class ImmutableTurn implements ITurn {

	private final int turnNumber;
	private final Set<IBot> bots;
	private final Set<IBullet> bullets;
	private final Set<IEvent> observerEvents;
	private final Map<Integer, Set<IEvent>> botEventsMap;

	public ImmutableTurn(int turnNumber, Set<IBot> bots, Set<IBullet> bullets, Set<IEvent> observerEvents,
			Map<Integer, Set<IEvent>> botEventsMap) {

		this.turnNumber = turnNumber;

		Set<ImmutableBot> immuBots = new HashSet<>();
		if (bots != null) {
			for (IBot bot : bots) {
				immuBots.add(new ImmutableBot(bot));
			}
		}
		this.bots = Collections.unmodifiableSet(immuBots);

		Set<ImmutableBullet> immuBullets = new HashSet<>();
		if (bullets != null) {
			for (IBullet bullet : bullets) {
				immuBullets.add(new ImmutableBullet(bullet));
			}
		}
		this.bullets = Collections.unmodifiableSet(immuBullets);

		Set<IEvent> immuObserverEvents = new HashSet<>();
		if (observerEvents != null) {
			immuObserverEvents.addAll(observerEvents);
		}
		this.observerEvents = Collections.unmodifiableSet(immuObserverEvents);

		Map<Integer, Set<IEvent>> immuBotEventsMap = new HashMap<>();
		if (botEventsMap != null) {
			immuBotEventsMap.putAll(botEventsMap);
		}
		this.botEventsMap = Collections.unmodifiableMap(immuBotEventsMap);
	}

	public ImmutableTurn(ITurn turn) {
		this(turn.getTurnNumber(), turn.getBots(), turn.getBullets(), turn.getObserverEvents(), turn.getBotEventsMap());
	}

	@Override
	public int getTurnNumber() {
		return turnNumber;
	}

	@Override
	public Set<IBot> getBots() {
		return bots;
	}

	@Override
	public Set<IBullet> getBullets() {
		return bullets;
	}

	@Override
	public Set<IEvent> getObserverEvents() {
		return observerEvents;
	}

	@Override
	public Map<Integer, Set<IEvent>> getBotEventsMap() {
		return botEventsMap;
	}
}