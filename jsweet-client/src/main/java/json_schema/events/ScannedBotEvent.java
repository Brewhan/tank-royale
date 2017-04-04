package json_schema.events;

import static def.jquery.Globals.$;

import json_schema.types.Point;

public final class ScannedBotEvent extends Event {

	public static final String TYPE = "scanned-bot-event";

	public ScannedBotEvent() {
		super(TYPE);
	}

	public Integer getScannedByBotId() {
		return (Integer) $get("scanned-by-bot-id");
	}

	public Integer getScannedBotId() {
		return (Integer) $get("scanned-bot-id");
	}

	public Double getEnergy() {
		return (Double) $get("energy");
	}

	public Point getPosition() {
		return (Point) $.extend(false, new Point(), $get("position"));
	}

	public Double getDirection() {
		return (Double) $get("direction");
	}

	public Double getSpeed() {
		return (Double) $get("speed");
	}
}