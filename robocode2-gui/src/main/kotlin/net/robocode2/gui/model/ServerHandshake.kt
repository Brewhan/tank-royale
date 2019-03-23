package net.robocode2.gui.model

class ServerHandshake(
        clientKey: String,
        val protocolVersion: String,
        val games: Set<GameSetup>
) : ClientContent(type = ContentType.SERVER_HANDSHAKE.type, clientKey = clientKey)