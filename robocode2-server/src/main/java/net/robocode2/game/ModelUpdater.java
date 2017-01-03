package net.robocode2.game;

import static net.robocode2.model.Physics.BOT_BOUNDING_CIRCLE_DIAMETER;
import static net.robocode2.model.Physics.BOT_BOUNDING_CIRCLE_RADIUS;
import static net.robocode2.model.Physics.INITIAL_BOT_ENERGY;
import static net.robocode2.model.Physics.INITIAL_GUN_HEAT;
import static net.robocode2.model.Physics.MAX_BULLET_POWER;
import static net.robocode2.model.Physics.MAX_BULLET_SPEED;
import static net.robocode2.model.Physics.MIN_BULLET_POWER;
import static net.robocode2.model.Physics.RADAR_RADIUS;
import static net.robocode2.model.Physics.calcBotSpeed;
import static net.robocode2.model.Physics.calcBulletSpeed;
import static net.robocode2.model.Physics.calcGunHeat;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;

import net.robocode2.model.Arc;
import net.robocode2.model.Arena;
import net.robocode2.model.Bot;
import net.robocode2.model.BotIntent;
import net.robocode2.model.Bullet;
import net.robocode2.model.GameSetup;
import net.robocode2.model.GameState;
import net.robocode2.model.ImmutableBot;
import net.robocode2.model.Physics;
import net.robocode2.model.Position;
import net.robocode2.model.Round;
import net.robocode2.model.Score;
import net.robocode2.model.Size;
import net.robocode2.model.Turn;
import net.robocode2.model.events.BotHitBotEvent;
import net.robocode2.model.events.BotHitWallEvent;
import net.robocode2.model.events.BulletFiredEvent;
import net.robocode2.model.events.BulletHitBulletEvent;
import net.robocode2.model.events.BulletMissedEvent;

public class ModelUpdater {

	private final static double RAM_DAMAGE = 0.6;

	private final GameSetup setup;

	private final ScoreKeeper scoreKeeper;

	private GameState.Builder gameStateBuilder;
	private Round.Builder roundBuilder;
	private Turn.Builder turnBuilder;

	private int roundNumber;
	private int turnNumber;
	private boolean roundEnded;

	private int nextBulletId;

	private Map<Integer /* BotId */, BotIntent> botIntentMap = new HashMap<>();
	private Map<Integer /* BotId */, Bot.Builder> botStateMap = new HashMap<>();
	private Set<Bullet.Builder> bulletStateSet = new HashSet<>();

	public ModelUpdater(GameSetup setup) {
		this.setup = setup;
		this.scoreKeeper = new ScoreKeeper(setup.getParticipantIds());

		initialize();
	}

	private void initialize() {
		// Prepare game state builders
		gameStateBuilder = new GameState.Builder();
		roundBuilder = new Round.Builder();
		turnBuilder = new Turn.Builder();

		// Prepare game state builder
		Arena arena = new Arena(new Size(setup.getArenaWidth(), setup.getArenaHeight()));
		gameStateBuilder.setArena(arena);

		roundNumber = 0;
		turnNumber = 0;
	}

	public GameState update(Map<Integer /* BotId */, BotIntent> botIntents) {
		botIntentMap = botIntents;

		if (roundEnded || roundNumber == 0) {
			nextRound();
		}

		nextTurn();

		return buildGameState();
	}

	private void nextRound() {
		roundNumber++;
		roundBuilder.setRoundNumber(roundNumber);

		roundEnded = false;

		nextBulletId = 0;

		Set<Bot> bots = initialBotStates();
		turnBuilder.setBots(bots);

		scoreKeeper.reset(setup.getParticipantIds());
	}

