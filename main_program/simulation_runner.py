from calcul_tools import *
from draw import *
from simulation import Simulation
from boat import Boat
from whale import Whale
from fisherman import Fisherman
from island import Island
from ship import Ship
from rules import RuleApplicationWindow
import threading


class SimulationRunner:
    def __init__(self):
        self.s = 15 
        self.dt = 0.1 
        self.k = 0.5 
        self.num_steps = 1000
        self.rules = ["finish overtaking the obstacle", "overtaking the obstacle on the left side", 
                      "overtaking the obstacle on the right side", "red to red rule to avoid the collision"]

    def initialize_sea_objects(self):
        sea_objects = []
        sea_objects.append(Whale(-0.5, -3.5, 1.5, 1.5))      
        sea_objects.append(Boat(-3, 5, 1.5, 0.25))  
        sea_objects.append(Island(0, 2, 0, 1))
        sea_objects.append(Ship(10, -4, 1.5, 3))  
        return sea_objects

    def run(self):
        ax = init_figure(-self.s, self.s, -self.s, self.s)
        sea_objects = self.initialize_sea_objects()
        simulation = Simulation(sea_objects, self.dt, self.k)
        rule_window = RuleApplicationWindow(self.rules)
        simulation.run(self.num_steps, ax, 2, self.s, rule_window)
        threading.Thread(target=rule_window.run).start()

    # ------------------------------------------------------------------------------------------------

""" Examples of initial position to test different cases """

''' Four boats '''
# boats.append(Ship(-2.5, -3.5, 1.5, 0.25))  # x,y,v,θ of the boat
# boats.append(Fisherman(1.5, 1.5, 0.5, 1))  # x,y,v,θ of the boat
# boats.append(Boat(-1, 3, 1.5, 4.75))  # x,y,v,θ of the boat
# boats.append(Boat(0, 0, 0.25, 2))

''' Left lower zone '''
# xp = array([[-2.5,-5,2,1]]).T      #x,y,v,θ of the boat
# xq = array([[2,0,0.25,2]]).T    #x,y,v,θ of the obstacle boat

''' Right lower zone '''
# xp = array([[5,-6,1.5,2]]).T      #x,y,v,θ of the boat
# xq = array([[0,0,0.25,2]]).T    #x,y,v,θ of the obstacle boat

''' Left upper zone '''
# xp = array([[-1,2,1.5,5]]).T      #x,y,v,θ of the boat
# xq = array([[0,-2,0.25,2]]).T    #x,y,v,θ of the obstacle boat

''' Right upper zone '''
# xp = array([[3,3,1.5,4]]).T      #x,y,v,θ of the boat
# xq = array([[0,-2,0.25,2]]).T    #x,y,v,θ of the obstacle boat

''' Opposite direction '''
# xp = array([[-1, 3, 1.5, 4.75]]).T      #x,y,v,θ of the boat
# xq = array([[0,-2, 0.25, 1.75]]).T    #x,y,v,θ of the obstacle boat

# xp = array([[3, 3, 1.5, 4.75]]).T      #x,y,v,θ of the boat
# xq = array([[0,-2, 0.25, 1.75]]).T    #x,y,v,θ of the obstacle boat

