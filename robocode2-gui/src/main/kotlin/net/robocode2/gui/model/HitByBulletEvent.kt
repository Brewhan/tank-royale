package net.robocode2.gui.model

class HitByBulletEvent(
        val bullet: BulletState,
        val damage: Double,
        val energy: Double
) : Content(type = ContentType.HIT_BY_BULLET_EVENT.type)