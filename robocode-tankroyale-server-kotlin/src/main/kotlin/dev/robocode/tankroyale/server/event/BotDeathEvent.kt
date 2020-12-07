package dev.robocode.tankroyale.server.event

/** Event sent when a bot has been killed. */
data class BotDeathEvent(
    /** Turn number when event occurred */
    override val turnNumber: Int,

    /** Bot id of the victim that got killed */
    val victimId: BotId,

) : Event()
