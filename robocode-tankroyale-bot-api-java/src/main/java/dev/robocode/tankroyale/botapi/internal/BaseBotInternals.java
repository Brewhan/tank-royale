package dev.robocode.tankroyale.botapi.internal;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.typeadapters.RuntimeTypeAdapterFactory;
import com.neovisionaries.ws.client.*;
import dev.robocode.tankroyale.botapi.*;
import dev.robocode.tankroyale.botapi.GameSetup;
import dev.robocode.tankroyale.botapi.events.BulletFiredEvent;
import dev.robocode.tankroyale.botapi.events.SkippedTurnEvent;
import dev.robocode.tankroyale.botapi.events.*;
import dev.robocode.tankroyale.botapi.mapper.EventMapper;
import dev.robocode.tankroyale.botapi.mapper.GameSetupMapper;
import dev.robocode.tankroyale.botapi.mapper.ResultsMapper;
import dev.robocode.tankroyale.schema.*;

import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import static java.lang.Math.max;
import static java.lang.Math.min;

public final class BaseBotInternals {
  private static final String SERVER_URL_PROPERTY_KEY = "server.url";

  private static final String NOT_CONNECTED_TO_SERVER_MSG =
      "Not connected to game server yes. Make sure onConnected() event handler has been called first";

  private static final String GAME_NOT_RUNNING_MSG =
      "Game is not running. Make sure onGameStarted() event handler has been called first";

  private static final String TICK_NOT_AVAILABLE_MSG =
      "Game is not running or tick has not occurred yet. Make sure onTick() event handler has been called first";

  private final Gson gson;

  {
    RuntimeTypeAdapterFactory<dev.robocode.tankroyale.schema.Event> typeFactory =
        RuntimeTypeAdapterFactory.of(dev.robocode.tankroyale.schema.Event.class, "$type")
            .registerSubtype(dev.robocode.tankroyale.schema.BotDeathEvent.class, "BotDeathEvent")
            .registerSubtype(dev.robocode.tankroyale.schema.BotHitBotEvent.class, "BotHitBotEvent")
            .registerSubtype(
                dev.robocode.tankroyale.schema.BotHitWallEvent.class, "BotHitWallEvent")
            .registerSubtype(
                dev.robocode.tankroyale.schema.BulletFiredEvent.class, "BulletFiredEvent")
            .registerSubtype(
                dev.robocode.tankroyale.schema.BulletHitBotEvent.class, "BulletHitBotEvent")
            .registerSubtype(
                dev.robocode.tankroyale.schema.BulletHitBulletEvent.class, "BulletHitBulletEvent")
            .registerSubtype(
                dev.robocode.tankroyale.schema.BulletHitWallEvent.class, "BulletHitWallEvent")
            .registerSubtype(
                dev.robocode.tankroyale.schema.ScannedBotEvent.class, "ScannedBotEvent")
            .registerSubtype(dev.robocode.tankroyale.schema.WonRoundEvent.class, "WonRoundEvent");

    gson = new GsonBuilder().registerTypeAdapterFactory(typeFactory).create();
  }

  private final double absDeceleration = Math.abs(IBot.DECELERATION);

  private final IBaseBot baseBot;
  private final dev.robocode.tankroyale.botapi.BotInfo botInfo;
  private final BotEventHandlers botEventHandlers;
  private final EventQueue eventQueue;
  private final Set<Condition> conditions = new HashSet<>();

  private BotIntent botIntent = newBotIntent();

  // Server connection:
  private WebSocket socket;
  private ServerHandshake serverHandshake;

  // Current game states:
  private Integer myId;
  private dev.robocode.tankroyale.botapi.GameSetup gameSetup;
  private TickEvent tickEvent;
  private Long tickStartNanoTime;

  // Maximum speed and turn rates
  private double maxSpeed = IBot.MAX_SPEED;
  private double maxTurnRate = IBot.MAX_TURN_RATE;
  private double maxGunTurnRate = IBot.MAX_GUN_TURN_RATE;
  private double maxRadarTurnRate = IBot.MAX_RADAR_TURN_RATE;

  public BaseBotInternals(
      IBaseBot baseBot, dev.robocode.tankroyale.botapi.BotInfo botInfo, URI serverUrl) {
    this.baseBot = baseBot;
    this.botInfo = (botInfo == null) ? EnvVars.getBotInfo() : botInfo;

    this.botEventHandlers = new BotEventHandlers(baseBot);
    this.eventQueue = new EventQueue(this, botEventHandlers);

    init(serverUrl == null ? getServerUrlFromSetting() : serverUrl);
  }

