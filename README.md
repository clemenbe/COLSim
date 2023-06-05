# USV Simulator

## Author
- DUBROMEL Marie  <marie.dubromel@ensta-bretagne.org> (Promotion ENSTA Bretagne 2024 - Spécialité Robotique Autonome)]



## Summary
1. [Project Goals](#project-goals) 
2. [Existing Simulators](#existing-simulators)
3. [Ideas for the new simulator](#ideas-for-the-new-simulator)
4. [Structure of the USV Simulator](#structure-of-the-usv-simulator)


## Project Goals

This project present a new USV simulator using and merging two existing simulators in order to have an anti-collision system.
The goal is to have a simple simulation so that it can be run a great number of times and learn from each simulation.

In the simulation, we should be able to simulate old boat scenes from AIS data, and add to these scenes a new boat. All the boats should adapt their trajectory to the new added boat.

The decision making module should have a basic implementation of obeying the rules of the sea.


## Existing Simulators

### The Fossen Simulator
The [Fossen Simulator](https://www.fossen.biz/wiley/pythonVehicleSim.php) is designed to simulate the **behavior** of **different types of vehicles** in a **3D simulation** environment. It takes into account different simulation parameters such as **gravity, friction, air resistance**, and **vehicle dynamics** to simulate the movement and behavior of vehicles in real-time. Users can adjust simulation parameters to represent different types of vehicles and environments.
Each vehicle is modeled as an object in Python and the vehicle class has methods for guidance, navigation and control. The main program main.py is used to define vehicle objects for real-time simulation

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



## Structure of the USV Simulator

### main_program

### matplot_version
In this folder, there is a first version of the USV Simulator, using matlab to display the simulation.
With those codes, you will be able to simulate two boats, be chosing his position (x and y), his speed v, and his heading/orientation theta.
It is equipped with an avoiding collision system.
We used different classes to create a flexible structure :
- [ ] **Simulation** : run a for loop in the time, depending on the number of steps chosen, applies the avoiding collision system which will atttribute the correct controler for each situation, will update the state vector of the considerated boat, and will display the boats.
- [ ] **Boat** : allow to define each boat with x, y, v, theta, and define an update and get_state_vector fonction

We created three .py files to use as librairies : **_calcul_tools, draw_** and **_potential_fields_**

### new_version
The New Version is the matplotlib version extended to more than two boats. The structure completely changed. In order to make the avoiding collision system work individually for each boat, it is now located in the **Boat** class :
- [ ] **Simulation** : run a for loop in the time, depending on the number of steps chosen. Route in a loop all boats present in the simulation, where it will call the function *move* form *Boat*, and then the function *draw* to display the simulation. It will also initialize a set where all the boats which has been checked for the risk of collision are gonna be put inside, in the *move* function 
- [ ] **Boat** : allow to define each boat with x, y, v, theta, and define an *update* and *get_state_vector* function, *draw*, the all *avoiding_collision* function (retrun the consign *up* for the considerated boat p), *move_straight* to generate the consign *up* to follow his initial path, and *move* to called every iteration to make the boats move depending on their situation.

### cross_path_version

