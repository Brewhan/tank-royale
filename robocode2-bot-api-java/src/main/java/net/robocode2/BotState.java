package net.robocode2;

import lombok.Builder;
import lombok.Value;

/** Current bot state */
@Value
@Builder
public class BotState {
  /** Energy level */
  double energy;
  /** X coordinate */
  double x;
  /** Y coordinate */
  double y;
  /** Driving direction in degrees */
  double direction;
  /** Gun direction in degrees */
  double gunDirection;
  /** Radar direction in degrees */
  double radarDirection;
  /** Radar sweep angle in degrees, i.e. angle between old and current direction */
  double radarSweep;
  /** Speed measured in pixels per turn */
  double speed;
}