  private void init(URI serverUrl) {
    try {
      socket = new WebSocketFactory().createSocket(serverUrl);
    } catch (IOException ex) {
      throw new BotException("Could not create socket for URL: " + serverUrl, ex);
    }
    socket.addListener(new WebSocketListener());

    botEventHandlers.onNewRound.subscribe(this::handleNewRound, 100);
    botEventHandlers.onBulletFired.subscribe(this::handleBulletFired, 100);
  }

  private BotIntent newBotIntent() {
    BotIntent botIntent = new BotIntent();
    botIntent.set$type(BotReady.$type.BOT_INTENT); // must be set!
    return botIntent;
  }

  public void connect() {
    if (!socket.isOpen()) {
      try {
        socket.connect();
      } catch (WebSocketException ex) {
        throw new BotException(
            "Could not connect to web socket: "
                + socket.getURI()
                + ". Setup "
                + EnvVars.SERVER_URL
                + " to point to a server that is up and running.",
            ex);
      }
    }
  }

  public BotEventHandlers getBotEventHandlers() {
    return botEventHandlers;
  }

  public Set<Condition> getConditions() {
    return conditions;
  }

  public void addCondition(Condition condition) {
    conditions.add(condition);
  }

  public void removeCondition(Condition condition) {
    conditions.remove(condition);
  }

  public void execute() {
    // Send the bot intent to the server
    sendIntent();
    botIntent.setScan(false);

    // Dispatch all bot events
    new Thread(() -> eventQueue.dispatchEvents(baseBot, getCurrentTick().getTurnNumber())).start();
  }

  private void sendIntent() {
    if (botIntent.getTargetSpeed() > maxSpeed) {
      botIntent.setTargetSpeed(maxSpeed);
    }
    if (botIntent.getTurnRate() > maxTurnRate) {
      botIntent.setTurnRate(maxTurnRate);
    }
    if (botIntent.getGunTurnRate() > maxGunTurnRate) {
      botIntent.setGunTurnRate(maxGunTurnRate);
    }
    if (botIntent.getRadarTurnRate() > maxRadarTurnRate) {
      botIntent.setRadarTurnRate(maxRadarTurnRate);
    }
    socket.sendText(gson.toJson(botIntent));
  }

  private void clearCurrentGameState() {
    // Clear setting that are only available during a running game
    tickEvent = null;
    gameSetup = null;
    myId = null;
  }

  private URI getServerUrlFromSetting() {
    String url = EnvVars.getServerUrl();
    if (url == null) {
      url = System.getProperty(SERVER_URL_PROPERTY_KEY);
      if (url == null) {
        url = EnvVars.getServerUrl();
      }
    }
    if (url == null) {
      url = "ws://localhost";
    }
    try {
      return new URI(url);
    } catch (URISyntaxException ex) {
      throw new BotException("Incorrect syntax for server URL: " + url);
    }
  }

  public String getVariant() {
    return getServerHandshake().getVariant();
  }

  public String getVersion() {
    return getServerHandshake().getVersion();
  }

  private ServerHandshake getServerHandshake() {
    if (serverHandshake == null) {
      throw new BotException(NOT_CONNECTED_TO_SERVER_MSG);
    }
    return serverHandshake;
  }

  public int getMyId() {
    if (myId == null) {
      throw new BotException(GAME_NOT_RUNNING_MSG);
    }
    return myId;
  }

  public GameSetup getGameSetup() {
    if (gameSetup == null) {
      throw new BotException(GAME_NOT_RUNNING_MSG);
    }
    return gameSetup;
  }

  public BotIntent getBotIntent() {
    return botIntent;
  }

  public TickEvent getCurrentTick() {
    if (tickEvent == null) {
      throw new BotException(TICK_NOT_AVAILABLE_MSG);
    }
    return tickEvent;
  }

  private long getTicksStart() {
    if (tickStartNanoTime == null) {
      throw new BotException(TICK_NOT_AVAILABLE_MSG);
    }
    return tickStartNanoTime;
  }

  public int getTimeLeft() {
    long passesMicroSeconds = (System.nanoTime() - getTicksStart()) / 1000;
    return (int) (getGameSetup().getTurnTimeout() - passesMicroSeconds);
  }

