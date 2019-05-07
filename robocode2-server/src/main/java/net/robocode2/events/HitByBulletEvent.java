package net.robocode2.events;

import lombok.Value;
import net.robocode2.model.Bullet;

/**
 * Event sent when a bot is hit by a bullet.
 * 
 * @author Flemming N. Larsen
 */
@Value
public class HitByBulletEvent implements Event {

	/** Turn number when event occurred */
	int turnNumber;

	/** Bullet that hit the bot */
	Bullet bullet;

	/** Damage dealt to the bot */
	double damage;

	/** New energy level of the bot after damage */
	double energy;
}