	private void nextTurn() {

		Turn previousTurn = turnBuilder.build();

		turnNumber++;
		turnBuilder.setTurnNumber(turnNumber);

		// Prepare map over new bot states
		botStateMap.clear();
		for (Bot bot : previousTurn.getBots()) {
			botStateMap.put(bot.getId(), new Bot.Builder(bot));
		}

		// Prepare new bullet states
		bulletStateSet.clear();
		for (Bullet bullet : previousTurn.getBullets()) {
			bulletStateSet.add(new Bullet.Builder(bullet));
		}

		// Execute bot intents
		executeBotIntents();

		// Check bullet to bullet collisions
		checkBulletToBulletCollisions();

		// Update bullet positions
		updateBulletPositions();

		// Check bot wall collisions
		checkBotWallCollisions();

		// Check bullet wall collisions
		checkBulletWallCollisions();

		// Check bot to bot collisions
		checkBotToBotCollisions();

		// Check bullet to bot collisions (bullet hits)

		// Fire guns
		fireGuns();

		// Cleanup dead robots (remove from arena + events)
	}

	private GameState buildGameState() {
		Turn turn = turnBuilder.build();
		roundBuilder.appendTurn(turn);

		Round round = roundBuilder.build();
		gameStateBuilder.appendRound(round);

		GameState gameState = gameStateBuilder.build();
		return gameState;
	}

	private Set<Bot> initialBotStates() {
		Set<Bot> bots = new HashSet<Bot>();

		Set<Integer> occupiedCells = new HashSet<Integer>();

		for (int id : setup.getParticipantIds()) {

			Bot.Builder builder = new Bot.Builder();
			builder.setId(id);
			builder.setEnergy(INITIAL_BOT_ENERGY);
			builder.setSpeed(0);
			builder.setPosition(randomBotPosition(occupiedCells));
			builder.setDirection(randomDirection());
			builder.setGunDirection(randomDirection());
			builder.setRadarDirection(randomDirection());
			builder.setScanArc(new Arc(0, RADAR_RADIUS));
			builder.setGunHeat(INITIAL_GUN_HEAT);
			builder.setScore(new Score.Builder().build());

			bots.add(builder.build());
		}

		return bots;
	}

	private Position randomBotPosition(Set<Integer> occupiedCells) {

		final int gridWidth = setup.getArenaWidth() / 100;
		final int gridHeight = setup.getArenaHeight() / 100;

		final int cellCount = gridWidth * gridHeight;

		final int numBots = setup.getParticipantIds().size();
		if (cellCount < numBots) {
			throw new IllegalArgumentException("Area size (" + setup.getArenaWidth() + ',' + setup.getArenaHeight()
					+ ") is to small to contain " + numBots + " bots");
		}

		final int cellWidth = setup.getArenaWidth() / gridWidth;
		final int cellHeight = setup.getArenaHeight() / gridHeight;

		double x, y;

		while (true) {
			int cell = (int) (Math.random() * cellCount);
			if (!occupiedCells.contains(cell)) {
				occupiedCells.add(cell);

				y = cell / gridWidth;
				x = cell - y * gridWidth;

				x *= cellWidth;
				y *= cellHeight;

				x += Math.random() * (cellWidth - BOT_BOUNDING_CIRCLE_DIAMETER);
				y += Math.random() * (cellHeight - BOT_BOUNDING_CIRCLE_DIAMETER);

				break;
			}
		}
		return new Position(x, y);
	}

	private void executeBotIntents() {
		for (Integer botId : botStateMap.keySet()) {
			BotIntent intent = botIntentMap.get(botId);
			Bot.Builder bot = botStateMap.get(botId);

			// Turn body, gun, radar, and move bot to new position
			double direction = bot.getDirection() + intent.getBodyTurnRate();
			double gunDirection = bot.getGunDirection() + intent.getGunTurnRate();
			double radarDirection = bot.getRadarDirection() + intent.getRadarTurnRate();
			double speed = calcBotSpeed(bot.getSpeed(), intent.getTargetSpeed());

			bot.setDirection(direction);
			bot.setGunDirection(gunDirection);
			bot.setRadarDirection(radarDirection);
			bot.setSpeed(speed);
			bot.setPosition(bot.getPosition().calcNewPosition(direction, speed));
		}
	}