  public boolean setFire(double firepower) {
    if (Double.isNaN(firepower)) {
      throw new IllegalArgumentException("firepower cannot be NaN");
    }
    if (getCurrentTick().getBotState().getGunHeat() > 0) {
      return false; // cannot fire yet
    }
    botIntent.setFirepower(firepower);
    return true;
  }

  public void setMaxSpeed(double maxSpeed) {
    if (maxSpeed < 0) {
      maxSpeed = 0;
    } else if (maxSpeed > IBot.MAX_SPEED) {
      maxSpeed = IBot.MAX_SPEED;
    }
    this.maxSpeed = maxSpeed;
  }

  public void setMaxTurnRate(double maxTurnRate) {
    if (maxTurnRate < 0) {
      maxTurnRate = 0;
    } else if (maxTurnRate > IBot.MAX_TURN_RATE) {
      maxTurnRate = IBot.MAX_TURN_RATE;
    }
    this.maxTurnRate = maxTurnRate;
  }

  public void setMaxGunTurnRate(double maxGunTurnRate) {
    if (maxGunTurnRate < 0) {
      maxGunTurnRate = 0;
    } else if (maxGunTurnRate > IBot.MAX_GUN_TURN_RATE) {
      maxGunTurnRate = IBot.MAX_GUN_TURN_RATE;
    }
    this.maxGunTurnRate = maxGunTurnRate;
  }

  public void setMaxRadarTurnRate(double maxRadarTurnRate) {
    if (maxRadarTurnRate < 0) {
      maxRadarTurnRate = 0;
    } else if (maxRadarTurnRate > IBot.MAX_RADAR_TURN_RATE) {
      maxRadarTurnRate = IBot.MAX_RADAR_TURN_RATE;
    }
    this.maxRadarTurnRate = maxRadarTurnRate;
  }

  /**
   * Returns the new speed based on the current speed and distance to move.
   *
   * @param speed is the current speed
   * @param distance is the distance to move
   * @return The new speed
   */
  // Credits for this algorithm goes to Patrick Cupka (aka Voidious),
  // Julian Kent (aka Skilgannon), and Positive:
  // https://robowiki.net/wiki/User:Voidious/Optimal_Velocity#Hijack_2
  public double getNewSpeed(double speed, double distance) {

    if (distance < 0) {
      // If the distance is negative, then change it to be positive and change the sign of the
      // input velocity and the result
      return -getNewSpeed(-speed, -distance);
    }

    final double targetSpeed;
    if (distance == Double.POSITIVE_INFINITY) {
      targetSpeed = maxSpeed;
    } else {
      targetSpeed = min(getMaxSpeed(distance), maxSpeed);
    }

    if (speed >= 0) {
      return max(speed - absDeceleration, min(targetSpeed, speed + IBot.ACCELERATION));
    } // else
    return max(speed - IBot.ACCELERATION, min(targetSpeed, speed + getMaxDeceleration(-speed)));
  }

  private double getMaxSpeed(double distance) {
    double decelTime =
            max(
                    1,
                    Math.ceil( // sum of 0... decelTime, solving for decelTime using quadratic formula
                            (Math.sqrt((4 * 2 / absDeceleration) * distance + 1) - 1) / 2));

    if (decelTime == Double.POSITIVE_INFINITY) {
      return IBot.MAX_SPEED;
    }

    double decelDist =
            (decelTime / 2)
                    * (decelTime - 1) // sum of 0..(decelTime-1)
                    * absDeceleration;

    return ((decelTime - 1) * absDeceleration) + ((distance - decelDist) / decelTime);
  }

  private double getMaxDeceleration(double speed) {
    double decelTime = speed / absDeceleration;
    double accelTime = (1 - decelTime);

    return min(1, decelTime) * absDeceleration + max(0, accelTime) * IBot.ACCELERATION;
  }

  public double getDistanceTraveledUntilStop(double speed) {
    speed = Math.abs(speed);
    double distance = 0;
    while (speed > 0) {
      distance += (speed = getNewSpeed(speed, 0));
    }
    return distance;
  }

  private final class WebSocketListener extends WebSocketAdapter {

    @Override
    public final void onConnected(WebSocket websocket, Map<String, List<String>> headers) {
      botEventHandlers.onConnected.publish(new ConnectedEvent(websocket.getURI()));
    }

    @Override
    public final void onDisconnected(
        WebSocket websocket,
        WebSocketFrame serverCloseFrame,
        WebSocketFrame clientCloseFrame,
        boolean closedByServer) {

      botEventHandlers.onDisconnected.publish(
          new DisconnectedEvent(websocket.getURI(), closedByServer));

      clearCurrentGameState();
    }

