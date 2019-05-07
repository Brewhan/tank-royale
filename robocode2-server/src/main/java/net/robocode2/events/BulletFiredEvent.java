package net.robocode2.events;

import lombok.Value;
import net.robocode2.model.Bullet;

/**
 * Event sent when a bullet has fired a bullet.
 * 
 * @author Flemming N. Larsen
 */
@Value
public class BulletFiredEvent implements Event {

	/** Turn number when event occurred */
	int turnNumber;

	/** Fired bullet */
	Bullet bullet;
}