	private void checkBulletToBulletCollisions() {
		Line[] boundingLines = new Line[bulletStateSet.size()];

		Bullet.Builder[] bulletBuilders = new Bullet.Builder[bulletStateSet.size()];
		bulletBuilders = bulletStateSet.toArray(bulletBuilders);

		for (int i = boundingLines.length - 1; i >= 0; i--) {
			Bullet.Builder bulletBuilder = bulletBuilders[i];

			Line line = new Line();
			line.start = bulletBuilder.calcPosition();
			line.end = bulletBuilder.calcNextPosition();

			boundingLines[i] = line;
		}

		for (int i = boundingLines.length - 1; i >= 0; i--) {
			Position endPos1 = boundingLines[i].end;

			for (int j = i - 1; j >= 0; j--) {
				Position endPos2 = boundingLines[j].end;

				// Check if the bullets bounding circles intersects (is fast) before checking if the bullets bounding
				// lines intersect (is slower)
				if (isBulletsBoundingCirclesColliding(endPos1, endPos2) && MathUtil.doLinesIntersect(
						boundingLines[i].start, boundingLines[i].end, boundingLines[j].start, boundingLines[j].end)) {

					Bullet.Builder bulletBuilder1 = bulletBuilders[i];
					Bullet.Builder bulletBuilder2 = bulletBuilders[j];

					Bullet bullet1 = bulletBuilder1.build();
					Bullet bullet2 = bulletBuilder2.build();

					BulletHitBulletEvent bulletHitBulletEvent1 = new BulletHitBulletEvent(bullet1, bullet2);
					turnBuilder.addBotEvent(bullet1.getBotId(), bulletHitBulletEvent1);

					BulletHitBulletEvent bulletHitBulletEvent2 = new BulletHitBulletEvent(bullet2, bullet1);
					turnBuilder.addBotEvent(bullet2.getBotId(), bulletHitBulletEvent2);

					// Observers only need a single event
					turnBuilder.addObserverEvent(bulletHitBulletEvent1);

					// Remove bullets from the arena
					bulletStateSet.remove(bulletBuilder1);
					bulletStateSet.remove(bulletBuilder2);
				}
			}
		}
	}

	private static final double BULLET_BOUNDING_CIRCLE_DIAMETER = 2 * MAX_BULLET_SPEED;
	private static final double BULLET_BOUNDING_CIRCLE_DIAMETER_SQUARED = BULLET_BOUNDING_CIRCLE_DIAMETER
			* BULLET_BOUNDING_CIRCLE_DIAMETER;

	private static boolean isBulletsBoundingCirclesColliding(Position bullet1Position, Position bullet2Position) {
		double dx = bullet2Position.x - bullet1Position.x;
		if (Math.abs(dx) > BULLET_BOUNDING_CIRCLE_DIAMETER) {
			return false;
		}
		double dy = bullet2Position.y - bullet1Position.y;
		if (Math.abs(dy) > BULLET_BOUNDING_CIRCLE_DIAMETER) {
			return false;
		}
		return ((dx * dx) + (dy * dy) <= BULLET_BOUNDING_CIRCLE_DIAMETER_SQUARED);
	}

	private void checkBotToBotCollisions() {

		Position[] positions = new Position[botStateMap.size()];

		Bot.Builder[] botBuilders = new Bot.Builder[botStateMap.size()];
		botBuilders = botStateMap.values().toArray(botBuilders);

		for (int i = positions.length - 1; i >= 0; i--) {
			positions[i] = botBuilders[i].getPosition();
		}

		for (int i = positions.length - 1; i >= 0; i--) {
			Position pos1 = botBuilders[i].getPosition();

			for (int j = i - 1; j >= 0; j--) {
				Position pos2 = botBuilders[i].getPosition();

				if (isBotsBoundingCirclesColliding(pos1, pos2)) {
					Bot.Builder botBuilder1 = botBuilders[i];
					Bot.Builder botBuilder2 = botBuilders[j];

					int botId1 = botBuilder1.getId();
					int botId2 = botBuilder2.getId();

					boolean bot1Killed = botBuilder1.addDamage(RAM_DAMAGE);
					boolean bot2Killed = botBuilder2.addDamage(RAM_DAMAGE);

					boolean bot1Rammed = isRamming(botBuilder2, botBuilder1);
					boolean bot2Rammed = isRamming(botBuilder1, botBuilder2);

					double bot1BounceDist = 0;
					double bot2BounceDist = 0;

					if (bot1Rammed) {
						bot2BounceDist = MathUtil.distance(pos1, pos2);
						scoreKeeper.addRamHit(botId2, botId1, RAM_DAMAGE, bot1Killed);
					}
					if (bot2Rammed) {
						bot1BounceDist = MathUtil.distance(pos2, pos1);
						scoreKeeper.addRamHit(botId1, botId2, RAM_DAMAGE, bot2Killed);
					}
					if (bot1Rammed && bot2Rammed) {
						bot1BounceDist /= 2;
						bot2BounceDist /= 2;
					}
					botBuilder1.bounceBackPosition(bot1BounceDist);
					botBuilder2.bounceBackPosition(bot2BounceDist);

					pos1 = botBuilder1.getPosition();
					pos2 = botBuilder2.getPosition();

					BotHitBotEvent BotHitBotEvent1 = new BotHitBotEvent(botId1, botId2, botBuilder2.getEnergy(),
							botBuilder2.getPosition(), bot2Rammed);
					BotHitBotEvent BotHitBotEvent2 = new BotHitBotEvent(botId2, botId1, botBuilder1.getEnergy(),
							botBuilder1.getPosition(), bot1Rammed);

					turnBuilder.addBotEvent(botId1, BotHitBotEvent1);
					turnBuilder.addBotEvent(botId2, BotHitBotEvent2);

					turnBuilder.addObserverEvent(BotHitBotEvent1);
					turnBuilder.addObserverEvent(BotHitBotEvent2);
				}
			}
		}
	}

