from gym import Env 
from gym.spaces import Discrete, Box
import numpy as np
import random
# from stable_baselines3.common.env_checker import check_env
from simulation_runner import SimulationRunner
from calcul_tools import dist

class ASVEnv(Env):

    def __init__(self):
        # Actions that we can take: turn left, turn right, go straight
        self.action_space = Discrete(3)
        # Distance to objective and risk of collision
        self.observation_space = Box(low=np.array([0, 0]), high=np.array([20, 1]), dtype=np.float64)
        # Set start position of the Boat agent using initialize_sea_objects_random
        runner = SimulationRunner()
        self.boat = runner.initialize_sea_objects_random(["Boat"])[0]
        self.boat.agent = True
        # Set the destination of the Boat agent
        destination_distance = random.uniform(10, 30)
        self.boat.phat = np.array([[self.boat.x + destination_distance * np.cos(self.boat.theta)], [self.boat.y + destination_distance * np.sin(self.boat.theta)]])
        # Set the distance to the objective and the risk of collision
        self.state = np.array([dist(np.array([[self.boat.x], [self.boat.y]]), self.boat.phat), self.boat.collision_risk], dtype=np.float64)
        # Set the simulation lenght
        self.simulation_length = 120




    def step(self, action):
        # Apply action
        # 0 = turn left
        # 1 = turn right
        # 2 = go straight
        # TODO: Implement action
        
        # Recalculation of the boat's position and risk of collision
        self.state = np.array([dist(np.array([[self.boat.x], [self.boat.y]]), self.boat.phat), self.boat.collision_risk], dtype=np.float64)



        # Reduce shower length by 1 second
        self.simulation_length -= 1

        # TODO: Implement reward
        # Calculate reward
        if self.state >= 37 and self.state <= 39:
            reward = 1
        else:
            reward = -1

        # Check if simulation is done
        if self.simulation_length <= 0:
            done = True
        else:
            done = False

        # Set placeholder for info
        info = {}
        return np.array([self.state], dtype=np.float64), reward, done, info

    
    def render(self):
        pass
    
    def reset(self):
        # Reset boat position and destination
        runner = SimulationRunner()
        self.boat = runner.initialize_sea_objects_random(["Boat"])[0]
        # Set the destination of the Boat agent
        destination_distance = random.uniform(10, 30)
        self.boat.phat = np.array([[self.boat.x + destination_distance * np.cos(self.boat.theta)], [self.boat.y + destination_distance * np.sin(self.boat.theta)]])
        # Set the distance to the objective and the risk of collision
        self.state = np.array([dist(np.array([[self.boat.x], [self.boat.y]]), self.boat.phat), 0], dtype=np.float64)

        # Reset simulation time
        self.simulation_length = 60
        return np.array([self.state], dtype=np.float64)
    

env = ASVEnv()
print(env.state)
# check_env(env)