    @Override
    public final void onError(WebSocket websocket, WebSocketException cause) {
      botEventHandlers.onConnectionError.publish(
          new ConnectionErrorEvent(websocket.getURI(), cause));
    }

    @Override
    public void onPingFrame(WebSocket websocket, WebSocketFrame frame) {
      // Make sure to send pong as reply to ping in order to stay connected to server
      socket.sendPong();
    }

    @Override
    public final void onTextMessage(WebSocket websocket, String json) {
      JsonObject jsonMsg = gson.fromJson(json, JsonObject.class);

      JsonElement jsonType = jsonMsg.get("$type");
      if (jsonType != null) {
        String type = jsonType.getAsString();

        switch (dev.robocode.tankroyale.schema.Message.$type.fromValue(type)) {
          case TICK_EVENT_FOR_BOT:
            handleTickEvent(jsonMsg);
            break;
          case SERVER_HANDSHAKE:
            handleServerHandshake(jsonMsg);
            break;
          case GAME_STARTED_EVENT_FOR_BOT:
            handleGameStartedEvent(jsonMsg);
            break;
          case GAME_ENDED_EVENT_FOR_BOT:
            handleGameEndedEvent(jsonMsg);
            break;
          case SKIPPED_TURN_EVENT:
            handleSkippedTurnEvent(jsonMsg);
            break;
          default:
            throw new BotException("Unsupported WebSocket message type: " + type);
        }
      }
    }

    private void handleServerHandshake(JsonObject jsonMsg) {
      serverHandshake = gson.fromJson(jsonMsg, ServerHandshake.class);

      // Reply by sending bot handshake
      BotHandshake botHandshake = BotHandshakeFactory.create(botInfo);
      String msg = gson.toJson(botHandshake);

      socket.sendText(msg);
    }

    private void handleGameStartedEvent(JsonObject jsonMsg) {
      GameStartedEventForBot gameStartedEventForBot =
          gson.fromJson(jsonMsg, GameStartedEventForBot.class);

      myId = gameStartedEventForBot.getMyId();
      gameSetup = GameSetupMapper.map(gameStartedEventForBot.getGameSetup());

      // Send ready signal
      BotReady ready = new BotReady();
      ready.set$type(BotReady.$type.BOT_READY);

      String msg = gson.toJson(ready);
      socket.sendText(msg);

      botEventHandlers.onGameStarted.publish(
          new GameStartedEvent(gameStartedEventForBot.getMyId(), gameSetup));
    }
  }

  private void handleGameEndedEvent(JsonObject jsonMsg) {
    // Clear current game state
    clearCurrentGameState();

    // Send the game ended event
    GameEndedEventForBot gameEndedEventForBot = gson.fromJson(jsonMsg, GameEndedEventForBot.class);

    GameEndedEvent gameEndedEvent =
        new GameEndedEvent(
            gameEndedEventForBot.getNumberOfRounds(),
            ResultsMapper.map(gameEndedEventForBot.getResults()));

    botEventHandlers.onGameEnded.publish(gameEndedEvent);
  }

  private void handleSkippedTurnEvent(JsonObject jsonMsg) {
    dev.robocode.tankroyale.schema.SkippedTurnEvent skippedTurnEvent =
        gson.fromJson(jsonMsg, dev.robocode.tankroyale.schema.SkippedTurnEvent.class);

    botEventHandlers.onSkippedTurn.publish((SkippedTurnEvent) EventMapper.map(skippedTurnEvent));
  }

  private void handleTickEvent(JsonObject jsonMsg) {
    TickEventForBot tickEventForBot = gson.fromJson(jsonMsg, TickEventForBot.class);
    tickEvent = EventMapper.map(tickEventForBot);

    tickStartNanoTime = System.nanoTime();

    eventQueue.addEventsFromTick(baseBot, tickEvent);

    if (tickEvent.getTurnNumber() == 1) {
      botEventHandlers.onNewRound.publish(tickEvent);
    }

    botEventHandlers.onProcessTurn.publish(tickEvent);
  }

  private void handleNewRound(TickEvent e) {
    tickEvent = e; // use new bot coordinate, rates and directions etc.
    botIntent = newBotIntent();
    eventQueue.clear();
  }

  private void handleBulletFired(BulletFiredEvent e) {
    botIntent.setFirepower(0d); // Reset firepower so the bot stops firing continuously
  }
}
