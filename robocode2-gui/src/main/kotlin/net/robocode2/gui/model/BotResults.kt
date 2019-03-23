package net.robocode2.gui.model

import net.robocode2.gui.model.Content
import net.robocode2.gui.model.ContentType

class BotResults(
        id: Int,
        rank: Int,
        survival: Int,
        lastSurvivorBonus: Int,
        bulletDamage: Int,
        bulletKillBonus: Int,
        ramDamage: Int,
        ramKillBonus: Int,
        totalScore: Int,
        firstPlaces: Int,
        secondPlaces: Int,
        thirdPlaces: Int
) : Content(type = ContentType.BOT_RESULTS.type)