	private static final double BOT_BOUNDING_CIRCLE_DIAMETER_SQUARED = BOT_BOUNDING_CIRCLE_DIAMETER
			* BOT_BOUNDING_CIRCLE_DIAMETER;

	private static boolean isBotsBoundingCirclesColliding(Position bot1Position, Position bot2Position) {
		double dx = bot2Position.x - bot1Position.x;
		if (Math.abs(dx) > BOT_BOUNDING_CIRCLE_DIAMETER) {
			return false;
		}
		double dy = bot2Position.y - bot1Position.y;
		if (Math.abs(dy) > BOT_BOUNDING_CIRCLE_DIAMETER) {
			return false;
		}
		return ((dx * dx) + (dy * dy) <= BOT_BOUNDING_CIRCLE_DIAMETER_SQUARED);
	}

	private static boolean isRamming(ImmutableBot bot, ImmutableBot victim) {

		double dx = victim.getPosition().x - bot.getPosition().x;
		double dy = victim.getPosition().y - bot.getPosition().y;

		double angle = Math.atan2(dx, dy);

		double bearing = MathUtil.normalRelativeAngleDegrees(Math.toDegrees(angle) - bot.getDirection());

		return ((bot.getSpeed() > 0 && (bearing > -90 && bearing < 90))
				|| (bot.getSpeed() < 0 && (bearing < -90 || bearing > 90)));
	}

	private void updateBulletPositions() {
		for (Bullet.Builder state : bulletStateSet) {
			state.incrementTick(); // The tick is used to calculate new position by calling getPosition()
		}
	}

	private void checkBotWallCollisions() {
		for (Bot.Builder bot : botStateMap.values()) {
			Position position = bot.getPosition();
			double x = position.x;
			double y = position.x;

			boolean hitWall = false;

			if (x - BOT_BOUNDING_CIRCLE_RADIUS <= 0) {
				x = BOT_BOUNDING_CIRCLE_RADIUS;
				hitWall = true;
			} else if (x + BOT_BOUNDING_CIRCLE_RADIUS >= setup.getArenaWidth()) {
				x = setup.getArenaWidth() - BOT_BOUNDING_CIRCLE_RADIUS;
				hitWall = true;
			} else if (y - BOT_BOUNDING_CIRCLE_RADIUS <= 0) {
				y = BOT_BOUNDING_CIRCLE_RADIUS;
				hitWall = true;
			} else if (y + BOT_BOUNDING_CIRCLE_RADIUS >= setup.getArenaHeight()) {
				y = setup.getArenaHeight() - BOT_BOUNDING_CIRCLE_RADIUS;
				hitWall = true;
			}

			if (hitWall) {
				bot.setPosition(new Position(x, y));

				BotHitWallEvent botHitWallEvent = new BotHitWallEvent(bot.getId());
				turnBuilder.addBotEvent(bot.getId(), botHitWallEvent);
				turnBuilder.addObserverEvent(botHitWallEvent);

				double damage = Physics.calcWallDamage(bot.getSpeed());
				bot.addDamage(damage);
			}
		}
	}

