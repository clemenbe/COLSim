# Main Program of USV Simulator

This directory contains the most up-to-date and comprehensive version of the USV simulator. It introduces a more sophisticated structure for the simulation of sea objects, featuring the following key classes:

- `SimulationRunner`: This class is responsible for initializing all objects and constants for the simulation. This includes objects such as `Ship`, `Whale`, and constants like repulsive force.

- `Simulation`: This class is tasked with running the simulation. It accepts the `sea_objects` vector, which includes various objects derived from the `SeaObject` class. In each iteration of the simulation, it calls each object's `move()` and `draw()` methods.

- `SeaObject`: This is the parent class for all sea objects (`Boat`, `Ship`, `Whale`, `Island` etc.). It contains critical methods such as `move()`, which checks the distance with other sea objects and applies collision avoidance logic based on certain conditions.

Each object in the simulation follows a set of behaviors as defined by their associated methods. For instance, during a simulation run, the `move()` method of each `SeaObject` is called. The `move()` method checks the distance of the object from other objects and applies logic to avoid collisions.

For a detailed explanation of how these classes function and interact with one another, please refer to the comments in the source code. 

The simulator offers the possibility of simulating different sea conditions and object interactions, which makes it a versatile tool for researching and studying marine navigation and collision avoidance systems.

