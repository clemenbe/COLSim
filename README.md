# Multiagent USV Simulator

## Contributors 
**2023**
- Marie Dubromel  <marie.dubromel@ensta-bretagne.org> (Promotion ENSTA Bretagne 2024 - Spécialité Robotique Autonome)
- Peter Wu <peterzikangwu@gmail.com>

**2024**
- Tiphaine Calvier-Moisson  <tiphaine.calvier-moisson@ensta-bretagne.org> (Promotion ENSTA Bretagne 2025 - Spécialité Robotique Autonome)

**Supervison:** 
Benoit Clement




## Summary
1. [Project Goals](#project-goals) 
2. [Existing Simulators](#existing-simulators)
3. [Versions of the USV Simulator](#versions-of-the-usv-simulator)


## Project Goals

This project present a new USV simulator implemented in Python, with a collision avoidance system on every USV, that adheres to the COLREGs. With this simulator, several research could then use it to train an AI using historical AIS-based simulations of real-world scenarios.
Therefore, the goal is to have a simple simulation so that it can be run a great number of times and learn from each simulation.

Old boat scenes from AIS data can be simulated, but also fictive boats. All the boats should adapt their trajectory to the new added boats.

The decision making module should have a basic implementation of obeying the rules of the sea (COLREGs).


## Existing Simulators

### The Python Vehicle Simulator
The [Python Vehicle Simulator](https://www.fossen.biz/wiley/pythonVehicleSim.php) is designed to simulate the **behavior** of **different types of vehicles** in a **3D simulation** environment. It takes into account different simulation parameters such as **gravity, friction, air resistance**, and **vehicle dynamics** to simulate the movement and behavior of vehicles in real-time. Users can adjust simulation parameters to represent different types of vehicles and environments.

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



## Versions of the USV Simulator

### Librairies
We created three .py files to use as librairies : **_calcul_tools, draw_** and **_potential_fields_**

### main_program
This is the most up-to-date version of the simulator and allows to runned a simualtion with fictive USV that the user can choose to initialise.
It includes the following key components:

- `SimulationRunner` : Initializes all objects and constants for the simulation like **Ship**, **Whale**, repulsive force, etc.
- `Simulation` : Runs the whole simulation in a for loop, depended on the number of steps chosen. It accepts the sea_objects vector which includes different objects of **SeaObject**, **Ship**, **Whale**, **Island** classes, and calls each of them's *move* and *draw* in each matplotlib iteration.
- `SeaObject` : The parent class for all sea objects including **Boat**, **Ship**, **Whale**, **Island** etc. It defines each sea object with x, y, v, theta, and defines an *update* and *get_state_vector* function, contains the *move* function that checks the distance with other sea objects and *avoid_collision* based on certain conditions. It also includes a *draw* function so that each child class can draw its own image. For more information on how the main_program version works, see the [README in the main_program directory](./main_program/README.md).

It can be runned in two different ways : 
- [ ] The simulation with the scene **displayed**
- [ ] The simulation runned without any display, but with the USV's following information : **MMSI number, x, y, theta, v** saved in a .csv file


### AIS
This version allows this time to run a simulation based on AIS data, so of an past real scene.
For more information on how the AIS version works, see the [README in the AIS directory](./AIS/README.md).

### AIS_new
This version is the implementation of a new solution to run a simulation based on AIS data. The implementation is not done yet.
For more information on how the AIS_new version works, see the [README in the AIS_new directory](./AIS new/README.md).



For a detailed explanation of how the different classes, function and other specific notions interact with one another, please refer to the comments in the source code. The simulator offers the possibility of simulating different sea conditions and object interactions, which makes it a versatile tool for researching and studying marine navigation and collision avoidance systems.

