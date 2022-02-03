import dev.robocode.tankroyale.botapi.*;
import dev.robocode.tankroyale.botapi.events.*;

import java.io.IOException;

// ------------------------------------------------------------------
// Target
// ------------------------------------------------------------------
// A sample bot original made for Robocode by Mathew Nelson.
// Ported to Robocode Tank Royale by Flemming N. Larsen.
//
// Sits still. Moves every time energy drops by 20.
// This Robot demonstrates custom events.
// ------------------------------------------------------------------
public class Target extends Bot {

    int trigger; // Keeps track of when to move

    // The main method starts our bot
    public static void main(String[] args) throws IOException {
        new Target().start();
    }

    // Constructor, which loads the bot config file
    protected Target() throws IOException {
        super(BotInfo.fromFile("/Target.json"));
    }

    // Called when a new round is started -> initialize and do movement
    @Override
    public void run() {
        // Set colors
        setBodyColor("#FFF"); // white
        setTurretColor("#FFF"); // white
        setRadarColor("#FFF"); // white

        // Initially, we'll move when energy passes 80
        trigger = 80;

        // Add a custom event named "trigger-hit"
        addCustomEvent(
                new Condition("trigger-hit") {
                    public boolean test() {
                        return getEnergy() <= trigger;
                    }
                });

        // While loop that prevents bot from exiting the run() method, which would stop the bot
        while (isRunning()) {
            go(); // just call go() to skip turn doing nothing
        }
    }

    // A custom event occurred
    @Override
    public void onCustomEvent(CustomEvent e) {
        // Check if our custom event "trigger-hit" went off
        if (e.getCondition().getName().equals("trigger-hit")) {
            // Adjust the trigger value, or else the event will fire again and again and again...
            trigger -= 20;

            // Print out energy level
            System.out.println("Ouch, down to " + (int) (getEnergy() + .5) + " energy.");

            // Move around a bit
            turnLeft(65);
            forward(100);
        }
    }
}