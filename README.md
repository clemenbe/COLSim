# USV Simulator

## Author
- DUBROMEL Marie  <marie.dubromel@ensta-bretagne.org> (Promotion ENSTA Bretagne 2024 - Spécialité Robotique Autonome)]
- Peter Wu <peterzikangwu@gmail.com>



## Summary
1. [Project Goals](#project-goals) 
2. [Existing Simulators](#existing-simulators)
3. [Ideas for the new simulator](#ideas-for-the-new-simulator)
4. [Versions of the USV Simulator](#versions-of-the-usv-simulator)


## Project Goals

This project present a new USV simulator using and merging two existing simulators in order to have an anti-collision system.
The goal is to have a simple simulation so that it can be run a great number of times and learn from each simulation.

In the simulation, we should be able to simulate old boat scenes from AIS data, and add to these scenes a new boat. All the boats should adapt their trajectory to the new added boat.

The decision making module should have a basic implementation of obeying the rules of the sea.


## Existing Simulators

### The Fossen Simulator
The [Python Vehicle Simulator](https://www.fossen.biz/wiley/pythonVehicleSim.php) is designed to simulate the **behavior** of **different types of vehicles** in a **3D simulation** environment. It takes into account different simulation parameters such as **gravity, friction, air resistance**, and **vehicle dynamics** to simulate the movement and behavior of vehicles in real-time. Users can adjust simulation parameters to represent different types of vehicles and environments.
Each vehicle is modeled as an object in Python and the vehicle class has methods for guidance, navigation and control. The main program main.py is used to define vehicle objects for real-time simulation.

**Pros :**
- good dynamic modelisation

**Cons :**
- does not take into account the concept of collision with other boats, maybe too precise ? 
- Time of execution too long if many simulations ?



### The UTSeaSim Simulator

The [UTSeaSim simulator](https://www.cs.utexas.edu/~UTSeaSim/download/1.0/Oct2013Documentation.pdf) is a multi-agent simulation environment for underwater robotics research. It allows users to **simulate underwater vehicles** and their **interactions with the environment**, as well as **communication between vehicles and with a surface station**.
The simulation environment includes several modules, such as a **physics engine, a sensor module, a communication module**, and a **behavior module**. The physics engine simulates the dynamics and kinematics of the underwater vehicles, while the sensor module simulates various sensors such as sonar and vision sensors. The communication module simulates acoustic and radio communication between vehicles and with the surface station. The behavior module is responsible for controlling the behavior of the vehicles in the simulation.

The simulator also includes a **graphical user interface (GUI)** for visualizing the simulation, controlling the simulation parameters, and monitoring the behavior of the vehicles. Users can interact with the GUI to create and modify scenarios, as well as to run simulations and analyze the results. → interesting for the new simulator

Overall, the UTSeaSim simulator uses an RRT algorithm to avoid obstacle.

**Pros :**
- have a GUI window (choice in the command-line flag) → useful for users 
- speed of simulation controllable

**Cons :**
- limited use to the rules of the sea
- the robot will follow approximately the RRT path, so if the obstacle is to close, it might collides





## Ideas for the new simulator
- [ ] regrouping the different types of boat in python Classes (work with those described in fossen simu)
- [ ] artificial potential fields ? → potential based method to find a good controller (if they can see each other but can’t communicate)
- [ ] coupled to a path planning method



## Versions of the USV Simulator

### main_program
This is the most up-to-date version of the simulator and includes the following key components:

- [ ] **SimulationRunner** : Initializes all objects and constants for the simulation like **Ship**, **Whale**, repulsive force, etc.
- [ ] **Simulation** : Runs the whole simulation in a for loop, depended on the number of steps chosen. It accepts the sea_objects vector which includes different objects of **SeaObject**, **Ship**, **Whale**, **Island** classes, and calls each of them's *move* and *draw* in each matplotlib iteration.
- [ ] **SeaObject** : The parent class for all sea objects including **Boat**, **Ship**, **Whale**, **Island** etc. It defines each sea object with x, y, v, theta, and defines an *update* and *get_state_vector* function, contains the *move* function that checks the distance with other sea objects and *avoid_collision* based on certain conditions. It also includes a *draw* function so that each child class can draw its own image. For more information on how the main_program version works, see the [README in the main_program directory](./main_program/README.md).

### matplot_version
This is the first version of the USV Simulator, using matlab to display the simulation.
With those codes, you will be able to simulate two boats, be chosing his position (x and y), his speed v, and his heading/orientation theta.
It is equipped with an avoiding collision system.
We used different classes to create a flexible structure :
- [ ] **Simulation** : run a for loop in the time, depending on the number of steps chosen, applies the avoiding collision system which will atttribute the correct controler for each situation, will update the state vector of the considerated boat, and will display the boats.
- [ ] **Boat** : allow to define each boat with x, y, v, theta, and define an update and get_state_vector fonction

We created three .py files to use as librairies : **_calcul_tools, draw_** and **_potential_fields_**

### cross_path_version
This version of the simulator addresses scenarios where a **Ship** moves northwards and another **Ship** or **SeaObject** moves beneath it. In the current system, the moving **Ship** would detect the collision zone and attempt to avoid the **Ship** moving beneath by also moving northwards. This leads to inefficiency and safety issues as the **Ship** deviates from its original path. This version aims to improve the pathing logic to enable the **Ship** to maintain its original path if it's safe to do so.

### map_version

This version is a future concept where a background map would be inputted to the simulator. This would allow for more realistic simulations as the map could represent different sea conditions, the presence of islands, and other features. This could provide the **SeaObject** objects with a richer context and allow for more complex and realistic simulations.