	private void checkBulletWallCollisions() {
		Iterator<Bullet.Builder> iterator = bulletStateSet.iterator(); // due to removal
		while (iterator.hasNext()) {
			Bullet.Builder bullet = iterator.next();
			Position position = bullet.calcPosition();

			if ((position.x <= 0) || (position.x >= setup.getArenaWidth()) || (position.y <= 0)
					|| (position.y >= setup.getArenaHeight())) {

				iterator.remove(); // remove bullet from arena,

				BulletMissedEvent bulletMissedEvent = new BulletMissedEvent(bullet.build());
				turnBuilder.addBotEvent(bullet.getBotId(), bulletMissedEvent);
				turnBuilder.addObserverEvent(bulletMissedEvent);
			}
		}
	}

	private void fireGuns() {
		for (Integer botId : botStateMap.keySet()) {
			BotIntent intent = botIntentMap.get(botId);
			Bot.Builder bot = botStateMap.get(botId);

			// Fire gun, if the gun heat is zero
			double gunHeat = bot.getGunHeat();
			gunHeat = Math.max(gunHeat - setup.getGunCoolingRate(), 0);

			if (gunHeat == 0) {
				// Gun can fire. Check if gun must be fired by intent
				double firepower = intent.getBulletPower();
				if (firepower >= MIN_BULLET_POWER) {
					// Gun is fired
					firepower = Math.min(firepower, MAX_BULLET_POWER);
					handleFiredBullet(bot, firepower);
				}
			}
		}
	}

	private void handleFiredBullet(Bot.Builder botBuilder, double firepower) {
		int botId = botBuilder.getId();

		double gunHeat = calcGunHeat(firepower);
		botBuilder.setGunHeat(gunHeat);

		Bullet.Builder builder = new Bullet.Builder();
		builder.setBotId(botId);
		builder.setBulletId(++nextBulletId);
		builder.setPower(firepower);
		builder.setFirePosition(botBuilder.getPosition());
		builder.setDirection(botBuilder.getGunDirection());
		builder.setSpeed(calcBulletSpeed(firepower));

		Bullet bullet = builder.build();

		turnBuilder.addBullet(bullet);

		BulletFiredEvent bulletFiredEvent = new BulletFiredEvent(bullet);
		turnBuilder.addBotEvent(botId, bulletFiredEvent);
		turnBuilder.addObserverEvent(bulletFiredEvent);
	}

	private static double randomDirection() {
		return Math.random() * 360;
	}

	private class Line {
		Position start;
		Position end;
	}

	public static void main(String[] args) {

		// Setup setup = new Setup("gameType", 200, 100, 0, 0, 0, new HashSet<Integer>(Arrays.asList(1, 2)));
		//
		// ModelUpdater updater = new ModelUpdater(setup);
		// updater.initialBotStates();

		// System.out.println("#0: " + computeNewSpeed(0, 0));
		//
		// System.out.println("#1: " + computeNewSpeed(1, 10));
		// System.out.println("#2: " + computeNewSpeed(8, 10));
		//
		// System.out.println("#3: " + computeNewSpeed(1, 1.5));
		// System.out.println("#4: " + computeNewSpeed(0, 0.3));
		//
		// System.out.println("#5: " + computeNewSpeed(8, 0));
		// System.out.println("#6: " + computeNewSpeed(7.5, -3));
		//
		// System.out.println("#7: " + computeNewSpeed(8, -8));
		//
		// System.out.println("#-1: " + computeNewSpeed(-1, -10));
		// System.out.println("#-2: " + computeNewSpeed(-8, -10));
		//
		// System.out.println("#-3: " + computeNewSpeed(-1, -1.5));
		// System.out.println("#-4: " + computeNewSpeed(0, -0.3));
		//
		// System.out.println("#-5: " + computeNewSpeed(-8, 0));
		// System.out.println("#-6: " + computeNewSpeed(-7.5, 3));
		//
		// System.out.println("#-7: " + computeNewSpeed(-8, 8));
	}
}
