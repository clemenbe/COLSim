This simulator was implemented taking the main_program as a base. It keeps the same format while adding new features.

# Main Program of USV Simulator

This directory contains the most up-to-date and comprehensive version of the USV simulator. It introduces a more sophisticated structure for the simulation of sea objects. The main components are:

- `SimulationRunner`: This class is responsible for initializing all objects and constants for the simulation.

- `Simulation`: This class is tasked with running the simulation. 

- `SeaObject`: This is the parent class for all sea objects (`Boat`, `Ship`, `Whale`, `Island` etc.).

## SimulationRunner

In `SimulationRunner`, several key constants are initialized, such as `s`, `dt`, `k`, `num_steps`. A separate `RuleApplicationWindow` is also initialized to display the rules of collision avoidance at sea. 

A function called `initialize_sea_objects()` creates various sea objects (`Boat`, `Ship`, `Whale`, `Island` etc.). These objects are initialized with parameters such as `x`, `y`, `v`, and `theta`, then added to the `sea_objects` vector. 

The `run()` function then takes this `sea_objects` vector and the `RuleApplicationWindow`, and passes them to the `Simulation`.

## Simulation

`Simulation` accepts the `sea_objects` vector and runs the simulation. During each iteration, it calls the `move()` and `draw()` methods for each object in the `sea_objects` vector.

## SeaObject

Each time the `move()` method is called for a `SeaObject`, the `in_collision` variable is set to `False`, indicating that the object is not currently in collision with another. 

The `move()` method then loops over every other object in the `sea_objects` vector and calculates the distance between the current object and every other object. If the distance is smaller than the maximum radius of the two objects (this is to account for the fact that different objects might have different collision radii), the privilege of the two objects is compared.

If the current object has a lower privilege, it needs to avoid collision. In this case, the `avoid_collision()` function is called and `in_collision` is set to `True`. If the current object has a higher privilege, it does not need to do anything and ignores the potential collision. If the distance is larger than the collision radius, the current object also does not need to do anything.

The `move_straight()` function is called when the `SeaObject` either is not in collision with any other objects, or is in collision but has higher privilege. This function instructs the object to continue on its initial path. 

Whether an object moves straight or avoids collision, both actions return a control vector (`up`), which is then passed to the `update()` function to update the object's position. The `draw()` function is then called by `Simulation` to draw the new position of the object. This process repeats in each iteration of the simulation.

In this manner, each sea object is responsible for its own actions, deciding whether to avoid collision or not, based on the rules defined in its methods. The object does not care about the reactions of others, ensuring each object makes decisions autonomously.

For a detailed explanation of how these classes function and interact with one another, please refer to the comments in the source code. 


# Different algorithms

For each maneuverable **SeaObject**, an algorithm must be chosen at initialization. 
Available algorithms are "APF", "A*", "D*Lite", "ACO" and "PSO".
The algorithms are coded in their own file and implemented for the simulator in the [sea_object.py](./sea_object.py) file.

Algorithms already implemented are
- Artificial potential fields [here](./algo_potential_fields.py): initially present in the simulator, works well with mutiple objects if there is non "wall" obstacles.
- A* [here](./algo_astar.py): two differents versions selected online. It's a Dijkstra algorithm with heuristics
- D* Lite [here](./algo_dstar_lite.py): amelioration of A*.
- Ant Colony Optimisation [here](./algo_aco.py)
- Particle Swarm Optimisation [here](./algo_pso.py)


## Algorithm comparison

The [compare_algo.py](./compare_algo.py) file compare the algorithms based on multiple factors.

For the first iteration (static), it compares the time to find a path and the number of times the main loop of the programm is played.

Another function calculate the length of a path taken by a sea object to reach it's goal and compare them.  
To use it, first run the simulator with `self.record_data` set to True (in [simulation_runner.py](./simulation_runner.py)) then use the function `calculate_dist()` to compute the length of the path.

The [compare_pso.py](./compare_pso.py) file compare the results of PSO with different parameters.

Giving up on compare_energy or memory at the moment because of the configuration of the computer use.