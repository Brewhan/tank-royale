package net.robocode2.server;

import org.java_websocket.WebSocket;

import net.robocode2.json_schema.messages.ObserverHandshake;

public final class ObserverConn {

	private final WebSocket connection;
	private final ObserverHandshake handshake;

	public ObserverConn(WebSocket connection, ObserverHandshake handshake) {
		this.connection = connection;
		this.handshake = handshake;
	}

	public WebSocket getConnection() {
		return connection;
	}

	public ObserverHandshake getHandshake() {
		return handshake;
	}
}