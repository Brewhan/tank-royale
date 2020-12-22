package dev.robocode.tankroyale.server.model

/**
 * Defines an immutable 2D point.
 * @property x is the x coordinate.
 * @property y is the y coordinate.
 */
data class Point(override val x: Double, override val y: Double) : IPoint {
    /**
     * Returns a mutable copy of this point
     *
     * @return a MutablePoint that is a copy of this point.
     */
    fun toMutablePoint() = MutablePoint(x, y)
}